import streamlit as st
import backend.database as db
from backend.logic import process_new_word
from backend.level import Difficulty
import sys
import os

# Garante que o diretório raiz do projeto esteja no sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

db.create_tables()

# Title
st.title("Gerador de Cartas Anki")
st.header("o anki deve estar aberto, no computador, para que o Gerador funcione corretamente")

# Carregar idiomas e baralhos
languages = db.get_languages()
language_labels = [f"{lang[3]} ({lang[0]})" for lang in languages]
language_codes = [lang[0] for lang in languages]

selected_language_index = st.selectbox(
    "Escolha o idioma",
    range(len(language_codes)),
    format_func=lambda i: language_labels[i]
    )
selected_language = language_codes[selected_language_index]

# Listar baralhos existentes para o idioma escolhido
decks = db.get_decks_by_language(selected_language)
deck_codes = [deck[0] for deck in decks]
deck_labels = [deck[1] for deck in decks]
selected_deck = st.selectbox(
    "Escolha um baralho existente",
    range(len(deck_codes)),
    format_func=lambda i: deck_labels[i]
    ) if decks else None
st.write("debug:", selected_deck)

with st.expander("➕ Incluir novo baralho"):
    new_deck_name = st.text_input("Nome do novo baralho")
    if st.button("Incluir baralho") and new_deck_name.strip():
        db.add_deck(new_deck_name.strip(), selected_language)
        st.success(f"Baralho '{new_deck_name}' incluído com sucesso! Recarregue a página para continuar.")

# Load known words at the start
known_words = db.get_known_words(selected_language)

level = Difficulty.get_level_number(
    st.selectbox("Selecione o nível de complexidade das frases geradas",
            ["iniciante", "intermediário", "avançado"]
        )
    )

# Word input
new_words = st.text_input("Insira as palavras que você quer aprender (separadas por espaço)")\
    .strip()\
    .lower()\
    .split(" ")

if st.button("Gerar cartas Anki"):
    for word in new_words:
        # E SE A PALAVRA JÁ TIVER SIDO ADICIONADA?
        sentence, translation, anki_result = process_new_word(word, known_words, level, selected_deck, selected_language)
        st.write("📘 Frase de exemplo")
        st.success(sentence)
        st.write("📖 Tradução:")
        st.info(translation)
        st.write("🧠 Anki:")
        st.success(anki_result)