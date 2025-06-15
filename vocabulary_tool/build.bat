@echo off
echo === Iniciando empacotamento com PyInstaller (sem terminal) ===

REM Garante que o script esta a ser executado a partir do seu proprio diretorio
cd /d %~dp0

REM Empacota o ficheiro .pyw para garantir que nenhuma janela de console apareca.
pyinstaller run_app.pyw ^
--name "VocabularyGenerator" ^
--onefile ^
--windowed ^
--icon="icon.ico" ^
--noconfirm ^
--add-data "app.py;." ^
--add-data "backend;backend" ^
--add-data "models;models" ^
--add-data "utils;utils" ^
--add-data "data;data"

echo.
echo === Empacotamento concluido! ===
echo O seu executavel unico foi gerado em 'dist/VocabularyGenerator.exe'.
echo.
pause