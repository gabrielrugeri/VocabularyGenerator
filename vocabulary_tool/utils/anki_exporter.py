import requests

def send_to_anki(word, sentence, translation, deck_name="VocabularyBuilder", model_name="Basic"):
    front = sentence.replace(word, f"<b>{word}</b>")
    back = f"{word} — {translation}\n\n{sentence}"

    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck_name,
                "modelName": model_name,
                "fields": {
                    "Front": front,
                    "Back": back
                },
                "tags": ["vocabtool"],
                "options": {
                    "allowDuplicate": False
                }
            }
        }
    }

    try:
        response = requests.post("http://localhost:8765", json=payload)
        result = response.json()
        if result.get("error") is None:
            return "✅ Card sent to Anki."
        else:
            return f"⚠️ Anki error: {result['error']}"
    except Exception as e:
        return f"❌ Could not connect to Anki: {e}"
