import streamlit as st
import base64

def get_image_html(path, height="200px"):
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f'<img src="data:image/jpeg;base64,{data}" style="width:100%; height:{height}; object-fit:cover; border-radius: 20px;">'


def show_anime_page():
    # col1, col2, col3 = st.columns([1, 3, 1])
    # with col2:
    st.markdown(get_image_html("streamlit_app/assets/wallpaper.jpg"), unsafe_allow_html=True)

    st.title("My Anime")
    st.write("This is the My Anime page.")
    st.write("You can add your favorite anime here.")
    # Add your anime-related content here
    st.text_input("Anime Title")
    st.text_area("Description")
    st.button("Add to My Anime")  # Placeholder for adding functionality