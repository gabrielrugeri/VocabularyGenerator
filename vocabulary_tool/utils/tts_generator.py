"""
tts_generator.py - Módulo para gerar ficheiros de áudio TTS usando a API do Google.
"""
from gtts import gTTS, gTTSError
import os
import time

class TTSGeneratorError(Exception):
    """Exceção customizada para erros de geração de TTS."""
    pass

def create_audio_file(text: str, lang_code: str, deck_name: str) -> str:
    """
    Cria um ficheiro de áudio .mp3 a partir de um texto.

    Args:
        text: O texto a ser convertido em áudio.
        lang_code: O código do idioma (ex: 'en', 'pt', 'es').
        deck_name: O nome do baralho, usado para organizar os ficheiros.

    Returns:
        O nome do ficheiro de áudio gerado.

    Raises:
        TTSGeneratorError: Se a geração do áudio falhar.
    """
    try:
        # Cria um nome de ficheiro único para evitar colisões
        # Ex: anki_tts_English_Vocabulary_1623456789.mp3
        sanitized_deck = "".join(c for c in deck_name if c.isalnum())
        filename = f"anki_tts_{sanitized_deck}_{int(time.time() * 100)}.mp3"

        # Gera o áudio
        tts = gTTS(text=text, lang=lang_code, slow=False)
        
        # Salva o ficheiro temporariamente
        temp_path = os.path.join("temp_audio") # Uma pasta temporária
        os.makedirs(temp_path, exist_ok=True)
        full_temp_path = os.path.join(temp_path, filename)
        
        tts.save(full_temp_path)
        
        return filename

    except gTTSError as e:
        raise TTSGeneratorError(f"gTTS API error: {e}")
    except Exception as e:
        raise TTSGeneratorError(f"Failed to create audio file: {e}")

