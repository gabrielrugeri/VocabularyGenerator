import streamlit as st

# Title
st.title("Vocabulary Builder")

# Language and level selection
language = st.selectbox("Select language", ["en", "es", "fr"])
level = st.selectbox("Select level", ["beginner", "intermediate", "advanced"])

# Word input
new_word = st.text_input("Enter a new word you want to learn")

# Placeholder for a generated sentence (simulate for now)
if st.button("Generate sentence"):
    st.write(f"Example sentence with **{new_word}** (language: {language}, level: {level})")

# Placeholder for history
st.subheader("Your sentence history (coming soon...)")