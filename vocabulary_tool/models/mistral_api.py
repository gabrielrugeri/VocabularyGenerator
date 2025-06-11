import requests
import backend.database as db
from typing import Tuple
from backend.level import Difficulty

def build_prompt(new_word: str, known_words: list[str], difficulty: int, lang_code: str) -> str:
    written_level = Difficulty.get_level(difficulty)
    
    difficulty_instructions = {
        1: "Use very short sentences (3-5 words) with basic structure.",
        2: "Use simple sentences (5-7 words) with one basic conjunction if needed.",
        3: "You may use slightly longer sentences (7-10 words) with one or two conjunctions."
    }
    
    lang_name = db.get_language_by_iso(lang_code)['name_en']
    
    return (
        f"Generate two outputs for language learning:\n\n"
        f"1. A {written_level}-difficulty sentence in {lang_name} using the word '{new_word}'.\n"
        f"   - Use only words from this list: {', '.join(known_words)}\n"
        f"   - {difficulty_instructions.get(difficulty, '')}\n"
        f"   - Clearly demonstrate the meaning of '{new_word}' in context\n\n"
        f"2. A short list of 3-5 related tags (in {lang_name}) for vocabulary categorization.\n"
        f"   - Tags should be simple, relevant to '{new_word}', and useful for flashcards\n"
        f"   - Example format: ['tag1', 'tag2', 'tag3']\n\n"
        f"Output format:\n"
        f"Sentence: [generated sentence]\n"
        f"Tags: [comma-separated tags]"
    )
    
def generate_sentence_and_tags(new_word: str, known_words: list[str], difficulty: int, lang_code: str) -> Tuple[str, list[str]]:
    """
    Gera uma frase e tags relacionadas usando o modelo Mistral
    
    Args:
        new_word: Palavra para incluir na frase
        known_words: Lista de palavras conhecidas
        difficulty: Nível de dificuldade (1-3)
        lang_code: Código do idioma (ex: 'en_US')
    
    Returns:
        Tupla com (frase_gerada, lista_de_tags)
        Em caso de erro: (mensagem_de_erro, lista_vazia)
    """
    prompt = build_prompt(new_word, known_words, difficulty, lang_code)
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False},
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        
        # Processa a resposta para extrair frase e tags
        full_response = result["response"].strip()
        
        # Separa a frase das tags
        if "Sentence:" in full_response and "Tags:" in full_response:
            sentence_part, tags_part = full_response.split("Tags:")
            sentence = sentence_part.replace("Sentence:", "").strip()
            
            # Extrai as tags removendo colchetes e aspas
            tags_str = tags_part.strip().strip("[]").replace("'", "")
            tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]
            
            return (sentence, tags)
        else:
            return (full_response, [])  # Fallback para respostas não formatadas
            
    except requests.exceptions.RequestException as e:
        return (f"API Error: {str(e)}", [])
    except (KeyError, json.JSONDecodeError) as e:
        return (f"Response parsing error: {str(e)}", [])
    except Exception as e:
        return (f"Unexpected error: {str(e)}", [])