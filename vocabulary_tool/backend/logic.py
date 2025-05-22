import models.mistral_api as mistral
import models.deepl_api as dl
import backend.database as db
import utils.anki_exporter as anki

def process_new_word(new_word: str, known_words: list[str], level: int, deck: str, lang: str) -> tuple[str, str]:
    sentence = mistral.generate_sentence(new_word, known_words, level, lang)
    translation = dl.translate_text(sentence, lang)
    #eu não quero palavra, frases. quero palavra, idioma, deck, data e dificuldade
    db.add_word(new_word, sentence, translation)
    anki_result = anki.upload(new_word, sentence, translation, deck)
    return sentence, anki_result