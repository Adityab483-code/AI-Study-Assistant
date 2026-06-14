import sqlite3

def initialize_database():
    conn =sqlite3.connect("eduai_valut.db")
    cursor=conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        Upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        processed_text TEXT NOT NULL
    )''')       
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS response_cache(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   text_hash TEXT UNIQUE NOT NULL,
                   request_type TEXT NOT NULL, -- 'summary' or 'quiz'
                   cached_response TEXT NOT NULL)
                   ''')
    conn.commit()
    conn.close()
    print("database initialized! , eduai_valut.db is ready.")
if __name__ == "__main__":
    initialize_database()                              