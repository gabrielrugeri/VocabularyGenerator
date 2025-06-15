# lancher.py
import subprocess
import os
import sys

# Obtém o caminho para o ficheiro principal da aplicação
# Este método garante que funciona tanto em desenvolvimento como no executável
if hasattr(sys, '_MEIPASS'):
    # Caminho quando executado pelo PyInstaller
    APP_PATH = os.path.join(sys._MEIPASS, 'app.py')
else:
    # Caminho em desenvolvimento normal
    APP_PATH = os.path.join(os.path.dirname(__file__), 'app.py')

# Comando para iniciar o Streamlit
command = ["streamlit", "run", APP_PATH]

# Executa o comando
try:
    subprocess.run(command, check=True)
except FileNotFoundError:
    print("Erro: 'streamlit' não encontrado. Certifique-se de que está instalado e no PATH do sistema.")
except subprocess.CalledProcessError as e:
    print(f"A aplicação Streamlit terminou com um erro: {e}")