# 🧠 Gerador de Vocabulário

Uma ferramenta inteligente para aprender idiomas por meio de frases contextualizadas, tradução automática e integração direta com o Anki.

---

## 📦 Funcionalidades

✅ Geração de frases com base em modelos de IA (Ollama + Mistral)  
✅ Tradução automática usando a API do DeepL  
✅ Armazenamento local do vocabulário (SQLite)  
✅ Envio direto de cards para o Anki via AnkiConnect  
✅ Interface simples em navegador (Streamlit)

---

## 🚀 Como usar

### 1. Pré-requisitos

| Requisito        | Instalar                                           |
|------------------|----------------------------------------------------|
| **Python 3.9+**   | [https://www.python.org](https://www.python.org)   |
| **Ollama**       | [https://ollama.com](https://ollama.com)           |
| **Modelo Mistral** | No terminal: `ollama run mistral`                 |
| **Anki**         | [https://apps.ankiweb.net/](https://apps.ankiweb.net/) |
| **AnkiConnect**  | No Anki: `Tools > Add-ons > Get Add-ons` → código `2055492159` |
| **DeepL API Key**| [https://www.deepl.com/pro#developer](https://www.deepl.com/pro#developer) |

---

### 2. Configurar sua chave da DeepL

Crie um arquivo chamado `.env` na raiz do projeto com o seguinte conteúdo:

```
DEEPL_API_KEY=sua_chave_aqui
```

---

### 3. Executar o aplicativo (via terminal)

Caso esteja usando o código fonte:

```bash
streamlit run app.py
```

---

### 4. Empacotar para distribuição (.exe / .app)

Use o PyInstaller com o arquivo `.spec` incluso:

```bash
pyinstaller gerador_vocabulario.spec
```

O executável será gerado em:

```
dist/Gerador de Vocabulario/
```

---

## 📁 Estrutura do Projeto

```
vocabulary_tool/
├── app.py
├── .env
├── data/
│   └── vocab.db
├── backend/
├── models/
├── utils/
├── build.bat
├── gerador_vocabulario.spec
└── README.md
```

---

## 🧾 Licença

Este projeto é de uso pessoal e educacional. Se quiser distribuir ou adaptar comercialmente, entre em contato com o autor.

---

## 🙋‍♂️ Suporte

Caso tenha dúvidas ou sugestões, entre em contato diretamente com o desenvolvedor ou abra uma issue no repositório.
