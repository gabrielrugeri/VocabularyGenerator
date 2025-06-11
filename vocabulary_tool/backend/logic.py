import models.mistral_api as mistral
import models.deepl_api as dl
import backend.database as db
from utils.anki_exporter import AnkiExporter

def process_new_word(
    new_word: str,
    known_words: list[str],
    level: int,
    deck: int,
    lang:str
    ) -> tuple[str, str]:
    
    sentence, tags = mistral.generate_sentence_and_tags(new_word, known_words, level, lang)

    translation = dl.translate_text(sentence, lang.upper())
    
    db.add_word(new_word, lang, deck, level)

    lang_tts = db.get_language_by_iso(lang)["code_tts"]
    deck_info = db.get_deck_by_id(deck)
    if deck_info is None:
        raise ValueError(f"Deck with ID {deck} not found")
    deck_name = deck_info["name"]
    exporter = AnkiExporter()
    anki_result = exporter.add_card(deck_name, sentence, translation, lang_tts, tags=tags)

    return sentence, anki_result