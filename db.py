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

    # Create other tables as needed (e.g., polls, options, votes)

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

