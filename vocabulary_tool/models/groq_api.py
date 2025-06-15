import os
from groq import Groq, GroqError
from typing import Tuple, List, Set
import re

# --- CORREÇÃO: Importar o gestor de configuração ---
from utils import config_manager
import backend.database as db
from backend.level import Difficulty

class GroqAPIError(Exception):
    """Exceção customizada para erros relacionados com a API."""
    pass

# --- Configuração do Cliente da API ---
try:
    groq_api_key = config_manager.get_api_key("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("A chave GROQ_API_KEY não foi configurada.")
    client = Groq(api_key=groq_api_key)
except ValueError as e:
    # Esta exceção será levantada na primeira vez que a app corre, o que é esperado.
    # A app principal irá lidar com isto mostrando o ecrã de configuração.
    pass
except Exception as e:
    raise GroqAPIError(f"Erro inesperado na inicialização da API do Groq: {e}")

def build_prompt(new_word: str, known_words: Set[str], difficulty: int, lang_code: str) -> str:
    """Constrói um prompt detalhado para o LLM"""
    lang_info = db.get_language_by_iso(lang_code)
    if not lang_info:
        raise GroqAPIError(f"O idioma com o código '{lang_code}' não foi encontrado.")
        
    lang_name = lang_info['name_en']
    written_level = Difficulty.get_level(difficulty)
    
    difficulty_instructions = {
        1: "Use very short sentences (3-5 words).",
        2: "Use simple sentences (5-8 words).",
        3: "You can use slightly longer sentences (8-12 words)."
    }

    known_words_sample = ", ".join(list(known_words)[:50]) if known_words else "any common words"

    return (
        f"You are a language learning assistant. Your task is to generate three pieces of educational content in {lang_name} for the word '{new_word}'.\n\n"
        f"1. **Sentence:** Create one single, clear, {written_level}-difficulty sentence in **{lang_name}** that prominently features the word **'{new_word}'**.\n"
        f"2. **Phonetic:** Provide the International Phonetic Alphabet transcription for '{new_word}'.\n"
        f"3. **Tags:** Provide a list of 3-5 relevant learning tags in **{lang_name}** for the word '{new_word}'.\n\n"
        f"**IMPORTANT**: Respond ONLY in the following format, with nothing before or after:\n"
        f"Sentence: [The generated sentence goes here]\n"
        f"Phonetic: [The IPA transcription goes here]\n"
        f"Tags: [tag1, tag2, tag3]"
    )

def _parse_response(response_text: str) -> Tuple[str, str, List[str]]:
    """Processa a resposta de texto do modelo de forma robusta para extrair frase, fonética e tags."""
    try:
        match = re.search(
            r"Sentence:\s*(?P<sentence>.*?)\s*\n\s*Phonetic:\s*(?P<phonetic>.*?)\s*\n\s*Tags:\s*(?P<tags>.*)", 
            response_text, 
            re.DOTALL | re.IGNORECASE
        )
        if not match:
            raise GroqAPIError(f"A resposta da API não seguiu o formato esperado. Resposta: '{response_text[:150]}...'")

        sentence = match.group('sentence').strip()
        phonetic = match.group('phonetic').strip()
        tags_str = match.group('tags').strip().strip("[]'\"")
        tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]

        if not sentence or not phonetic or not tags:
             raise GroqAPIError("A API retornou um campo (frase, fonética ou tags) vazio.")
        return sentence, phonetic, tags
    except Exception as e:
        raise GroqAPIError(f"Falha ao processar a resposta da API: {e}")

def generate_card_content(new_word: str, known_words: Set[str], difficulty: int, lang_code: str) -> Tuple[str, str, List[str]]:
    """Gera o conteúdo completo para um cartão (frase, fonética, tags) usando a API do Groq."""
    prompt = build_prompt(new_word, known_words, difficulty, lang_code)
    
    try:
        # Re-inicializa o cliente aqui para garantir que a chave mais recente seja usada
        # após a configuração inicial.
        groq_api_key = config_manager.get_api_key("GROQ_API_KEY")
        if not groq_api_key:
            raise GroqAPIError("A chave da API do Groq não está configurada. Por favor, configure-a na aplicação.")
        
        local_client = Groq(api_key=groq_api_key)

        chat_completion = local_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            temperature=0.6,
        )
        response_content = chat_completion.choices[0].message.content
        if not response_content:
            raise GroqAPIError("A API retornou uma resposta vazia.")
        
        return _parse_response(response_content)
        
    except GroqError as e:
        raise GroqAPIError(f"Erro na API do Groq: {e.body.get('message', str(e))}")
    except Exception as e:
        raise GroqAPIError(f"Erro inesperado ao contactar a API: {e}")

