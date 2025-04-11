import streamlit as st
from streamlit_option_menu import option_menu
from UI import about, home, anime, news, account, profile
import pathlib



#set page config
try:
    st.set_page_config(
        page_title="Anime Hub",
        page_icon=":sparkles:",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
except:
    pass

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None


# Animated background
page_bg_img = f"""
<style>
/* Animated background gradient */
[data-testid="stAppViewContainer"] > .main {{
background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
background-size: 400% 400%;
animation: gradientBG 15s ease infinite;
}}

[data-testid="stSidebar"] > div:first-child {{
background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
background-size: 400% 400%;
animation: gradientBG 15s ease infinite;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}



@keyframes gradientBG {{
    0% {{
        background-position: 0% 50%;
    }}
    50% {{
        background-position: 100% 50%;
    }}
    100% {{
        background-position: 0% 50%;
    }}
}}
</style>
"""



# st.markdown(page_bg_img, unsafe_allow_html=True)


class MultiApp:
    def __init__(self):
        if st.session_state.logged_in:
            self.apps = [
                {"title": "Home", "function": home.app},
                {"title": "My Anime", "function": anime.show_anime_page},
                {"title": "News", "function": news.app},
                {"title": "About", "function": about.show_about_page},
                {"title": "Account", "function": account.my_account},
                {"title": "Profile", "function": profile.show_profile}
            ]
        else:
            self.apps = [
                {"title": "Home", "function": home.app},
                {"title": "Account", "function": account.my_account}
            ]

    def run(self):

        # Inject custom CSS
        st.markdown(
            """
            <style>
            /* Target the outermost navbar wrapper with class 'menu' */
            [data-testid = "st.menu"] {
                background-color: transparent ; /* Or match your theme */
                border-radius: 30px !important;
                box-shadow: none !important;
                margin-top: 10px;
                padding: 0 !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )


        # only display the menu if the user is logged in
        if st.session_state.logged_in:
            menu_items = ["Home", "My Anime", "News", "About", "Profile", "Account"]
            icons_list = ["house", "book", "journal-text", "info-circle", "person-badge", "person"]
        
        else:
            menu_items = ["Home", "Account"]
            icons_list = ["house", "person"]

        selected = option_menu(
            menu_title=None,
            options=menu_items,
            icons=icons_list,
            orientation="horizontal",
            default_index=0,
            styles={
                "container": {
                    # "padding": "0", 
                    "background-color": "#1f1f2e",
                    "border-radius": "10px",
                },
                "nav-link": {
                    "font-size": "16px",
                    "color": "white",
                    "margin": "0",
                    "left": "0px",
                },
                "nav-link-selected": {
                    "color": "black",
                    "background-color": "#fce4ec",
                },
            }
        )



        for app in self.apps:
            if app["title"] == selected:
                app["function"]()

app = MultiApp()
app.run()
