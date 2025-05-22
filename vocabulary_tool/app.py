import streamlit as st
import backend.database as db
from backend.logic import process_new_word
from backend.level import Difficulty

db.create_tables()

# Load known words at the start
known_words = db.get_known_words()

# Title
st.title("Gerador de Cartas Anki")
st.header("o anki deve estar aberto, no computador, para que o Gerador funcione corretamente")

#inserir nome do baralho onde ele quer adicionar (preferencialmente apenas uma vez)
deck = st.text_input("Insira o baralho onde você quer inserir as cartas")
#inserir idioma que ele quer praticar!

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
        sentence, translation, anki_result = process_new_word(word, known_words, level, deck)
        st.write("📘 Frase de exemplo")
        st.success(sentence)
        st.write("📖 Tradução:")
        st.info(translation)
        st.write("🧠 Anki:")
        st.success(anki_result)