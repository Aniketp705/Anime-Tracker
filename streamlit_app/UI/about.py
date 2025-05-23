import streamlit as st

def show_about_page():
    st.markdown(
        """
        <style>
        /* Removed Global App Background Animation to avoid affecting other tabs */
        .stApp {
            color: #ffffff;
            font-family: 'Arial', sans-serif;
            padding: 20px;
        }

        /* Title Styling with Subtle Animation */
        h1 {
            color: #fce4ec;
            text-align: center;
            padding-bottom: 1rem;
            border-bottom: 2px solid #444;
            margin-bottom: 2rem;
            text-shadow: 0 0 5px rgba(252, 228, 236, 0.5); /* Subtle glow */
            transition: text-shadow 0.3s ease;
        }
        h1:hover {
            text-shadow: 0 0 15px rgba(252, 228, 236, 0.8); /* Stronger glow on hover */
        }

        /* About Box Styling with Hover Effect */
        .about-box {
            background-color: #ffffff10;
            padding: 2rem;
            margin: 2rem auto;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            font-weight: 500;
            line-height: 1.6;
            max-width: 800px;
            transition: transform 0.3s ease, box-shadow 0.3s ease, background-color 0.3s ease; /* Smooth transitions */
            border: 1px solid transparent; /* Initial transparent border */
        }
        .about-box:hover {
            transform: translateY(-5px); /* Lift effect on hover */
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3); /* Stronger shadow on hover */
            background-color: #ffffff15; /* Slightly lighter background on hover */
            border-color: #fce4ec; /* Accent border on hover */
        }

        .about-box p {
            margin-bottom: 1rem;
        }
        .about-box strong {
            font-weight: 600;
            color: #fce4ec;
        }

        /* List Item Animations */
        .about-box ul {
            list-style: none; /* Remove default bullet points */
            padding-left: 0;
        }
        .about-box li {
            position: relative;
            padding-left: 25px; /* Space for custom bullet */
            margin-bottom: 0.8rem;
            opacity: 0; /* Start hidden for animation */
            transform: translateX(-20px); /* Start slightly left for slide-in */
            animation: fadeInSlideIn 0.6s ease-out forwards;
        }
        .about-box li:nth-child(1) { animation-delay: 0.2s; }
        .about-box li:nth-child(2) { animation-delay: 0.4s; }
        .about-box li:nth-child(3) { animation-delay: 0.6s; }
        /* Add more nth-child rules if you have more list items */

        /* Custom bullet point for list items */
        .about-box li::before {
            content: "✨"; /* Fun emoji bullet */
            position: absolute;
            left: 0;
            color: #fce4ec; /* Match accent color */
            font-size: 1.2em;
            line-height: 1;
        }

        @keyframes fadeInSlideIn {
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        /* Removed .about-image styling as images are no longer present */
        .st-emotion-cache-lky0z6 { /* Target expander header */
             background-color: #3a4a5a;
             color: #ffffff;
             border-radius: 5px;
             padding: 10px;
             margin-bottom: 0;
        }
        .st-emotion-cache-lky0z6 .st-emotion-cache-10trjem { /* Target expander title */
             color: #ffffff;
             font-weight: bold;
        }
        .st-emotion-cache-lky0z6 .st-emotion-cache-1k7hjsq { /* Target expander content */
             background-color: #2a3a4a;
             padding: 10px;
             border-radius: 5px;
             border: 1px solid #3a4a5a;
             margin-top: 0;
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
                    <li><strong>Track Your Progress</strong> by marking episodes as watched and keeping a clear overview of your completed, currently watching, and planned series.</li>
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
