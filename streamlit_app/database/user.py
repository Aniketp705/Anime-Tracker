import os
import sqlite3
from datetime import datetime # Import datetime for current timestamp

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

# New table for unique anime details
def create_anime_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS anime (
            anime_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            total_episodes INTEGER,
            year TEXT,
            rating REAL
        )
    ''')
    conn.commit()

# New table for unique genre names
def create_genres_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS genres (
            genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
            genre_name TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()

# New junction table for many-to-many relationship between anime and genres
def create_anime_genres_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS anime_genres (
            anime_id INTEGER NOT NULL,
            genre_id INTEGER NOT NULL,
            PRIMARY KEY (anime_id, genre_id),
            FOREIGN KEY (anime_id) REFERENCES anime (anime_id) ON DELETE CASCADE,
            FOREIGN KEY (genre_id) REFERENCES genres (genre_id) ON DELETE CASCADE
        )
    ''')
    conn.commit()

# Modified user_anime table to link to anime_id
def create_user_anime_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_anime (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            anime_id INTEGER NOT NULL,
            episodes_watched INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE,
            FOREIGN KEY (anime_id) REFERENCES anime (anime_id) ON DELETE CASCADE,
            UNIQUE (username, anime_id) -- Ensure a user can only add an anime once
        )
    ''')
    conn.commit()

# Helper function to get anime_id by title, inserting if not exists
def _get_or_create_anime_id(title, total_eps, year, rating):
    cursor.execute("SELECT anime_id FROM anime WHERE title = ?", (title,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute('''
            INSERT INTO anime (title, total_episodes, year, rating)
            VALUES (?, ?, ?, ?)
        ''', (title, total_eps, year, rating))
        conn.commit()
        return cursor.lastrowid

# Helper function to get genre_id by name, inserting if not exists
def _get_or_create_genre_id(genre_name):
    cursor.execute("SELECT genre_id FROM genres WHERE genre_name = ?", (genre_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute("INSERT INTO genres (genre_name) VALUES (?)", (genre_name,))
        conn.commit()
        return cursor.lastrowid

# Helper function to link anime and genre
def _link_anime_genre(anime_id, genre_id):
    try:
        cursor.execute('''
            INSERT INTO anime_genres (anime_id, genre_id)
            VALUES (?, ?)
        ''', (anime_id, genre_id))
        conn.commit()
    except sqlite3.IntegrityError:
        # This means the link already exists (anime_id, genre_id) is a PRIMARY KEY
        pass # Do nothing if already linked


#get the user id from the username
def get_user_id(username):
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    return result[0] if result else None


#add user to the database
def add_user(username, email, password):
    try:
        default_profile = "streamlit_app/database/blankprofile.png"
        with open(default_profile, 'rb') as f:
            default_pic = f.read()
        cursor.execute('''
            INSERT INTO users (username, email, password, profile) VALUES (?, ?, ?, ?)
        ''', (username, email, password, default_pic))
        conn.commit()
        return True, "User registered successfully!"
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed: users.username" in str(e):
            return False, "Username already exists. Please choose a different one."
        elif "UNIQUE constraint failed: users.email" in str(e):
            return False, "Email already registered. Please use a different email."
        return False, f"Database error: {str(e)}"
    except Exception as e:
        return False, f"An unexpected error occurred: {str(e)}"



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


#add anime to the user (Modified for normalization)
def add_anime(username, title, episodes_watched, status, genre, total_eps, year, rating):
    try:
        # Get or create anime entry in the 'anime' table
        anime_id = _get_or_create_anime_id(title, total_eps, year, rating)

        # Prevent duplicates in user_anime (unique constraint handles this, but explicit check for better message)
        cursor.execute('''
            SELECT id FROM user_anime
            WHERE username = ? AND anime_id = ?
        ''', (username, anime_id))
        if cursor.fetchone():
            return False, "Anime already exists in your list."

        # Process genres and link them
        if genre and genre != "N/A":
            genre_list = [g.strip() for g in genre.split(",") if g.strip()]
            for g_name in genre_list:
                genre_id = _get_or_create_genre_id(g_name)
                _link_anime_genre(anime_id, genre_id)

        # Insert into user_anime table
        cursor.execute('''
            INSERT INTO user_anime (username, anime_id, episodes_watched, status)
            VALUES (?, ?, ?, ?)
        ''', (username, anime_id, episodes_watched, status))
        conn.commit()
        return True, "Anime added successfully!"

    except Exception as e:
        return False, f"Error: {str(e)}"

#get all the anime of the user (Modified for normalization)
def get_all_anime(username):
    cursor.execute('''
        SELECT
            a.title,
            ua.episodes_watched,
            GROUP_CONCAT(g.genre_name, ', '), -- Reconstruct genre string
            ua.added_at
        FROM user_anime ua
        JOIN anime a ON ua.anime_id = a.anime_id
        LEFT JOIN anime_genres ag ON a.anime_id = ag.anime_id
        LEFT JOIN genres g ON ag.genre_id = g.genre_id
        WHERE ua.username = ?
        GROUP BY ua.id -- Group by user_anime.id to get distinct rows
        ORDER BY ua.added_at DESC
    ''', (username,))
    anime = cursor.fetchall()
    return anime

#get all the watched anime of the user (Modified for normalization)
def get_watched_anime(username):
    cursor.execute('''
        SELECT
            ua.id,
            ua.username,
            a.title,
            ua.episodes_watched,
            ua.status,
            GROUP_CONCAT(g.genre_name, ', '), -- Reconstruct genre string
            a.total_episodes,
            a.year,
            a.rating,
            ua.added_at
        FROM user_anime ua
        JOIN anime a ON ua.anime_id = a.anime_id
        LEFT JOIN anime_genres ag ON a.anime_id = ag.anime_id
        LEFT JOIN genres g ON ag.genre_id = g.genre_id
        WHERE ua.username = ? AND ua.status = 'Completed'
        GROUP BY ua.id
        ORDER BY ua.added_at DESC
    ''', (username,))
    anime = cursor.fetchall()
    return anime

#get all the planned anime of the user (Modified for normalization)
def get_planned_anime(username):
    cursor.execute('''
        SELECT
            ua.id,
            ua.username,
            a.title,
            ua.episodes_watched,
            ua.status,
            GROUP_CONCAT(g.genre_name, ', '),
            a.total_episodes,
            a.year,
            a.rating,
            ua.added_at
        FROM user_anime ua
        JOIN anime a ON ua.anime_id = a.anime_id
        LEFT JOIN anime_genres ag ON a.anime_id = ag.anime_id
        LEFT JOIN genres g ON ag.genre_id = g.genre_id
        WHERE ua.username = ? AND ua.status = 'Plan to Watch'
        GROUP BY ua.id
        ORDER BY ua.added_at DESC
    ''', (username,))
    anime = cursor.fetchall()
    return anime

#get all the watching anime of the user (Modified for normalization)
def get_watching_anime(username):
    cursor.execute('''
        SELECT
            ua.id,
            ua.username,
            a.title,
            ua.episodes_watched,
            ua.status,
            GROUP_CONCAT(g.genre_name, ', '),
            a.total_episodes,
            a.year,
            a.rating,
            ua.added_at
        FROM user_anime ua
        JOIN anime a ON ua.anime_id = a.anime_id
        LEFT JOIN anime_genres ag ON a.anime_id = ag.anime_id
        LEFT JOIN genres g ON ag.genre_id = g.genre_id
        WHERE ua.username = ? AND ua.status = 'Watching'
        GROUP BY ua.id
        ORDER BY ua.added_at DESC
    ''', (username,))
    anime = cursor.fetchall()
    return anime

# ... (other database functions like create_table, add_user, find_user, etc.)

# Update watched anime (Modified for normalization)
def update_watched_anime(username, anime_title, episodes_watched, status):
    try:
        # Get anime_id from anime_title
        cursor.execute("SELECT anime_id FROM anime WHERE title = ?", (anime_title,))
        anime_id_result = cursor.fetchone()
        if not anime_id_result:
            return False, f"Anime '{anime_title}' not found in database."
        anime_id = anime_id_result[0]

        cursor.execute('''
            UPDATE user_anime
            SET episodes_watched = ?, status = ?
            WHERE username = ? AND anime_id = ?
        ''', (episodes_watched, status, username, anime_id))
        conn.commit()
        return True, "Update successful."
    except Exception as e:
        print(f"Database error updating anime progress for user {username}, anime {anime_title}: {e}")
        return False, f"An error occurred during the update: {e}"

#delete the anime from the db (Modified for normalization)
def delete_user_anime(username, anime_title):
    try:
        # Get anime_id from anime_title
        cursor.execute("SELECT anime_id FROM anime WHERE title = ?", (anime_title,))
        anime_id_result = cursor.fetchone()
        if not anime_id_result:
            return False, f"Anime '{anime_title}' not found in database."
        anime_id = anime_id_result[0]

        cursor.execute('''
            DELETE FROM user_anime
            WHERE username = ? AND anime_id = ?
        ''', (username, anime_id))
        conn.commit()
        return True, "Anime deleted successfully."
    except Exception as e:
        print(f"Database error deleting anime for user {username}, anime {anime_title}: {e}")
        return False, f"An error occurred during deletion: {e}"

#remove all the anime of an user
def delete_all_anime(username):
    cursor.execute('''
        DELETE FROM user_anime WHERE username = ?
    ''', (username,))
    conn.commit()


# Initial table creations (Order matters due to foreign keys)
# create_table() 
# create_anime_table() 
# create_genres_table() 
# create_anime_genres_table() 
# create_user_anime_table() 
# conn.commit()