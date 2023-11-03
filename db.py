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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS polls (
            id INTEGER PRIMARY KEY,
            question TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS poll_options (
            id INTEGER PRIMARY KEY,
            poll_id INTEGER,
            option_text TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            poll_id INTEGER,
            option_id INTEGER
        )
    ''')

    conn.commit()
    conn.close()

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Initialize the database with the schema
    cursor.executescript('''
        -- Create the 'polls' table
        CREATE TABLE IF NOT EXISTS polls (
            id INTEGER PRIMARY KEY,
            question TEXT NOT NULL
        );

        -- Create the 'poll_options' table
        CREATE TABLE IF NOT EXISTS poll_options (
            id INTEGER PRIMARY KEY,
            poll_id INTEGER,
            option_text TEXT NOT NULL
        );

        -- Create the 'votes' table
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            poll_id INTEGER,
            option_id INTEGER
        );
    ''')

    conn.commit()
    conn.close()

def add_user(username, password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

# Add poll-related database functions
def get_all_polls():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, question FROM polls")
    polls = cursor.fetchall()
    conn.close()
    return polls
