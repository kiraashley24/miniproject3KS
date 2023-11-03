import sqlite3

DATABASE = 'polls.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def create_tables():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Add other table creation statements here if needed (e.g., polls, options, votes)

    conn.commit()
    conn.close()

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Initialize the database with the schema
    cursor.executescript('''
        -- Add your schema here
    ''')

    conn.commit()
    conn.close()

def add_user(username, password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user
