import os
import sqlite3

# Get the absolute path to the db folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "anime_news.db")

# Connect using the full path
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()

# Create the table if it doesn't exist
def create_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS anime_news(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            link TEXT NOT NULL,
            date TEXT DEFAULT (DATE('now'))
        )
    ''')
    conn.commit()
    
#add news to the database
def add_news(title, description, link):
    cursor.execute("SELECT * FROM anime_news WHERE title = ?", (title,))
    if cursor.fetchone() is None:
        cursor.execute('''
            INSERT INTO anime_news (title, description, link) VALUES (?, ?, ?)
        ''', (title, description, link))
        conn.commit()


# Get the latest news from the database
def get_news():
    cursor.execute('''SELECT title,link FROM anime_news ORDER BY date DESC''')
    news = cursor.fetchall()
    return news

#clear the news from the database
def delete_news():
    cursor.execute('''DELETE FROM anime_news''')
    conn.commit()


print(get_news())