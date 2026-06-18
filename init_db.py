"""
Run once to pre-create the database:
    python init_db.py

The app also calls initialize_database() on startup automatically,
so this file is optional but useful for first-time setup.
"""
from utils.db_manager import initialize_database

if __name__ == "__main__":
    initialize_database()
    print("✅ Database initialized — eduai_valut.db is ready.")
