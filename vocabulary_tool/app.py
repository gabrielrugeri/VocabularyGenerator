import streamlit as st
from main import load_known_words, generate_sentence_with_mistral, save_word_to_vocab
from database import create_tables

create_tables()

# Load known words at the start
known_words = load_known_words()

# Title
st.title("Vocabulary Builder")

# Language and level selection
language = st.selectbox("Select language", ["en", "es", "fr"])
level = st.selectbox("Select level", ["beginner", "intermediate", "advanced"])

# Word input
new_word = st.text_input("Enter a new word you want to learn").strip().lower()

if st.button("Generate sentence"):
    sentence = generate_sentence_with_mistral(new_word, known_words)
    st.write("📘 Example sentence:")
    st.success(sentence)
    save_word_to_vocab(new_word)
    st.write(f"✅ '{new_word}' added to vocab!")


# Placeholder for history
st.subheader("Your sentence history (coming soon...)")