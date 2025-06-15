import os
import requests
from typing import Tuple
from dotenv import load_dotenv
from utils.helpers import resource_path

# Carrega o .env a partir do caminho correto
dotenv_path = resource_path(".env")
load_dotenv(dotenv_path=dotenv_path)

# Validação: Garante que a chave da API foi carregada
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
if not DEEPL_API_KEY:
    raise ValueError("A chave DEEPL_API_KEY não foi encontrada. Verifique o seu ficheiro .env.")

# URL da API do DeepL (versão gratuita)
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
    """
    Traduz uma frase e uma palavra específica usando a API do DeepL.

    Args:
        sentence: A frase de exemplo a ser traduzida.
        word: A palavra específica a ser traduzida.
        source_lang: O código do idioma de origem (ex: 'EN', 'DE').
        target_lang: O código do idioma de destino (ex: 'PT-BR').

    Returns:
        Uma tupla contendo (tradução_da_frase, tradução_da_palavra).

    Raises:
        DeepLError: Se ocorrer um erro durante a comunicação com a API do DeepL.
    """
    headers = {
        "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}"
    }
    # Envia a frase e a palavra na mesma requisição para maior eficiência
    data = {
        "text": [sentence, word],
        "source_lang": source_lang,
        "target_lang": target_lang,
    }

    try:
        response = requests.post(DEEPL_API_URL, headers=headers, data=data)

        # Lança uma exceção para erros HTTP (4xx, 5xx)
        response.raise_for_status()

        result = response.json()

        # Verifica se a resposta contém as traduções esperadas
        if "translations" not in result or len(result["translations"]) < 2:
            raise DeepLError("A resposta da API do DeepL está malformada.")

        sentence_translation = result["translations"][0]["text"]
        word_translation = result["translations"][1]["text"]

        return sentence_translation, word_translation

    except requests.exceptions.HTTPError as e:
        # Erros específicos de HTTP, como chave de API inválida (403) ou cota excedida (456)
        if e.response.status_code == 403:
            raise DeepLError("Erro de autenticação. A chave da API do DeepL é inválida.")
        elif e.response.status_code == 456:
             raise DeepLError("Cota da API do DeepL excedida. Tente novamente mais tarde.")
        else:
            raise DeepLError(f"Erro HTTP ao contactar o DeepL: {e}")

    except requests.exceptions.RequestException as e:
        # Erros de rede (timeout, falha de conexão, etc.)
        raise DeepLError(f"Erro de conexão com a API do DeepL: {e}")
    
    except (KeyError, IndexError) as e:
        # Erro se a estrutura da resposta JSON for inesperada
        raise DeepLError(f"Erro ao processar a resposta do DeepL: {e}")

