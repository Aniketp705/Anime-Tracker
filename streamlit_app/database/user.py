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


# Create the user_anime table
def create_watched_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_anime (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            anime_title TEXT NOT NULL,
            episodes_watched INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL,
            genre TEXT,
            total_episodes INTEGER,
            year TEXT,
            rating REAL,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()



#get the user id from the username
def get_user_id(username):
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    return result[0] if result else None




#add user to the database
def add_user(username, email, password):
    #add default profile pic
    default_profile = "streamlit_app/database/blankprofile.png"
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
def add_anime(username, title, episodes_watched, status, genre, total_eps, year, rating):
    try:
        # prevent duplicates
        cursor.execute('''
            SELECT * FROM user_anime
            WHERE username = ? AND anime_title = ?
        ''', (username, title))
        if cursor.fetchone():
            return False, "Anime already exists in your list."

        cursor.execute('''
            INSERT INTO user_anime (username, anime_title, episodes_watched, status, genre, total_episodes, year, rating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, title, episodes_watched, status, genre, total_eps, year, rating))
        conn.commit()
        return True, "Anime added successfully!"

    except Exception as e:
        return False, f"Error: {str(e)}"
    
#get all the anime of the user
def get_all_anime(username):
    cursor.execute('''
        SELECT anime_title,episodes_watched,genre,added_at FROM user_anime WHERE username = ?
    ''', (username,))
    anime = cursor.fetchall()
    return anime

#get all the watched anime of the user
def get_watched_anime(username):
    cursor.execute('''
        SELECT * FROM user_anime WHERE username = ? AND status = 'Completed'
    ''', (username,))
    anime = cursor.fetchall()
    return anime

#get all the planned anime of the user
def get_planned_anime(username):
    cursor.execute('''
        SELECT * FROM user_anime WHERE username = ? AND status = 'Plan to Watch'
    ''', (username,))
    anime = cursor.fetchall()
    return anime

#get all the watching anime of the user
def get_watching_anime(username):
    cursor.execute('''
        SELECT * FROM user_anime WHERE username = ? AND status = 'Watching'
    ''', (username,))
    anime = cursor.fetchall()
    return anime

# ... (other database functions like create_table, add_user, find_user, etc.)

def update_watched_anime(username, anime_title, episodes_watched, status):
    """Updates the episodes watched and status for a user's anime."""
    try:
        cursor.execute('''
            UPDATE user_anime
            SET episodes_watched = ?, status = ?
            WHERE username = ? AND anime_title = ?
        ''', (episodes_watched, status, username, anime_title))
        conn.commit()
        return True, "Update successful."
    except Exception as e:
        # It's good practice to log the actual error for debugging
        print(f"Database error updating anime progress for user {username}, anime {anime_title}: {e}")
        return False, f"An error occurred during the update: {e}"
    
    
#delete the anime from the db
def delete_user_anime(username, anime_title):
    """Deletes a user's anime from the database."""
    try:
        cursor.execute('''
            DELETE FROM user_anime
            WHERE username = ? AND anime_title = ?
        ''', (username, anime_title))
        conn.commit()
        return True, "Anime deleted successfully."
    except Exception as e:
        # It's good practice to log the actual error for debugging
        print(f"Database error deleting anime for user {username}, anime {anime_title}: {e}")
        return False, f"An error occurred during deletion: {e}"
    

#remove all the anime of an user
def delete_all_anime(username):
    cursor.execute('''
        DELETE FROM user_anime WHERE username = ?
    ''', (username,))
    conn.commit()


