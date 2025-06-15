import sys
import os
import streamlit as st

# --- CORREÇÃO FINAL PARA EMPACOTAMENTO ---
# Este bloco determina a pasta raiz do projeto e a adiciona ao caminho do Python.
if getattr(sys, 'frozen', False):
    project_root = sys._MEIPASS
else:
    project_root = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, project_root)

# A CONFIGURAÇÃO DA PÁGINA DEVE SER O PRIMEIRO COMANDO STREAMLIT
st.set_page_config(page_title="Gerador Anki", layout="centered")

# Agora podemos importar os nossos módulos com segurança
from backend.logic import process_new_word, LogicError
import backend.database as db
from backend.level import Difficulty

# --- O resto do seu código permanece exatamente o mesmo ---

# Inicializa o banco de dados
db.init_db()

# Inicializa o session_state
if 'words_input' not in st.session_state:
    st.session_state.words_input = ""

# Título da Aplicação
st.title("🚀 Gerador de Cartas Anki")
st.caption("O Anki deve estar aberto no computador para que a exportação funcione.")

# --- Seleção de Idioma e Baralho ---
st.subheader("1. Selecione o Idioma e o Baralho")

languages = db.get_languages()
if not languages:
    st.error("Nenhum idioma encontrado na base de dados. Verifique a função seed_languages.")
    st.stop()

language_labels = [f"{lang[3]} ({lang[0]})" for lang in languages]
language_codes = [lang[0] for lang in languages]

selected_language = st.selectbox(
    "Escolha o idioma",
    options=language_codes,
    format_func=lambda code: dict(zip(language_codes, language_labels)).get(code, code)
)

decks = db.get_decks_by_language(selected_language)
deck_options = {deck[0]: deck[1] for deck in decks}

selected_deck_id = st.selectbox(
    "Escolha um baralho existente",
    options=list(deck_options.keys()),
    format_func=lambda id: deck_options.get(id, "N/A"),
    help="Selecione o baralho Anki para onde as cartas serão enviadas."
)

with st.expander("➕ Criar um novo baralho"):
    with st.form("new_deck_form", clear_on_submit=True):
        new_deck_name = st.text_input("Nome do novo baralho")
        submitted = st.form_submit_button("Criar e Adicionar")
        if submitted and new_deck_name.strip():
            try:
                db.add_deck(new_deck_name.strip(), selected_language)
                st.success(f"Baralho '{new_deck_name}' adicionado! A lista será atualizada.")
            except Exception as e:
                st.error(f"Não foi possível criar o baralho: {e}")

# Seleção de Nível e Input de Palavras
st.subheader("2. Insira as Palavras")

known_words = db.get_known_words(selected_language)
st.info(f"Você já conhece **{len(known_words)}** palavras neste idioma.")

level = Difficulty.get_level_number(
    st.selectbox("Selecione o nível de complexidade das frases",
                 options=["iniciante", "intermediário", "avançado"],
                 help="Isto define a complexidade da frase de exemplo gerada.")
)

words_to_process_input = st.text_area(
    "Insira as palavras que você quer aprender (separadas por espaço ou vírgula)",
    key="words_input",
    help="Pode colar várias palavras de uma vez."
)

# --- Configurações Adicionais ---
with st.expander("⚙️ Configurações Adicionais"):
    highlight_color = st.color_picker("Cor de destaque da palavra", "#007aff")


# Botão de Ação e Processamento
if st.button("✨ Gerar Cartas Anki", type="primary", use_container_width=True):
    words = [word for word in words_to_process_input.strip().lower().replace(",", " ").split() if word]

    if not words:
        st.warning("Por favor, insira pelo menos uma palavra.")
    elif not selected_deck_id:
        st.error("Por favor, selecione ou crie um baralho antes de gerar as cartas.")
    else:
        progress_bar = st.progress(0, "A iniciar...")
        total_words = len(words)
        
        for i, word in enumerate(words):
            progress_text = f"Processando: **{word}** ({i + 1}/{total_words})"
            progress_bar.progress((i + 1) / total_words, text=progress_text)
            
            with st.container():
                st.markdown(f"---")
                
                if word in known_words:
                    st.warning(f"A palavra '{word}' já foi adicionada anteriormente. A ignorar.", icon="⚠️")
                    continue

                try:
                    # Chama a lógica de negócio passando a cor selecionada
                    sentence, translation, anki_result = process_new_word(
                        word, known_words, level, selected_deck_id, selected_language,
                        highlight_color=highlight_color
                    )
                    
                    st.success(f"**Frase:** {sentence}", icon="🚀")
                    st.info(f"**Tradução:** {translation}", icon="📖")
                    st.success(f"**Anki:** {anki_result}", icon="🧠")
                    
                    known_words.add(word)

                except LogicError as e:
                    st.error(f"Ocorreu um erro ao processar '{word}': {e}", icon="❌")
        
        progress_bar.empty()
        st.balloons()
        st.success("Processamento concluído!")
