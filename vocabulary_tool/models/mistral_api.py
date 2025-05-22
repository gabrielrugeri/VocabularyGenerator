import requests
from backend.level import Difficulty

def build_prompt(new_word: str, known_words: list[str], difficulty: int, lang: str = 'EN') -> str:
    written_level = Difficulty.get_level(difficulty)
    
    difficulty_instructions = {
        1: "Use very short sentences (3-5 words) with basic structure.",
        2: "Use simple sentences (5-7 words) with one basic conjunction if needed.",
        3: "You may use slightly longer sentences (7-10 words) with one or two conjunctions."
    }
    
    return (
        f"Generate a simple and natural {written_level}-difficulty sentence in {lang} using the word '{new_word}'. "
        f"The sentence should not contain any other uncommon or difficult words. "
        f"Use only words from this known vocabulary list: {', '.join(known_words)}. "
        f"{difficulty_instructions.get(difficulty, '')} "
        f"The sentence must be suitable for a language learner who only knows these words. "
        f"Ensure the sentence demonstrates the meaning of '{new_word}' clearly in context."
    )
    
def generate_sentence(new_word: str, known_words: list[str], difficulty: int) -> str:
    prompt = build_prompt(new_word, known_words, difficulty)
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False}
        )
        result = response.json()
        return result["response"].strip()
    except Exception as e:
        return f"Error generating sentence: {e}"