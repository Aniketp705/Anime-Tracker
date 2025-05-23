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
        /* No .stApp global background changes here */

        /* Keyframes for animations */
        @keyframes fadeInScale {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }

        @keyframes slideInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes pulseGlow {
            0% { text-shadow: 0 0 5px rgba(252, 228, 236, 0.5); }
            50% { text-shadow: 0 0 15px rgba(252, 228, 236, 0.8); }
            100% { text-shadow: 0 0 5px rgba(252, 228, 236, 0.5); }
        }

        /* Title Styling with Animation */
        .stApp h1 {
            color: #fce4ec;
            text-align: center;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            opacity: 0; /* Start hidden */
            animation: fadeInScale 1s ease-out forwards;
            animation-delay: 0.2s;
        }

        /* Subheading Styling with Animation */
        .stApp h4 {
            color: #b3e5fc;
            text-align: center;
            margin-top: 0;
            margin-bottom: 30px;
            opacity: 0; /* Start hidden */
            animation: slideInUp 0.8s ease-out forwards;
            animation-delay: 0.5s;
        }

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
            opacity: 0; /* Start hidden for animation */
            transform: translateY(20px); /* Start slightly down */
            animation: slideInUp 0.7s ease-out forwards;
            transition: transform 0.3s ease, box-shadow 0.3s ease; /* Hover transition */
        }
        .feature-item:hover {
            transform: translateY(-5px); /* Lift effect on hover */
            box-shadow: 0 8px 16px rgba(0,0,0,0.4); /* Stronger shadow on hover */
        }
        /* Staggered animation delays for feature items */
        .st-emotion-cache-1r6dm5b > div:nth-child(1) .feature-item { animation-delay: 0.8s; } /* Target first column's feature-item */
        .st-emotion-cache-1r6dm5b > div:nth-child(2) .feature-item { animation-delay: 1.0s; } /* Target second column's feature-item */
        .st-emotion-cache-1r6dm5b > div:nth-child(3) .feature-item { animation-delay: 1.2s; } /* Target third column's feature-item */


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
            font-size: 2.5em; /* Slightly larger icon */
            color: #4F8BF9;
            margin-bottom: 10px;
            animation: pulseGlow 2s infinite alternate; /* Pulsing glow for icons */
        }
        /* Staggered pulse glow for icons */
        .st-emotion-cache-1r6dm5b > div:nth-child(1) .feature-icon { animation-delay: 0.5s; }
        .st-emotion-cache-1r6dm5b > div:nth-child(2) .feature-icon { animation-delay: 0.7s; }
        .st-emotion-cache-1r6dm5b > div:nth-child(3) .feature-icon { animation-delay: 0.9s; }


        /* Main Image Section Animation */
        .main-image-container img {
            opacity: 0;
            transform: translateY(20px);
            animation: slideInUp 1s ease-out forwards;
            animation-delay: 1.5s; /* Delay after features */
        }

        .footer {
            text-align: center;
            margin-top: 50px;
            font-size: 0.9em;
            color: #b0bec5;
            opacity: 0;
            animation: fadeInScale 1s ease-out forwards;
            animation-delay: 2s; /* Delay footer appearance */
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
    # Added a container for feature items to better target them with CSS
    st.markdown('<div class="feature-section-container" style="margin-bottom: 30px;">', unsafe_allow_html=True)

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

    st.markdown('</div>', unsafe_allow_html=True) # Close feature-section-container


    st.markdown("---")


    # --- Main Image Section ---
    image_path = "streamlit_app/assets/cityscape.jpg"
    # Added a container for the image to apply animation to it
    st.markdown('<div class="main-image-container">', unsafe_allow_html=True)
    st.markdown(get_image_html(image_path, height="200px", border_radius="10px"), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


    st.markdown("---")


    # --- Footer ---
    st.markdown("""
        <div class="footer">
            <p>Made with ❤️ for anime lovers.</p>
            <p>&copy; 2023-2025 AnimeTracker. All rights reserved.</p>
        </div>
    """, unsafe_allow_html=True)
