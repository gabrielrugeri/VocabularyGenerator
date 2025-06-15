# utils/helpers.py
import sys
import os

def resource_path(relative_path):
    """ Retorna o caminho absoluto para o recurso, funciona para dev e PyInstaller """
    try:
        # PyInstaller cria uma pasta temp e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Se não estiver a correr como um executável, o caminho base é o diretório do projeto
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    return os.path.join(base_path, relative_path)