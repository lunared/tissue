import sqlite3

DATABASE = '../tissue.db'

def connect_to_database():
    return sqlite3.connect(DATABASE)

def get_db():
    db = connect_to_database()
    db.row_factory = sqlite3.Row
    return db
