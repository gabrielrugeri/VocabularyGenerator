@echo off
REM Este script instala todas as dependencias necessarias para o VocabularyGenerator.
REM Certifique-se de que o Python e o pip estao instalados e no PATH do sistema.

echo ========================================================
echo   Instalador de Dependencias para VocabularyGenerator
echo ========================================================
echo.

REM Verifica se o ficheiro requirements.txt existe
IF NOT EXIST "requirements.txt" (
    echo [ERRO] O ficheiro 'requirements.txt' nao foi encontrado.
    echo Certifique-se de que ele esta na mesma pasta que este script.
    pause
    exit /b 1
)

echo -> A instalar as bibliotecas listadas em requirements.txt...
echo.

pip install -r requirements.txt

REM Verifica se a instalacao foi bem sucedida
IF %errorlevel% NEQ 0 (
    echo.
    echo [ERRO] Ocorreu um erro durante a instalacao.
    echo Verifique as mensagens acima para mais detalhes.
    echo Tente executar o prompt de comando como Administrador.
) ELSE (
    echo.
    echo [SUCESSO] Todas as dependencias foram instaladas com sucesso!
)

echo.
echo Pressione qualquer tecla para sair...
pause > nul