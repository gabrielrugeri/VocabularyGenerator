import sqlite3
from datetime import datetime
from backend.level import Difficulty
import os

# Define database path relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "vocab.db")

def create_tables() -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS languages (
            code_iso TEXT PRIMARY KEY,
            code_tts TEXT NOT NULL,
            name_en TEXT NOT NULL,
            name_pt TEXT NOT NULL
        )
    """)
    
    seed_languages()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS decks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            language TEXT NOT NULL,
            FOREIGN KEY (language) REFERENCES languages (code_iso)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vocabulary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL UNIQUE,
            language TEXT NOT NULL,
            deck TEXT NOT NULL,
            date TIMESTAMP,
            level INTEGER
        )
    """)

    conn.commit()
    conn.close()

def add_word(word: str, language: str, deck: int, level: int) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO vocabulary (word, language, deck, date, level)
            VALUES (?, ?, ?, ?, ?)
        """, (word, language, deck, datetime.now(), level))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"'{word}' - nível '{Difficulty.get_level(level, 'pt')}' - já existe no banco de dados.")
    finally:
        conn.close()
        
def get_known_words(language: str) -> list[str]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT word FROM vocabulary WHERE language = ?
    """, (language,))
    rows = cursor.fetchall()

    conn.close()
    return [row[0] for row in rows]

def get_languages():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT code_iso, code_tts, name_en, name_pt FROM languages")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_language_by_iso(iso_code: str):
    """
    Busca um idioma pelo código ISO no banco de dados
    
    Args:
        iso_code: Código ISO do idioma (ex: 'pt', 'en')
    Returns:
        Dicionário com os dados do idioma ou None se não encontrado
        Formato: {
            'code_iso': str,
            'code_tts': str,
            'name_en': str,
            'name_pt': str
        }
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row  # Permite acesso por nome de coluna
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT code_iso, code_tts, name_en, name_pt 
                FROM languages 
                WHERE code_iso = ?
            """, (iso_code,))
            
            if result := cursor.fetchone():
                return dict(result)  # Converte Row para dicionário
            return None
            
    except sqlite3.Error as e:
        print(f"Erro ao buscar idioma: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

def get_deck_by_id(id: int):
    """Retorna um deck específico pelo ID"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, name, language 
            FROM decks 
            WHERE id = ?
        """, (id,))
        
        deck = cursor.fetchone()
        
        if deck:
            return {
                "id": deck[0],
                "name": deck[1],
                "language": deck[2]
            }
        return None
        
    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return None
    finally:
        conn.close()

def get_decks_by_language(language_code):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM decks WHERE language = ?", (language_code,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_deck(name: str, language_code: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO decks (name, language)
        VALUES (?, ?)
    """, (name, language_code))
    conn.commit()
    conn.close()

def seed_languages() -> None:
    languages = [
        # (Código ISO, Código TTS, Idioma Inglês, Idioma Português)
        ("en", "en_US", "English", "Inglês"),
        ("es", "es_ES", "Spanish", "Espanhol"),
        ("fr", "fr_FR", "French", "Francês"),
        ("de", "de_DE", "German", "Alemão"),
        ("it", "it_IT", "Italian", "Italiano"),
        ("ja", "ja_JP", "Japanese", "Japonês"),
        ("zh", "zh_CN", "Chinese", "Chinês"),
        ("ru", "ru_RU", "Russian", "Russo"),
        ("ar", "ar_SA", "Arabic", "Árabe"),
        ("ko", "ko_KR", "Korean", "Coreano"),
        ("nl", "nl_NL", "Dutch", "Holandês"),
        ("hi", "hi_IN", "Hindi", "Hindi"),
        ("sv", "sv_SE", "Swedish", "Sueco"),
        ("pl", "pl_PL", "Polish", "Polonês"),
        ("tr", "tr_TR", "Turkish", "Turco"),
        ("el", "el_GR", "Greek", "Grego"),
        ("he", "he_IL", "Hebrew", "Hebraico")
    ]
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for code_iso, code_tts, name_en, name_pt in languages:
        cursor.execute("""
            INSERT OR IGNORE INTO languages (code_iso, code_tts, name_en, name_pt)
            VALUES (?, ?, ?, ?)
        """, (code_iso, code_tts, name_en, name_pt))

    conn.commit()
    conn.close()
