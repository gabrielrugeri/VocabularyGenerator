:: build.bat
@echo off
echo === Iniciando empacotamento com PyInstaller ===

REM Garante que o script esta a ser executado a partir do seu proprio diretorio
cd /d %~dp0

REM Empacotar com PyInstaller usando o caractere de continuacao de linha correto (^)
REM e o separador de caminho recomendado (;)
pyinstaller launcher.py ^
--name "VocabularyGenerator" ^
--noconfirm ^
--add-data "app.py;." ^
--add-data "backend;backend" ^
--add-data "models;models" ^
--add-data "utils;utils" ^
--add-data "data;data" ^
--add-data ".env;."

echo.
echo === Empacotamento concluido! ===
echo O seu projeto foi gerado na pasta 'dist/VocabularyGenerator'.
echo.
pause
