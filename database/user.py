import os
import sqlite3

# Get the absolute path to the db folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "user.db")

# Connect using the full path
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()

def create_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()



def add_user(username, email, password):
    cursor.execute('''
        INSERT INTO users (username, email, password) VALUES (?, ?, ?)
    ''', (username, email, password))
    conn.commit()

def find_user(username):
    cursor.execute('''
        SELECT * FROM users WHERE username = ?
    ''', (username,))
    user = cursor.fetchone()
    return user

def find_email(email):
    cursor.execute('''
        SELECT * FROM users WHERE email = ?
    ''', (email,))
    user = cursor.fetchone()
    return user

def get_user():
    cursor.execute('''SELECT * FROM users''')
    users = cursor.fetchall()
    return users

def delete_user(username):
    cursor.execute('''
        DELETE FROM users WHERE username = ?
    ''', (username,))
    conn.commit()
