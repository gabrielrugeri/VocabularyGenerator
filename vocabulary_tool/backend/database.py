import streamlit as st
import sqlite3
import os
from datetime import datetime
from typing import List, Set, Dict, Any, Optional
from backend.level import Difficulty
from utils.helpers import resource_path

# Define o caminho da base de dados de forma segura
DB_PATH = resource_path(os.path.join("data", "vocab.db"))

# --- Funções de Inicialização e Estrutura ---

@st.cache_resource
def init_db():
    create_tables()

def create_tables() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS languages (
                code_iso TEXT PRIMARY KEY, code_tts TEXT NOT NULL,
                name_en TEXT NOT NULL, name_pt TEXT NOT NULL
            )""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS decks (
                id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
                language_code TEXT NOT NULL,
                FOREIGN KEY (language_code) REFERENCES languages (code_iso) ON DELETE CASCADE
            )""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vocabulary (
                id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT NOT NULL,
                language_code TEXT NOT NULL, deck_id INTEGER NOT NULL,
                date TIMESTAMP, level INTEGER,
                FOREIGN KEY (language_code) REFERENCES languages (code_iso) ON DELETE CASCADE,
                FOREIGN KEY (deck_id) REFERENCES decks (id) ON DELETE CASCADE,
                UNIQUE(word, language_code)
            )""")
        conn.commit()
    seed_languages()

def seed_languages() -> None:
    languages = [
        ("en", "en_US", "English", "Inglês"), ("es", "es_ES", "Spanish", "Espanhol"),
        ("fr", "fr_FR", "French", "Francês"), ("de", "de_DE", "German", "Alemão"),
        ("it", "it_IT", "Italian", "Italiano"), ("ja", "ja_JP", "Japanese", "Japonês"),
        ("pt", "pt_BR", "Portuguese", "Português")
    ]
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.executemany("""
            INSERT OR IGNORE INTO languages (code_iso, code_tts, name_en, name_pt)
            VALUES (?, ?, ?, ?)
        """, languages)
        conn.commit()

# --- Funções de Leitura (com Cache) ---

@st.cache_data
def get_languages() -> List[tuple]:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT code_iso, code_tts, name_en, name_pt FROM languages ORDER BY name_pt")
        return cursor.fetchall()

@st.cache_data
def get_decks_by_language(language_code: str) -> List[tuple]:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM decks WHERE language_code = ?", (language_code,))
        return cursor.fetchall()

@st.cache_data
def get_known_words(language_code: str) -> Set[str]:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT word FROM vocabulary WHERE language_code = ?", (language_code,))
        return {row[0] for row in cursor.fetchall()}

@st.cache_data
def get_language_by_iso(iso_code: str) -> Optional[Dict[str, Any]]:
    """Busca um idioma pelo código ISO. Retorna um dicionário ou None."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row  # Permite acesso por nome de coluna
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM languages WHERE code_iso = ?", (iso_code,))
        if result := cursor.fetchone():
            return dict(result)
        return None

@st.cache_data
def get_deck_by_id(deck_id: int) -> Optional[Dict[str, Any]]:
    """Busca um baralho pelo ID. Retorna um dicionário ou None."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM decks WHERE id = ?", (deck_id,))
        if result := cursor.fetchone():
            return dict(result)
        return None

# --- Funções de Escrita ---

def add_deck(name: str, language_code: str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO decks (name, language_code) VALUES (?, ?)", (name, language_code))
        conn.commit()
    get_decks_by_language.clear()

def add_word(word: str, language_code: str, deck_id: int, level: int) -> None:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO vocabulary (word, language_code, deck_id, date, level)
                VALUES (?, ?, ?, ?, ?)
            """, (word, language_code, deck_id, datetime.now(), level))
            conn.commit()
        get_known_words.clear()
    except sqlite3.IntegrityError:
        print(f"A palavra '{word}' já existe no banco de dados para este idioma.")
