import subprocess
import sys
import os
import tempfile
import shutil
from dotenv import load_dotenv

load_dotenv()

def resource_path(relative_path):
    """Retorna caminho absoluto (funciona com PyInstaller)"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

def main():
    temp_dir = tempfile.mkdtemp()

    # Copia todos os arquivos necessários
    required = [
        "app.py",
        "backend",
        "models",
        "utils",
        "data",
        ".env"
    ]

    for item in required:
        src = resource_path(item)
        dst = os.path.join(temp_dir, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        elif os.path.isfile(src):
            shutil.copy2(src, dst)

    # Define PYTHONPATH e executa
    env = os.environ.copy()
    env["PYTHONPATH"] = temp_dir

    subprocess.run(["streamlit", "run", os.path.join(temp_dir, "app.py")], env=env)

if __name__ == "__main__":
    main()
