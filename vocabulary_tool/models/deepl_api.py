import requests
from typing import Tuple
from utils import config_manager # Importa o novo gestor

DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"

class DeepLError(Exception):
    """Exceção customizada para erros relacionados com a API do DeepL."""
    pass

def translate_text(
    sentence: str,
    word: str,
    source_lang: str,
    target_lang: str = "PT-BR"
) -> Tuple[str, str]:
    """Traduz uma frase e uma palavra específica usando a API do DeepL."""
    
    # Obtém a chave do gestor de configuração
    deepl_api_key = config_manager.get_api_key("DEEPL_API_KEY")
    if not deepl_api_key:
        raise DeepLError("A chave da API do DeepL não foi configurada.")

    headers = {
        "Authorization": f"DeepL-Auth-Key {deepl_api_key}"
    }
    data = {
        "text": [sentence, word],
        "source_lang": source_lang,
        "target_lang": target_lang,
    }

    try:
        response = requests.post(DEEPL_API_URL, headers=headers, data=data)
        response.raise_for_status()
        result = response.json()
        if "translations" not in result or len(result["translations"]) < 2:
            raise DeepLError("A resposta da API do DeepL está malformada.")
        return result["translations"][0]["text"], result["translations"][1]["text"]
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            raise DeepLError("Erro de autenticação. A chave da API do DeepL é inválida.")
        else:
            raise DeepLError(f"Erro HTTP ao contactar o DeepL: {e}")
    except requests.exceptions.RequestException as e:
        raise DeepLError(f"Erro de conexão com a API do DeepL: {e}")
    except (KeyError, IndexError) as e:
        raise DeepLError(f"Erro ao processar a resposta do DeepL: {e}")

