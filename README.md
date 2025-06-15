# 🚀 Gerador de Vocabulário para Anki (Vocabulary Generator)

Bem-vindo! Esta é uma ferramenta para criar cartões de estudo (flashcards) para o Anki de forma automática.  
Ela usa Inteligência Artificial para gerar frases, traduções, áudio e a pronúncia das palavras que você quer aprender.

---

## ✨ O Que a Aplicação Faz?

### ✅ Cria Cartões Completos
Para cada palavra que você insere, a aplicação cria um cartão no Anki com:
- Uma frase de exemplo
- A transcrição fonética (como se pronuncia)
- A tradução da frase
- O áudio da frase no idioma original

### ✅ Poupa o seu Tempo
Automatiza todo o processo de criação de cartões, permitindo que você se foque em estudar.

### ✅ Fácil de Usar
É uma aplicação de um único arquivo, sem necessidade de instalação complicada.

---

## 📋 Antes de Começar (Pré-requisitos)

Para que a aplicação funcione, precisa de 3 coisas:

### 1. Anki Instalado
O programa de flashcards. Se não o tiver, faça download em [apps.ankiweb.net](https://apps.ankiweb.net)

### 2. Add-on AnkiConnect
Uma pequena extensão que permite que esta aplicação comunique com o seu Anki.

No Anki:
- Vá a **Ferramentas > Complementos > Obter complementos...**
- Cole o seguinte código: `2055492159`
- Feche e abra o Anki novamente

### 3. Chaves de API (Gratuitas)
São como "senhas" que dão à aplicação acesso aos serviços de IA e tradução. A aplicação pedirá estas chaves na primeira vez que a executar.

- **Chave do DeepL**: Crie uma conta gratuita em [DeepL API](https://www.deepl.com/pro#developer) para obter a sua chave.
- **Chave do Groq**: Crie uma conta gratuita em [Groq](https://console.groq.com) para obter a sua chave.

---

## ▶️ Como Usar a Aplicação

### 1. Execute o Ficheiro
Clique duas vezes no arquivo `VocabularyGenerator.exe`.

### 2. Configuração Inicial (Apenas na primeira vez)
- A aplicação irá pedir as suas chaves de API do DeepL e do Groq.
- Cole cada chave no seu campo correspondente e clique em **"Guardar e Iniciar"**.
- A aplicação irá reiniciar e não pedirá as chaves novamente.

### 3. Uso Diário
- Abra o Anki. Ele precisa de estar a ser executado para que a mágica aconteça.
- No Gerador de Vocabulário:
  - Escolha o idioma e o baralho para onde os cartões serão enviados
  - Insira as palavras que quer aprender (pode ser uma ou várias, separadas por espaço)
  - Clique no botão **"Gerar Cartas Anki"**
- Aguarde um momento. Os cartões aparecerão no seu Anki, prontos para estudar!

---

## 🔧 Ajuda e Solução de Problemas

### ❌ "Erro: Não foi possível conectar ao Anki"
**Solução**: Verifique se o Anki está aberto no seu computador.  
Se estiver, reinicie o Anki e tente novamente.

---

### ❌ "Erro de API do Groq / DeepL"
**Solução**: É provável que uma das chaves de API esteja incorreta.  
Para as inserir novamente, terá de apagar o arquivo de configuração:

1. Pressione `Win + R`, digite `%appdata%` e pressione Enter  
2. Encontre e apague a pasta `VocabularyGenerator`  
3. Execute a aplicação novamente. Ela pedirá as chaves de novo

---

### ❌ A Aplicação Não Abre?
**Solução**:  
Tente executar o arquivo `VocabularyGenerator.exe` como Administrador:  
Clique com o botão direito → **Executar como administrador**, pelo menos na primeira vez.
