import sys
import os
import streamlit as st

# --- Configuração de Caminhos para o PyInstaller ---
if getattr(sys, 'frozen', False):
    project_root = sys._MEIPASS
else:
    project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# --- Importação de Módulos ---
from utils import config_manager

def setup_screen():
    """Mostra o ecrã de configuração inicial para as chaves de API."""
    st.set_page_config(page_title="Configuração - Gerador Anki", layout="centered")
    st.title("⚙️ Configuração Inicial")
    st.warning("Para usar a aplicação pela primeira vez, precisa de fornecer as suas chaves de API.")
    st.info("Estas chaves serão guardadas localmente no seu computador e não serão partilhadas.")

    with st.form("api_key_form"):
        st.markdown("### 1. Chave da API do Groq")
        groq_key = st.text_input("Cole a sua chave da API do Groq aqui", type="password", help="Obtenha em https://console.groq.com/")
        st.markdown("### 2. Chave da API do DeepL")
        deepl_key = st.text_input("Cole a sua chave da API do DeepL aqui", type="password", help="Obtenha em https://www.deepl.com/pro-api")
        submitted = st.form_submit_button("Guardar e Iniciar")

        if submitted:
            if not groq_key or not deepl_key:
                st.error("Por favor, preencha ambas as chaves de API.")
            else:
                try:
                    config_manager.save_api_keys(groq_key, deepl_key)
                    st.success("Chaves guardadas com sucesso! A aplicação irá reiniciar...")
                    st.balloons()
                    st.rerun()
                except Exception as e:
                    st.error(f"Não foi possível guardar as chaves: {e}")

def main_app():
    """Mostra a interface principal da aplicação."""
    st.set_page_config(page_title="Gerador Anki", layout="centered")
    
    from backend.logic import process_new_word, LogicError
    import backend.database as db
    from backend.level import Difficulty

    db.init_db()

    if 'words_input' not in st.session_state:
        st.session_state.words_input = ""

    st.title("🚀 Gerador de Cartas Anki")
    st.caption("O Anki deve estar aberto no computador para que a exportação funcione.")
    
    st.subheader("1. Selecione o Idioma e o Baralho")
    languages = db.get_languages()
    if not languages:
        st.error("Nenhum idioma encontrado na base de dados.")
        st.stop()
    language_labels = [f"{lang[3]} ({lang[0]})" for lang in languages]
    language_codes = [lang[0] for lang in languages]
    selected_language = st.selectbox("Escolha o idioma", options=language_codes, format_func=lambda code: dict(zip(language_codes, language_labels)).get(code, code))
    
    decks = db.get_decks_by_language(selected_language)
    deck_options = {deck[0]: deck[1] for deck in decks}
    selected_deck_id = st.selectbox("Escolha um baralho existente", options=list(deck_options.keys()), format_func=lambda id: deck_options.get(id, "N/A"))

    with st.expander("➕ Criar um novo baralho"):
        with st.form("new_deck_form", clear_on_submit=True):
            new_deck_name = st.text_input("Nome do novo baralho")
            if st.form_submit_button("Criar e Adicionar") and new_deck_name.strip():
                try:
                    db.add_deck(new_deck_name.strip(), selected_language)
                    st.success(f"Baralho '{new_deck_name}' adicionado!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Não foi possível criar o baralho: {e}")

    st.subheader("2. Insira as Palavras")
    known_words = db.get_known_words(selected_language)
    st.info(f"Você já conhece **{len(known_words)}** palavras neste idioma.")
    level = Difficulty.get_level_number(st.selectbox("Selecione o nível de complexidade das frases", options=["iniciante", "intermediário", "avançado"]))
    words_to_process_input = st.text_area("Insira as palavras (separadas por espaço ou vírgula)", key="words_input")
    
    with st.expander("⚙️ Configurações Adicionais"):
        highlight_color = st.color_picker("Cor de destaque da palavra", "#007aff")

    if st.button("✨ Gerar Cartas Anki", type="primary", use_container_width=True):
        words = [word for word in words_to_process_input.strip().lower().replace(",", " ").split() if word]
        if not words:
            st.warning("Por favor, insira pelo menos uma palavra.")
        elif not selected_deck_id:
            st.error("Por favor, selecione ou crie um baralho antes de gerar as cartas.")
        else:
            progress_bar = st.progress(0, "A iniciar...")
            total_words = len(words)
            errors_found = False # Flag para controlar se ocorreram erros

            for i, word in enumerate(words):
                progress_text = f"Processando: **{word}** ({i + 1}/{total_words})"
                progress_bar.progress((i + 1) / total_words, text=progress_text)
                
                with st.container():
                    st.markdown(f"---")
                    if word in known_words:
                        st.warning(f"A palavra '{word}' já foi adicionada. A ignorar.", icon="⚠️")
                        continue
                    try:
                        sentence, translation, anki_result = process_new_word(word, known_words, level, selected_deck_id, selected_language, highlight_color=highlight_color)
                        st.success(f"**Frase:** {sentence}", icon="📘")
                        st.info(f"**Tradução:** {translation}", icon="📖")
                        st.success(f"**Anki:** {anki_result}", icon="🧠")
                        known_words.add(word)
                    except LogicError as e:
                        st.error(f"Ocorreu um erro ao processar '{word}': {e}", icon="❌")
                        errors_found = True # Marca que um erro ocorreu
            
            progress_bar.empty()
            
            # --- LÓGICA CORRIGIDA ---
            # Só mostra os balões e a mensagem de sucesso total se não houver erros.
            if not errors_found:
                st.balloons()
                st.success("Processamento concluído com sucesso!")
            else:
                st.warning("Processamento concluído, mas com alguns erros. Verifique as mensagens acima.")

if __name__ == "__main__":
    if config_manager.are_keys_configured():
        main_app()
    else:
        setup_screen()
