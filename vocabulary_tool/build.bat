@echo off
echo === Iniciando empacotamento com PyInstaller ===

REM Caminho relativo da pasta atual
cd /d %~dp0

REM Empacotar com PyInstaller
pyinstaller gerador_vocabulario.spec

echo === Empacotamento concluido! Executavel gerado em /dist ===
pause
