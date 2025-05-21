import json
import requests

def build_prompt(new_word, known_words):
    return (
        f"Generate a simple and natural sentence using the word '{new_word}'. "
        f"The sentence should not contain any other uncommon or difficult words. "
        f"Use only words from this known vocabulary list: {', '.join(known_words)}. "
        f"The sentence must be suitable for a language learner who only knows these words."
    )
    
def load_known_words(file_path="vocab.json"):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            return list(data.get("known_words", []))
    except FileNotFoundError:
        return []

def generate_sentence_with_mistral(new_word, known_words):
    prompt = build_prompt(new_word, known_words)
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False}
        )
        result = response.json()
        return result["response"].strip()
    except Exception as e:
        return f"Error generating sentence: {e}"
        
def save_word_to_vocab(new_word, file_path="vocab.json"):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"known_words": []}

    if new_word not in data["known_words"]:
        data["known_words"].append(new_word)
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

def frase_ok(frase, vocab, nova):
    palavras = set(frase.lower().replace('.', '').replace(',', '').split())
    desconhecidas = palavras - vocab
    return desconhecidas <= {nova.lower()}

def enviar_para_anki(palavra, frase):
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": "English",
                "modelName": "Basic",
                "fields": {
                    "Front": frase.replace(palavra, f"<b>{palavra}</b>"),
                    "Back": palavra
                },
                "tags": ["idioma_helper"]
            }
        }
    }
    res = requests.post("http://localhost:8765", json=payload)
    return res.json()

def main():
    vocab = load_known_words()
    nova = input("Qual palavra você quer aprender? ").strip()

    if nova in vocab:
        print("Você já conhece essa palavra!")
        return

    frase = generate_sentence_with_mistral(nova, vocab)
    print("Frase gerada:", frase)

    if frase_ok(frase, vocab, nova):
        enviar_para_anki(nova, frase)
        vocab.add(nova)
        print("Frase enviada para o Anki!")
    else:
        print("A frase tem palavras difíceis. Tente outra.")

if __name__ == "__main__":
    main()
