import streamlit as st
from streamlit_option_menu import option_menu

def show_about_page():
    st.markdown(
        """
        <style>
        h1 {
            color: #fce4ec;
            text-align: center;
            padding-bottom: 1rem;
            border-bottom: 2px solid #444;
            margin-bottom: 2rem;
        }
        .about-box {
            background-color: #ffffff10;
            padding: 2rem;
            margin: 2rem auto; /* Center the box */
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* Slightly stronger shadow */
            font-weight: 500; /* Slightly lighter font weight for body text */
            line-height: 1.6; /* Improved line height for readability */
            max-width: 700px; /* Limit the width of the box for better reading experience */
        }
        .about-box p {
            margin-bottom: 1rem;
        }
        .about-box strong {
            font-weight: 600; /* Emphasize key terms */
            color: #fce4ec; /* Highlight important words */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("About The Anime Tracker App")

    st.markdown(
        f"""
        <div class="about-box">
            <p>
                Welcome to the <strong>Anime Tracker App</strong>!
            </p>
            <p>
                This application is crafted with passion to serve as your dedicated companion in the vast and exciting world of anime. Our primary goal is to empower anime enthusiasts like yourself to effortlessly <strong>keep track of your favorite shows</strong>, <strong>discover captivating new series</strong>, and <strong>manage your personal watchlists</strong> with unparalleled efficiency.
            </p>
            <p>
                We understand the joy of finding a new anime that resonates with you, and the importance of remembering where you left off in a long-running series. That's why we've designed this app with an <strong>intuitive and user-friendly interface</strong>, coupled with <strong>powerful features</strong> to enhance your anime viewing experience.
            </p>
            <p>
                With the Anime Tracker App, you can:
                <ul>
                    <li><strong>Explore</strong> detailed information about a wide range of anime, including summaries, genres, ratings, and more.</li>
                    <li><strong>Track Your Progress</strong> by marking episodes as watched and keeping a clear overview of your completed, currently watching, and планируемые (planned) series.</li>
                    <li><strong>Stay Updated</strong> on upcoming anime releases and never miss the premiere of a show you're looking forward to.</li>
                </ul>
            </p>
            <p>
                Whether you identify as a <strong>casual anime enjoyer</strong> just starting your journey, or a <strong>dedicated, long-time fan</strong> with an extensive watchlist, we believe this app will become an indispensable tool in your anime adventures.
            </p>
            <p>
                Thank you for choosing the Anime Tracker App. We hope it brings you as much joy as the anime we all love!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )