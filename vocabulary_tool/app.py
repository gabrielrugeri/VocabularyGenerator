import streamlit as st
import backend.database as db
from backend.logic import process_new_word

db.create_tables()

# Load known words at the start
known_words = db.get_known_words()

# Title
st.title("Vocabulary Builder")

# Language and level selection
language = st.selectbox("Select language", ["en", "es", "fr"])
level = st.selectbox("Select level", ["beginner", "intermediate", "advanced"])

# Word input
new_word = st.text_input("Enter a new word you want to learn").strip().lower()

if st.button("Generate sentence"):
    sentence, translation, anki_result = process_new_word(new_word, known_words)
    st.write("📘 Example sentence:")
    st.success(sentence)
    st.write("📖 Translation:")
    st.info(translation)
    st.write("🧠 Anki:")
    st.success(anki_result)

# Placeholder for history
st.subheader("Your sentence history (coming soon...)")