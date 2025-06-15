import subprocess
import os
import sys

def get_app_path():
    """Obtém o caminho para o app.py, funcionando em dev e no executável."""
    if hasattr(sys, '_MEIPASS'):
        # Caminho quando executado pelo PyInstaller
        return os.path.join(sys._MEIPASS, 'app.py')
    # Caminho em desenvolvimento normal
    return os.path.join(os.path.dirname(__file__), 'app.py')

def run_streamlit():
    """Executa o comando do Streamlit com as flags corretas para cada SO."""
    app_path = get_app_path()
    command = ["streamlit", "run", app_path]
    
    if sys.platform == "win32":
        try:
            # Esta flag é a chave para suprimir a janela do terminal
            creation_flags = subprocess.CREATE_NO_WINDOW
            subprocess.run(command, check=True, creationflags=creation_flags)
        except AttributeError:
            # Fallback para versões mais antigas do Python que possam não ter a flag
            # (embora seja improvável)
            subprocess.run(command, check=True)
    else:
        # Em outros sistemas (Linux, macOS), a janela não é um problema.
        subprocess.run(command, check=True)

if __name__ == "__main__":
    try:
        run_streamlit()
    except FileNotFoundError:
        # Este erro só seria visível se executado num terminal, mas é uma boa prática
        print("ERRO: Comando 'streamlit' não encontrado. O Streamlit está instalado?")
    except subprocess.CalledProcessError as e:
        print(f"ERRO: A aplicação Streamlit terminou inesperadamente: {e}")
    except Exception as e:
        # Grava um ficheiro de log em caso de erro fatal
        with open("error_log.txt", "w") as f:
            f.write(f"Ocorreu um erro inesperado ao iniciar a aplicação:\n{str(e)}")

