"""
anki_exporter.py - Módulo para interagir com o Anki via AnkiConnect.
Agora com geração de áudio TTS independente.
"""
import requests
import json
import re
import os
import base64
from typing import Dict, List, Optional, Any
from utils.tts_generator import create_audio_file, TTSGeneratorError

class AnkiExporterError(Exception):
    """Exceção customizada para erros relacionados com o AnkiExporter."""
    pass

def _bold_word(word: str, sentence: str) -> str:
    return re.sub(f"\\b{re.escape(word)}\\b", f"<b>{word}</b>", sentence, flags=re.IGNORECASE)

class AnkiExporter:
    def __init__(self, anki_connect_url: str = "http://localhost:8765", highlight_color: str = "#007aff"):
        self.anki_connect_url = anki_connect_url
        self.model_name = "VocabularyGenerator_Audio" # Novo nome do modelo
        self.highlight_color = highlight_color
        self._ensure_model_exists()

    def _request(self, action: str, params: Optional[Dict] = None) -> Any:
        payload = {"action": action, "version": 6, "params": params or {}}
        try:
            response = requests.post(self.anki_connect_url, data=json.dumps(payload), timeout=10)
            response.raise_for_status()
            result = response.json()
            if result.get("error"):
                raise AnkiExporterError(f"API do Anki retornou um erro: {result['error']}")
            return result.get("result")
        except requests.exceptions.RequestException as e:
            raise AnkiExporterError(f"Não foi possível conectar ao Anki. Verifique se ele está aberto e com o AnkiConnect instalado. Erro: {e}")
        except json.JSONDecodeError:
            raise AnkiExporterError("Resposta inválida recebida do AnkiConnect.")

    def _store_media_file(self, filename: str) -> bool:
        """Envia um ficheiro de áudio para a coleção de mídia do Anki."""
        temp_path = os.path.join("temp_audio", filename)
        if not os.path.exists(temp_path):
            raise AnkiExporterError(f"Ficheiro de áudio temporário não encontrado: {temp_path}")

        with open(temp_path, "rb") as f:
            b64_audio = base64.b64encode(f.read()).decode("utf-8")
        
        params = {
            "filename": filename,
            "data": b64_audio
        }
        self._request("storeMediaFile", params)
        os.remove(temp_path) # Limpa o ficheiro temporário
        return True

    def _get_card_css(self) -> str:
        return f""".card {{ font-family: Arial, sans-serif; font-size: 22px; text-align: center; color: #333; background-color: #f7f7f7; }} b {{ color: {self.highlight_color}; }} .phonetic, .translation {{ font-size: 18px; color: #555; }}"""

    def _create_model(self) -> None:
        """Cria o modelo de cartão com um campo para o áudio."""
        params = {
            "modelName": self.model_name,
            "inOrderFields": ["Sentence", "Phonetic", "WordTranslation", "SentenceTranslation", "Audio"],
            "css": self._get_card_css(),
            "cardTemplates": [{
                "Name": "Vocabulary Card",
                "Front": "{{Sentence}}<br><span class='phonetic'>/{{Phonetic}}/</span><br>{{Audio}}",
                "Back": "{{FrontSide}}<hr id=answer><b>{{WordTranslation}}</b><br><span class='translation'>{{SentenceTranslation}}</span>"
            }]
        }
        self._request("createModel", params)

    def _ensure_model_exists(self) -> None:
        if self.model_name not in self._request("modelNames"):
            self._create_model()
            
    def add_card(self, deck_name: str, word: str, sentence: str, phonetic: str, sentence_translation: str, word_translation: str, tts_lang: str, tags: Optional[List[str]] = None) -> int:
        """Adiciona um novo cartão ao Anki, com geração de áudio TTS."""
        try:
            # --- CORREÇÃO ROBUSTA: Converte o código de idioma para o formato esperado pelo gTTS ---
            # Exemplo: 'en_US' ou 'en-US' -> 'en'
            gtts_lang_code = re.split(r'[-_]', tts_lang)[0]
            
            # 1. Gerar o nome do ficheiro de áudio com o código de idioma corrigido
            audio_filename = create_audio_file(sentence, gtts_lang_code, deck_name)
            
            # 2. Enviar o ficheiro para o Anki
            self._store_media_file(audio_filename)
            
            # 3. Preparar a nota com a tag de som
            audio_tag = f"[sound:{audio_filename}]"
            
            params = { "note": { "deckName": deck_name, "modelName": self.model_name, "fields": { "Sentence": _bold_word(word, sentence), "Phonetic": phonetic, "WordTranslation": word_translation, "SentenceTranslation": sentence_translation, "Audio": audio_tag }, "tags": tags or [] } }
            note_id = self._request("addNote", params)

            if not isinstance(note_id, int):
                 raise AnkiExporterError(f"Falha ao adicionar cartão. O Anki não retornou um ID válido.")
            return note_id
            
        except (TTSGeneratorError, AnkiExporterError) as e:
            # Repassa o erro para a camada de lógica
            raise AnkiExporterError(f"Erro ao gerar ou exportar áudio: {e}")

