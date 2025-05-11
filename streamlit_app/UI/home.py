import streamlit as st
import base64
import os
import requests
import time


def get_image_html(path, height="300px", width="100%", border_radius="10px"):
    """Reads image and returns HTML for embedding."""
    if not os.path.exists(path):
        st.error(f"Error: Image file not found at {path}")
        return f'<div style="width:{width}; height:{height}; background-color:grey; border-radius:{border_radius}; display:flex; align-items:center; justify-content:center; color:white;">Image not found</div>'

    try:
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f'<img src="data:image/jpeg;base64,{data}" style="width:{width}; height:{height}; object-fit:cover; border-radius: {border_radius}; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);">'
    except Exception as e:
        st.error(f"Error embedding image from {path}: {e}")
        return f'<div style="width:{width}; height:{height}; background-color:grey; border-radius:{border_radius}; display:flex; align-items:center; justify-content:center; color:white;">Error loading image</div>'


def app():
    # --- Custom CSS Styling ---
    st.markdown("""
        <style>
        # .stApp {
        #     background-color: #1f1f2e;
        #     color: white;
        #     font-family: 'Arial', sans-serif;
        # }

        .stApp h1 {
            color: #fce4ec;
            text-align: center;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }

        .stApp h4 {
             color: #b3e5fc;
             text-align: center;
             margin-top: 0;
             margin-bottom: 30px;
        }

        /* Removed .hero-section styles */

        .feature-item {
            background-color: #2c2c3d;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            text-align: center;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .feature-item h5 {
            color: #fce4ec;
            margin-top: 10px;
            margin-bottom: 5px;
        }
        .feature-item p {
            color: #b0bec5;
            font-size: 0.9em;
        }
        .feature-item .feature-icon {
             font-size: 2em;
             color: #4F8BF9;
             margin-bottom: 10px;
        }

        /* Removed .stButton styles */

        .footer {
            text-align: center;
            margin-top: 50px;
            font-size: 0.9em;
            color: #b0bec5;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Title and Subheading ---
    st.title("🎉 Welcome to Anime Tracker!")
    st.markdown("""
        <h4 style='text-align: center; color: #b3e5fc;'>
            Your personal space to explore, track, and organize all your favorite anime.
        </h4>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # --- Feature Highlights Section ---
    st.markdown("### ✨ Key Features:")
    st.markdown('<div style="margin-bottom: 30px;">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
            <div class="feature-item">
                <span class="feature-icon">🔍</span>
                <h5>Powerful Search</h5>
                <p>Find anime from a vast, constantly updated database.</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="feature-item">
                <span class="feature-icon">📝</span>
                <h5>Progress Tracking</h5>
                <p>Log episodes watched and manage your watchlists easily.</p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="feature-item">
                <span class="feature-icon">📊</span>
                <h5>Personalized Stats</h5>
                <p>Visualize your watching habits and favorite genres.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


    st.markdown("---")


    # --- Main Image Section ---
    image_path = "streamlit_app/assets/cityscape.jpg"
    st.markdown(get_image_html(image_path, height="200px", border_radius="10px"), unsafe_allow_html=True)


    st.markdown("---")


    # --- Footer ---
    st.markdown("""
        <div class="footer">
            <p>Made with ❤️ for anime lovers.</p>
            <p>&copy; 2023-2025 AnimeTracker. All rights reserved.</p>
        </div>
    """, unsafe_allow_html=True)