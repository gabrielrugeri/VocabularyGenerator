import os
import requests
from dotenv import load_dotenv
load_dotenv()

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

#INCLUIR TRADUÇÃO DA PALAVRA ESPECÍFICA?

def translate_text(text: str, source_lang: str = "EN", target_lang: str = "PT-BR") -> str:
    url = "https://api-free.deepl.com/v2/translate"
    headers = {
        "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}"
    }
    data = {
        "text": text,
        "source_lang": source_lang,
        "target_lang": target_lang
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        result = response.json()
        return result["translations"][0]["text"]
    except Exception as e:
        return f"[Translation error] {e}"
