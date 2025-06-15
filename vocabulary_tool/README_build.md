# 🛠️ Instruções de Build (README_build.md)

Este documento explica como usar os scripts `.bat` para compilar a aplicação num executável (`.exe`) usando o PyInstaller.

---

## Visão Geral

Para facilitar o processo de empacotamento, o projeto inclui scripts que automatizam os comandos do PyInstaller. Existem duas versões principais, cada uma para um propósito diferente.

---

## Scripts Disponíveis

### 1. `build_dev.bat` (Para Desenvolvimento e Testes)

Este é o script recomendado para usar durante o desenvolvimento.

- **O que faz:** Cria um executável que, ao ser executado, **mostra uma janela de terminal (consola)**.
- **Utilidade:** Essencial para depuração. Se ocorrer algum erro durante a execução, as mensagens aparecerão nesta janela de terminal, ajudando a identificar o problema.

```batch
@echo off
pyinstaller run_app.py ^
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
```

### 2. `build.bat` (Para a Versão Final do Utilizador)

Este script deve ser usado para criar a versão que será distribuída aos utilizadores finais. Ele corresponde ao script que estávamos a editar.

- **O que faz:** Cria um executável que **NÃO mostra uma janela de terminal**, graças à flag `--windowed`. A aplicação abre diretamente no navegador.
- **Utilidade:** Proporciona uma experiência de utilizador mais limpa e profissional. Use este script apenas quando tiver a certeza de que a aplicação está estável.

```batch
@echo off
pyinstaller run_app.py ^
--name "VocabularyGenerator" ^
--onefile ^
--windowed ^
--noconfirm ^
--add-data "app.py;." ^
--add-data "backend;backend" ^
--add-data "models;models" ^
--add-data "utils;utils" ^
--add-data "data;data"
```

---

## Como Usar

1. **Escolha o script** apropriado para a sua necessidade (desenvolvimento ou versão final).
2. **Clique duas vezes** no ficheiro `.bat` desejado.
3. Aguarde a conclusão do processo. Uma janela de terminal aparecerá e fechará sozinha quando o processo terminar.

---

## Resultado

Após a execução de qualquer um dos scripts, será criada uma pasta `dist`. Dentro dela, encontrará o ficheiro `.exe` pronto para ser usado e distribuído.
