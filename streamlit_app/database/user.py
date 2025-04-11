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
            password TEXT NOT NULL,
            profile BLOB DEFAULT NULL
        )
    ''')
    conn.commit()


#create a table for watched anime
def create_watched_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_anime (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            anime_title TEXT NOT NULL,
            episodes_watched INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()


#add user to the database
def add_user(username, email, password):
    #add default profile pic
    default_profile = "database/blankprofile.png"
    with open(default_profile, 'rb') as f:
        default_pic = f.read()
    cursor.execute('''
        INSERT INTO users (username, email, password, profile) VALUES (?, ?, ?, ?)
    ''', (username, email, password, default_pic))
    conn.commit()


#find the user
def find_user(username):
    cursor.execute('''
        SELECT * FROM users WHERE username = ?
    ''', (username,))
    user = cursor.fetchone()
    return user

#find the user by email
def find_email(email):
    cursor.execute('''
        SELECT * FROM users WHERE email = ?
    ''', (email,))
    user = cursor.fetchone()
    return user

#get all the users as list
def get_user():
    cursor.execute('''SELECT * FROM users''')
    users = cursor.fetchall()
    return users

#change password of the user
def update_password(username, new_pass):
    cursor.execute('''
        UPDATE users SET password = ? WHERE username = ?
    ''', (new_pass, username))
    conn.commit()

#update the email of the user
def update_email(username, new_email):
    cursor.execute('''
        UPDATE users SET email = ? WHERE username = ?
    ''', (new_email, username))
    conn.commit()

def add_profile_pic(username, profile_pic):
    cursor.execute('''
        UPDATE users SET profile = ? WHERE username = ?
    ''', (profile_pic, username))
    conn.commit()


#remove the user from the database
def delete_user(username):
    cursor.execute('''
        DELETE FROM users WHERE username = ?
    ''', (username,))
    conn.commit()


#add anime to the user
def add_anime(username, anime_title, episodes_watched, status):
    try:

        # Check for duplicate entry
        cursor.execute('''
            SELECT * FROM user_anime
            WHERE username = ? AND anime_title = ?
        ''', (username, anime_title))
        existing = cursor.fetchone()

        if existing:
            return False, "You've already added this anime."

        # Insert if not a duplicate
        cursor.execute('''
            INSERT INTO user_anime (username, anime_title, episodes_watched, status)
            VALUES (?, ?, ?, ?)
        ''', (username, anime_title, episodes_watched, status))
        conn.commit()
        return True, "Anime added successfully!"

    except Exception as e:
        return False, f"Error: {str(e)}"


cursor.execute('''DELETE FROM user_anime WHERE id == 2''')
conn.commit()