import streamlit as st
import base64
import requests
import os, time
from database import user



def get_image_html(path, height="200px"):
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f'<img src="data:image/jpeg;base64,{data}" style="width:100%; height:{height}; object-fit:cover; border-radius: 20px;">'


def show_anime_page():
    #custom css styling
    st.markdown("""
        <style>
        .anime-pic {
            width: 200px;
            height: 200px;
            border-radius: 20px;
            object-fit: cover;
            border: 3px solid black;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            margin-bottom: 10px;
            margin-top: 20px;
        }
        }
        .centered {
            display: flex;
            justify-content: center;
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown(get_image_html("streamlit_app/assets/wallpaper.jpg"), unsafe_allow_html=True)
    st.title("Add Watched Anime")
    st.write("Search and log your watched anime.")

    if "searched_anime" not in st.session_state:
        st.session_state.searched_anime = None

    # Always show the search box
    anime_title = st.text_input("Search Anime Title", key="anime_title_input")

    col_search, col_reset = st.columns([1, 1])
    with col_search:
        if st.button("Search"):
            if anime_title:
                with st.spinner("Searching..."):
                    query = anime_title.strip()
                    search_url = f"https://api.jikan.moe/v4/anime?q={query}&limit=1"
                    response = requests.get(search_url)
                    time.sleep(2)

                if response.status_code == 200 and response.json()["data"]:
                    st.session_state.searched_anime = response.json()["data"][0]
                else:
                    st.warning("Anime not found. Try another title.")
                    st.session_state.searched_anime = None

    if st.session_state.searched_anime:
        anime = st.session_state.searched_anime
        title = anime["title"]
        genres = ", ".join([g["name"] for g in anime["genres"]])
        total_eps = anime.get("episodes", 0)
        rating = anime.get("score", 0.0)
        year = anime.get("year", "Unknown")
        image_url = anime["images"]["jpg"]["image_url"]

        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"""
            <div class="centered">
                <img src="{image_url}" class="anime-pic">
            </div>
        """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <style>
                    .info-box {{
                        background-color: #1f1f2e;
                        padding: 20px;
                        border-radius: 20px;
                        color: white;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                        margin-top: 10px;
                        margin-bottom: 50px;
                        margin-left: 10px;
                    }}
                    .info-box p {{
                        margin: 5px 0;
                        font-size: 16px;
                    }}
                    .info-box h3 {{
                        margin-bottom: 15px;
                        color: #4F8BF9;
                    }}
                </style>

                <div class="info-box">
                    <h3>📺 Anime Information</h3>
                    <p><strong>Title:</strong> {title}</p>
                    <p><strong>Genres:</strong> {genres}</p>
                    <p><strong>Total Episodes:</strong> {total_eps}</p>
                    <p><strong>Rating:</strong> {rating}</p>
                    <p><strong>Year of Release:</strong> {year}</p>
                </div>
            """, unsafe_allow_html=True)


        with st.form("add_anime_form"):
            episodes_watched = st.number_input("Episodes Watched", min_value=0, max_value=total_eps or 1000, step=1)
            status = st.selectbox("Status", ["Watching", "Completed", "On-Hold", "Dropped", "Plan to Watch"])
            submitted = st.form_submit_button("Add to My Anime")

            if submitted:
                current_user = st.session_state.get("username", None)
                if not current_user:
                    st.warning("Please log in to add anime.")
                    return
                user.add_anime(
                    current_user,
                    title.title(),
                    episodes_watched,
                    status,
                    genres,
                    total_eps,
                    year,
                    rating
                )
                st.success(f"{title} added to your list!")
                time.sleep(2)
                st.session_state.searched_anime = None
                st.rerun()