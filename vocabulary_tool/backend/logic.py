# --- Importações Corrigidas para Empacotamento ---
# A configuração do caminho é feita no início do app.py
from backend import database as db
from models import groq_api
from models import deepl_api
from utils.anki_exporter import AnkiExporter, AnkiExporterError
from models.groq_api import GroqAPIError # Mantendo o nome da exceção por consistência
from models.deepl_api import DeepLError
from typing import Set, Tuple, Optional

class LogicError(Exception):
    """Exceção customizada para erros na lógica de processamento que devem ser mostrados ao utilizador."""
    pass

def process_new_word(
    new_word: str,
    known_words: Set[str],
    level: int,
    deck_id: int,
    lang_code: str,
    highlight_color: Optional[str] = "#007aff" # Parâmetro opcional para a cor
) -> Tuple[str, str, str]:
    """
    Orquestra o processo completo: gera conteúdo (incluindo fonética), traduz,
    exporta para o Anki e guarda na base de dados.
    """
    try:
        # --- ETAPA 1: Obter informações da Base de Dados ---
        lang_info = db.get_language_by_iso(lang_code)
        deck_info = db.get_deck_by_id(deck_id)

        if not lang_info:
            raise LogicError(f"Idioma '{lang_code}' não encontrado.")
        if not deck_info:
            raise LogicError(f"Baralho com ID '{deck_id}' não encontrado.")

        deck_name = deck_info["name"]
        lang_tts = lang_info["code_tts"]
        
        # --- ETAPA 2: Gerar Frase, Fonética e Tags com IA ---
        sentence, phonetic, tags = groq_api.generate_card_content(new_word, known_words, level, lang_code)

        # --- ETAPA 3: Traduzir conteúdo com DeepL ---
        sentence_translation, word_translation = deepl_api.translate_text(
            sentence=sentence,
            word=new_word,
            source_lang=lang_code.upper()
        )
        
        # --- ETAPA 4: Exportar para o Anki ---
        # Instancia o exportador com a cor de destaque
        exporter = AnkiExporter(highlight_color=highlight_color)
        card_id = exporter.add_card(
            deck_name=deck_name,
            word=new_word,
            sentence=sentence,
            phonetic=phonetic,
            sentence_translation=sentence_translation,
            word_translation=word_translation,
            tts_lang=lang_tts,
            tags=tags
        )
        
        # --- ETAPA 5: Persistir na Base de Dados ---
        db.add_word(new_word, lang_code, deck_id, level)

        # --- ETAPA 6: Retornar dados para a Interface ---
        success_message = f"Cartão adicionado ao Anki com sucesso! (ID: {card_id})"
        return sentence, sentence_translation, success_message

    except (GroqAPIError, DeepLError, AnkiExporterError) as api_error:
        raise LogicError(str(api_error))
        
    except Exception as e:
        print(f"DEBUG: Erro inesperado em logic.py: {e}")
        raise LogicError("Ocorreu um erro inesperado. Verifique o terminal para mais detalhes.")
