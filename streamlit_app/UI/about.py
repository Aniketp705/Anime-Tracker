import streamlit as st
from streamlit_option_menu import option_menu

def show_about_page():
    st.title("About The App")

    st.markdown('''
        <style>
        .about-box {
            background-color: #ffffff10;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            font-weight: 600;
        }
        </style>
    ''', unsafe_allow_html=True)

    st.markdown('''
        <div class="about-box">
        Welcome to the Anime Tracker App!

        This application is designed to help anime enthusiasts keep track of their favorite shows, discover new ones, and manage their watchlists efficiently. 
        With an intuitive interface and powerful features, you can explore anime details, track your progress, and stay updated on upcoming releases.

        Whether you're a casual viewer or a dedicated fan, this app is your ultimate companion for all things anime.
        </div>
    ''', unsafe_allow_html=True)
    