import sqlite3
import os

# Define database path relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "vocab.db")

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vocabulary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL UNIQUE,
            sentence TEXT,
            translation TEXT,
            language TEXT DEFAULT 'english',
            level TEXT DEFAULT 'beginner'
        )
    """)

    conn.commit()
    conn.close()

def add_word(word, sentence, translation, language="english", level="beginner"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO vocabulary (word, sentence, translation, language, level)
            VALUES (?, ?, ?, ?, ?)
        """, (word, sentence, translation, language, level))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"'{word}' already exists in database.")
    finally:
        conn.close()
        
def get_known_words(language="english"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT word FROM vocabulary WHERE language = ?
    """, (language,))
    rows = cursor.fetchall()

    conn.close()
    return [row[0] for row in rows]

