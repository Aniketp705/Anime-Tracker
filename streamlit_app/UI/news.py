import streamlit as st
import os
import sys
import time

# Go one level up from the current directory (scraper)
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import from scraper, database
from scraper import news_scraper
from database import anime_news


def app():
    st.title("📰 Latest Anime News")
    st.subheader("Stay updated with the latest buzz in the anime world!")

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
        /* Remove or comment out the hover effect on the news-box */
        /* .news-box:hover {
        background-color: #ffffff20;
        transition: background-color 0.3s ease;
        } */
        .news-box a {
            text-decoration: none;
            color: #fce4ec;
            transition: color 0.2s ease; /* Add transition for smooth color change */
        }
        .news-box a:hover {
            color: #6495ED; /* Cornflower Blue */
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state for news
    if "news" not in st.session_state:
        st.session_state.news = []

    if st.button("Get Latest News"):
        with st.spinner("Fetching fresh anime news..."):
            anime_news.delete_news()
            news_scraper.fetch_and_store_news()
            # time.sleep(1)
            # Get fresh news and store in session
            st.session_state.news = anime_news.get_news()
            time.sleep(1)
            st.rerun()  # Force a rerun to display the updated news
        

    # Display the news from session state
    if st.session_state.news:
        for i, (title, url) in enumerate(st.session_state.news[:10], start=1):
            st.markdown(f'''
                <div class="news-box">
                    {i}. <a href="{url}" target="_blank">{title}</a>
                </div>
            ''', unsafe_allow_html=True)
            time.sleep(0.1)
    else:
        st.info("Click 'Get Latest News' to fetch the latest updates.")

if __name__ == "__main__":
    app()