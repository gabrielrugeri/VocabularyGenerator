import models.mistral_api as mistral
import models.deepl_api as dl
import backend.database as db
import utils.anki_exporter as anki

def process_new_word(new_word, known_words):
    sentence = mistral.generate_sentence(new_word, known_words)
    translation = dl.translate_text(sentence)
    db.add_word(new_word, sentence, translation)
    anki_result = anki.send_to_anki(new_word, sentence, translation)
    return sentence, translation, anki_result