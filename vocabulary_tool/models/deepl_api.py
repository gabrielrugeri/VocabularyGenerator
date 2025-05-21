import os
import requests
from dotenv import load_dotenv
load_dotenv()

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

def translate_text(text, target_lang="PT"):
    url = "https://api-free.deepl.com/v2/translate"
    headers = {
        "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}"
    }
    data = {
        "text": text,
        "target_lang": target_lang
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        result = response.json()
        return result["translations"][0]["text"]
    except Exception as e:
        return f"[Translation error] {e}"
