import json
import requests

def carregar_vocab():
    with open("vocab.json", "r") as f:
        return set(json.load(f))

def salvar_vocab(vocab):
    with open("vocab.json", "w") as f:
        json.dump(list(vocab), f)

def gerar_frase(palavra):
    prompt = f"Write a simple English sentence using the word '{palavra}'. Use only basic vocabulary."

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": prompt},
        stream=True  # <- IMPORTANTE para processar resposta em partes
    )

    resposta_completa = ""
    for linha in response.iter_lines():
        if linha:
            try:
                dados = json.loads(linha)
                resposta_completa += dados.get("response", "")
            except json.JSONDecodeError:
                continue  # ignora linhas inválidas

    return resposta_completa.strip()

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
    vocab = carregar_vocab()
    nova = input("Qual palavra você quer aprender? ").strip()

    if nova in vocab:
        print("Você já conhece essa palavra!")
        return

    frase = gerar_frase(nova)
    print("Frase gerada:", frase)

    if frase_ok(frase, vocab, nova):
        enviar_para_anki(nova, frase)
        vocab.add(nova)
        salvar_vocab(vocab)
        print("Frase enviada para o Anki!")
    else:
        print("A frase tem palavras difíceis. Tente outra.")

if __name__ == "__main__":
    main()
