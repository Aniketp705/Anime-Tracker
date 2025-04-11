import streamlit as st
import base64
from database import user

def get_image_html(path, height="200px"):
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f'<img src="data:image/jpeg;base64,{data}" style="width:100%; height:{height}; object-fit:cover; border-radius: 20px;">'


def show_anime_page():
    # col1, col2, col3 = st.columns([1, 3, 1])
    # with col2:
    st.markdown(get_image_html("streamlit_app/assets/wallpaper.jpg"), unsafe_allow_html=True)

    st.title("My Anime")
    
    st.subheader("Add Anime to Your List")

    with st.form("anime_form"):
        anime_title = st.text_input("Anime Title", placeholder="e.g. Attack on Titan")
        episodes_watched = st.number_input("Episodes Watched", min_value=0, step=1)
        status = st.selectbox("Watch Status", ["Watching", "Completed", "Plan to Watch", "Dropped"])
        submitted = st.form_submit_button("Add Anime")

        if submitted:
            if anime_title.strip() == "":
                st.error("Anime title cannot be empty.")
            else:
                success, msg = user.add_anime(
                    username=st.session_state.username,
                    anime_title=anime_title.strip().title(),
                    episodes_watched=episodes_watched,
                    status=status
                )
                if success:
                    st.success(msg)
                else:
                    st.error(msg)