import streamlit as st 
import os
import sys
import time

# Go one level up from the current directory (scraper)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import from scraper, database
from scraper import news_scraper
from database import anime_news


def app():
    st.title("📰 Latest Anime News")
    st.subheader("Stay updated with the latest buzz in the anime world!")

    # Inject a little CSS for news card style
    st.markdown("""
        <style>
        .news-box {
            background-color: #ffffff10;
            padding: 1rem;
            margin: 1rem 0;
            border-left: 5px solid #e73c7e;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.button("Get Latest News"):
        with st.spinner("Fetching fresh anime news..."):
            # Clear the existing news from the database
            anime_news.delete_news()

            # Fetch and store the latest news
            news_scraper.fetch_and_store_news()
            time.sleep(1)
            
        # Get the latest news from the database
        news_list = anime_news.get_news()

        st.session_state.news = []
        if news_list:
            for i, (title, url) in enumerate(news_list, start=1):
                st.session_state.news.append(title)
                st.markdown(f'''
                    <div class="news-box">
                            {i}. <a href="{url}" target="_blank" style="text-decoration: none; color: #e73c7e;">{title}</a>
                    ''', unsafe_allow_html=True)    
                time.sleep(0.2)
                if i == 10:
                    break
        else:
            st.warning("No news available.")

    
    
