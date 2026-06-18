import sqlite3
import hashlib
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
DB_PATH = os.path.join(project_root, "eduai_valut.db")


def connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    """Create tables if they don't exist — called at startup."""
    conn = connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            Upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            processed_text TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS response_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text_hash TEXT NOT NULL,
            request_type TEXT NOT NULL,
            cached_response TEXT NOT NULL,
            UNIQUE(text_hash, request_type)
        )
    ''')
    conn.commit()
    conn.close()


def save_documnet_to_db(filename, raw_text):
    """Save a document to the database (no-op if already present)."""
    conn = connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM documents WHERE filename=?", (filename,))
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(
                "INSERT INTO documents (filename, processed_text) VALUES (?, ?)",
                (filename, raw_text)
            )
            conn.commit()
            print(f"Document '{filename}' saved to database.")
        else:
            print(f"Document '{filename}' already exists in the database.")
    except Exception as e:
        print(f"Error saving document to database: {e}")
    finally:
        conn.close()   # only closed once, inside finally


def get_all_document():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, filename, Upload_date, processed_text FROM documents ORDER BY Upload_date DESC"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def generate_text_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def check_cache(text_hash, request_type):
    conn = connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT cached_response FROM response_cache WHERE text_hash=? AND request_type=?",
            (text_hash, request_type)
        )
        result = cursor.fetchone()
        return result["cached_response"] if result else None
    except Exception as e:
        print(f"Error checking cache: {e}")
        return None
    finally:
        conn.close()


def save_to_cache(text_hash, request_type, cached_response):
    conn = connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT OR REPLACE INTO response_cache (text_hash, request_type, cached_response) VALUES (?, ?, ?)",
            (text_hash, request_type, cached_response)
        )
        conn.commit()
        print("Response cached cleanly.")
    except Exception as e:
        print(f"Error saving to cache: {e}")
    finally:
        conn.close()


def get_user_data():
    """Return list of documents with their cached summary (if available)."""
    documents = get_all_document()
    library_items = []
    conn = connection()
    cursor = conn.cursor()
    try:
        for doc in documents:
            text_hash = generate_text_hash(doc["processed_text"])
            cursor.execute(
                "SELECT cached_response FROM response_cache WHERE text_hash=? AND request_type='summary'",
                (text_hash,)
            )
            cache_row = cursor.fetchone()
            # ── FIX: don't crash when summary hasn't been generated yet ──
            summary = cache_row["cached_response"] if cache_row else "Summary not generated yet. Open the PDF and click 'Generate Summary'."
            library_items.append({
                "id": doc["id"],
                "filename": doc["filename"],
                "Upload_date": doc["Upload_date"],   # consistent key name
                "summary": summary,
                "processed_text": doc["processed_text"],
            })
    except Exception as e:
        print(f"Error fetching user data: {e}")
    finally:
        conn.close()
    return library_items
