-- schema.sql
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS polls (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    creator_id INTEGER,
    FOREIGN KEY (creator_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS options (
    id INTEGER PRIMARY KEY,
    option_text TEXT NOT NULL,
    poll_id INTEGER,
    FOREIGN KEY (poll_id) REFERENCES polls (id)
);

CREATE TABLE IF NOT EXISTS votes (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    poll_id INTEGER,
    option_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (poll_id) REFERENCES polls (id),
    FOREIGN KEY (option_id) REFERENCES options (id)
);