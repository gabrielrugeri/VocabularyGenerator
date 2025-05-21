import requests

def build_prompt(new_word, known_words):
    return (
        f"Generate a simple and natural sentence using the word '{new_word}'. "
        f"The sentence should not contain any other uncommon or difficult words. "
        f"Use only words from this known vocabulary list: {', '.join(known_words)}. "
        f"The sentence must be suitable for a language learner who only knows these words."
    )
    
def generate_sentence(new_word, known_words):
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