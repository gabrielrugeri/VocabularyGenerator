# 🚀 Gerador de Vocabulário para Anki (Vocabulary Generator)

Uma ferramenta poderosa para automatizar a criação de cartões de estudo (flashcards) para o Anki, enriquecidos com frases de exemplo, áudio TTS, transcrição fonética e traduções, tudo gerado por IA.

---

## ✨ Funcionalidades

- **Geração Inteligente:** Cria frases de exemplo que utilizam a palavra que você quer aprender, adaptadas ao seu nível de conhecimento (iniciante, intermediário, avançado).
- **Enriquecimento Completo:** Adiciona automaticamente a transcrição fonética (IPA), a tradução da frase e a tradução da palavra isolada.
- **Áudio Integrado:** Gera o áudio (TTS) da frase de exemplo e anexa-o diretamente ao cartão, sem depender de add-ons do Anki.
- **Integração com Anki:** Conecta-se diretamente ao seu Anki (via AnkiConnect) para adicionar os cartões ao baralho que você escolher.
- **Personalização:** Permite escolher a cor de destaque da palavra nos cartões para uma revisão visual mais agradável.
- **Suporte Multilíngue:** Estruturado para funcionar com diversos idiomas.

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de que tem os seguintes programas instalados no seu computador:

1.  **Python:** Versão 3.9 ou superior. Pode descarregar em [python.org](https://www.python.org/). **Importante:** Durante a instalação, marque a opção "Add Python to PATH".
2.  **Anki:** O software de flashcards. Pode descarregar em [apps.ankiweb.net](https://apps.ankiweb.net/).
3.  **Add-on AnkiConnect:** Essencial para que esta ferramenta possa comunicar com o Anki.
    - No Anki, vá a `Ferramentas > Complementos > Obter complementos...`
    - Cole o seguinte código: `2055492159`
    - Reinicie o Anki após a instalação.

---

## 🛠️ Instalação e Configuração

Siga estes passos para preparar a aplicação para ser usada.

### Passo 1: Descarregar o Projeto

- Descarregue os ficheiros deste repositório. Pode clicar em `Code > Download ZIP` ou usar o Git.
- Extraia os ficheiros para uma pasta da sua preferência no seu computador.

### Passo 2: Instalar as Dependências

- Dentro da pasta do projeto, encontrará um ficheiro chamado `install_dependencies.bat`.
- **Clique duas vezes** neste ficheiro. Ele abrirá uma janela de terminal e instalará automaticamente todas as bibliotecas Python necessárias.

### Passo 3: Configurar as Chaves de API

A aplicação precisa de chaves de API para os serviços de IA e tradução.

1.  Na pasta do projeto, crie um novo ficheiro de texto e renomeie-o para exatamente `.env` (sem nenhum nome antes do ponto).
2.  Abra este ficheiro `.env` com um editor de texto (como o Bloco de Notas) e cole o seguinte conteúdo:

    ```
    DEEPL_API_KEY=sua_chave_aqui
    GROQ_API_KEY=sua_chave_aqui
    ```

3.  **Substitua `sua_chave_aqui`** pelas suas chaves reais:
    - **DEEPL_API_KEY:** Obtenha uma chave gratuita no site do [DeepL API](https://www.deepl.com/pro-api).
    - **GROQ_API_KEY:** Obtenha uma chave gratuita no site do [Groq](https://console.groq.com/).

4.  Salve e feche o ficheiro.

---

## ▶️ Como Usar

1.  **Abra o Anki:** A aplicação precisa que o Anki esteja a ser executado para funcionar.
2.  **Execute o Gerador:** Na pasta `dist/VocabularyGenerator`, clique duas vezes no ficheiro `VocabularyGenerator.exe`.
3.  **Use a Interface:**
    - **Escolha o idioma** e o **baralho** de destino. Pode criar um novo baralho diretamente na interface.
    - **Selecione o nível** de complexidade da frase a ser gerada.
    - **Insira as palavras** que quer aprender, separadas por espaço ou vírgula.
    - (Opcional) Em `Configurações Adicionais`, pode escolher a cor de destaque.
    - **Clique em "Gerar Cartas Anki"** e aguarde o processamento. Os resultados aparecerão na interface e os cartões serão adicionados ao seu Anki.

---

## 🔧 Solução de Problemas Comuns

- **Erro "Não foi possível conectar ao Anki":**
  - Verifique se o Anki está aberto.
  - Verifique se o add-on AnkiConnect foi instalado corretamente.

- **Erro de API do Groq ou DeepL:**
  - Verifique se o ficheiro `.env` foi criado corretamente na pasta raiz do projeto.
  - Confirme que as suas chaves de API foram copiadas e coladas corretamente dentro do ficheiro `.env`.

- **A aplicação fecha logo após abrir:**
  - Execute o `install_dependencies.bat` novamente para garantir que todas as bibliotecas estão instaladas. Se o erro persistir, pode haver um problema mais profundo com a instalação do Python.
