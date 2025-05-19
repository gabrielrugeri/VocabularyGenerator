import requests

def translate_with_deepl(text, source_lang="EN", target_lang="PT"):
    url = "https://api-free.deepl.com/v2/translate"
    headers = {"Authorization": "DeepL-Auth-Key YOUR_API_KEY"}
    data = {
        "text": text,
        "source_lang": source_lang,
        "target_lang": target_lang
    }
    response = requests.post(url, data=data, headers=headers)
    return response.json()["translations"][0]["text"]
