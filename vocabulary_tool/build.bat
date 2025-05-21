@echo off
echo === Iniciando empacotamento com PyInstaller ===

REM Caminho relativo da pasta atual
cd /d %~dp0

REM Empacotar com PyInstaller
pyinstaller --onefile ^
  --name "Gerador de Vocabulario" ^
  --add-data "data;vocabulary_tool/data" ^
  --add-data ".env;." ^
  --hidden-import "streamlit" ^
  app.py

echo === Empacotamento concluído! Executável gerado em /dist ===
pause
