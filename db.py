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
               user_id INTEGER, -- Reference to the user who voted
               poll_id INTEGER, -- Reference to the poll
               option_id INTEGER -- Reference to the selected option
           )
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

# Add a new poll to the database
def add_poll(question):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO polls (question) VALUES (?)", (question,))
    poll_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return poll_id

# Get all polls from the database
def get_all_polls():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, question FROM polls")
    polls = cursor.fetchall()
    conn.close()
    return polls

# Add an option to a poll
def add_option_to_poll(poll_id, option_text):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO poll_options (poll_id, option_text) VALUES (?, ?)", (poll_id, option_text))
    conn.commit()
    conn.close()

# Get options for a specific poll
def get_poll_options(poll_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, option_text FROM poll_options WHERE poll_id=?", (poll_id,))
    options = cursor.fetchall()
    conn.close()
    return options

def get_vote_count(option_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM votes WHERE option_id = ?", (option_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def record_vote(user_id, poll_id, option_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO votes (user_id, poll_id, option_id) VALUES (?, ?, ?)", (user_id, poll_id, option_id))
    conn.commit()
    conn.close()

def has_user_voted(user_id, poll_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM votes WHERE user_id = ? AND poll_id = ?", (user_id, poll_id))
    result = cursor.fetchone() is not None
    conn.close()
    return result

def get_vote_counts(poll_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT option_text, COUNT(votes.id) FROM poll_options LEFT JOIN votes ON poll_options.id = votes.option_id WHERE poll_options.poll_id = ? GROUP BY poll_options.id", (poll_id,))
    vote_counts = cursor.fetchall()
    conn.close()
    return vote_counts



