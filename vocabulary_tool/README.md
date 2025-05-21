🧠 Gerador de Vocabulário - Instalação e Uso

📁 Conteúdo:
- Gerador de Vocabulario.exe
- Pasta /data (vocabulário)
- .env (chave da API do DeepL)

📌 Requisitos obrigatórios:
1. Anki instalado + add-on AnkiConnect (código: 2055492159)
2. Ollama instalado e rodando:
   - Instale: https://ollama.com
   - Rode o modelo: ollama run mistral
3. Conexão com a internet
4. Chave válida da API DeepL (cadastre-se em https://www.deepl.com/pro#developer)
   - Insira a chave no arquivo `.env`:
     DEEPL_API_KEY=sua_chave_aqui

▶️ Como usar:
1. Dê duplo clique no executável `Gerador de Vocabulario.exe`
2. Digite uma nova palavra
3. A ferramenta irá:
   - Gerar uma frase contextualizada com a palavra
   - Traduzir a frase automaticamente
   - Enviar o conteúdo para seu Anki

📂 Local de execução:
- O programa salva seu vocabulário em: data/vocab.db

❗ Importante:
- O Anki deve estar **aberto** durante o uso.
- O Ollama deve estar **rodando localmente**.

🛠 Suporte:
Esta ferramenta foi construída para uso local. Caso precise de ajuda, envie seu feedback para o criador.
