import streamlit as st
from streamlit_option_menu import option_menu
import base64
import assets


def get_image_html(path, height="200px"):
    # Add basic error handling for file not found
    try:
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f'<img src="data:image/jpeg;base64,{data}" style="width:100%; height:{height}; object-fit:cover; border-radius: 20px;">'
    except FileNotFoundError:
        st.error(f"Error: Wallpaper file not found at {path}")
        # Provide a fallback or placeholder if needed
        return '<div style="width:100%; height:200px; background-color:grey; border-radius:20px; display:flex; align-items:center; justify-content:center; color:white;">Wallpaper not found</div>'


def app():
    # Page title
    st.title("🎉 Welcome to Anime Tracker!")

    # Subheading
    st.markdown("""
        <h4 style='color: #888;'>Your personal space to explore, track, and organize all your favorite anime.</h4>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Feature Highlights
    st.markdown("""
        ### ✨ Features:
        - 🔍 **Search** for anime from a vast database.
        - 📝 **Track your watch progress** and update status.
        - 📊 **Get stats** on what you've watched.
        - 📰 **Stay updated** with the latest anime news.
    """)

    st.markdown("---")

    # Add a sample anime-themed image (optional: replace with your own hosted image later)
    st.markdown(get_image_html("streamlit_app/assets/animecharacters.jpg"), unsafe_allow_html=True)

    st.markdown("---")

    # Footer or welcome message
    st.markdown("""
        <p style="text-align:center; font-size:18px;">
            Made with ❤️ for anime lovers.
        </p>
    """, unsafe_allow_html=True)
