"""
config_manager.py - Gere o carregamento e o armazenamento das chaves de API
num ficheiro de configuração local.
"""
import configparser
import os
import sys
from typing import Union # Importa o Union para compatibilidade

CONFIG_DIR_NAME = "VocabularyGenerator"
CONFIG_FILE_NAME = "config.ini"

def get_config_path() -> str:
    """Obtém o caminho para o ficheiro de configuração, criando a pasta se necessário."""
    if sys.platform == "win32":
        # Usa a pasta %APPDATA% no Windows
        config_dir = os.path.join(os.environ['APPDATA'], CONFIG_DIR_NAME)
    else:
        # Usa a pasta ~/.config/ no Linux/macOS
        config_dir = os.path.join(os.path.expanduser('~'), '.config', CONFIG_DIR_NAME)
    
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, CONFIG_FILE_NAME)

def load_config() -> configparser.ConfigParser:
    """Carrega a configuração do ficheiro .ini."""
    config = configparser.ConfigParser()
    config_path = get_config_path()
    if os.path.exists(config_path):
        config.read(config_path)
    return config

def save_api_keys(groq_key: str, deepl_key: str):
    """Guarda as chaves de API no ficheiro de configuração."""
    config = configparser.ConfigParser()
    config['API_KEYS'] = {
        'GROQ_API_KEY': groq_key,
        'DEEPL_API_KEY': deepl_key
    }
    config_path = get_config_path()
    with open(config_path, 'w') as configfile:
        config.write(configfile)

def get_api_key(service: str) -> Union[str, None]:
    """Obtém uma chave de API específica da configuração."""
    config = load_config()
    return config.get('API_KEYS', service, fallback=None)

def are_keys_configured() -> bool:
    """Verifica se ambas as chaves de API estão configuradas."""
    groq_key = get_api_key('GROQ_API_KEY')
    deepl_key = get_api_key('DEEPL_API_KEY')
    return bool(groq_key and deepl_key)
