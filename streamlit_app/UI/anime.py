import streamlit as st
import base64
import requests
import os
import time
from database import user # Make sure this import works in your environment

# --- Helper Function (Updated) ---
def get_image_html(path, height="200px"):
    try:
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        # Added class 'wallpaper-image' and a wrapper 'wallpaper-container'
        return f'''<div class="wallpaper-container">
                     <img src="data:image/jpeg;base64,{data}" class="wallpaper-image"
                          style="width:100%; height:{height}; object-fit:cover; border-radius: 20px;">
                   </div>'''
    except FileNotFoundError:
        st.error(f"Error: Wallpaper file not found at {path}")
        return '<div style="width:100%; height:200px; background-color:grey; border-radius:20px; display:flex; align-items:center; justify-content:center; color:white;">Wallpaper not found</div>'

# --- Helper Function to Fetch Anime Genres (Cached) ---
@st.cache_data(ttl=3600) # Cache for 1 hour
def fetch_anime_genres():
    """Fetches anime genres from Jikan API."""
    try:
        response = requests.get("https://api.jikan.moe/v4/genres/anime", timeout=10)
        response.raise_for_status() # Raise an exception for HTTP errors
        genres_data = response.json().get("data", [])
        # Create a dictionary of genre_name: genre_id
        return {genre['name']: genre['mal_id'] for genre in genres_data if 'name' in genre and 'mal_id' in genre}
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch genres: {e}")
        return {}
    except Exception as e: # Catch any other unexpected errors during parsing etc.
        st.error(f"An unexpected error occurred while fetching genres: {e}")
        return {}


def show_anime_page():
    # --- Custom CSS Styling with Animations and Hover Effects ---
    st.markdown("""
        <style>
        /* --- General Page Font & Color (Examples, Streamlit themes might override) --- */
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333; /* Default text color */
        }

        /* --- Animations --- */
        @keyframes fadeInPage {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }

        @keyframes fadeInImage {
          from { opacity: 0; transform: scale(0.98); }
          to { opacity: 1; transform: scale(1); }
        }

        @keyframes slideInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes fadeInItem {
            from { opacity: 0; transform: translateX(-10px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        @keyframes fadeInDown {
            from { opacity:0; transform: translateY(-10px); }
            to { opacity:1; transform: translateY(0); }
        }

        /* Apply to wallpaper image */
        .wallpaper-container .wallpaper-image {
          opacity: 0;
          animation: fadeInImage 1s ease-in-out 0.2s forwards; /* 0.2s delay */
        }
        
        /* Styling for Streamlit Title and Subheaders */
        h1[data-testid="stHeading"] { /* Streamlit's title element */
            color: #2c3e50; 
            opacity: 0;
            animation: fadeInDown 0.5s ease-out 0.1s forwards;
            margin-bottom: 0.5rem; /* Adjust spacing */
        }
        
        /* Streamlit's st.write directly after title for subtitle */
        .main > div > div > div > div:nth-child(2) > div p { /* Selector for first st.write */
             opacity: 0;
             animation: fadeInDown 0.5s ease-out 0.3s forwards;
             font-size: 1.1em;
             color: #555;
             margin-bottom: 25px;
        }

        h2[data-testid="stHeading"] { /* Streamlit's st.subheader */
            color: #34495e;
            margin-top: 30px; /* More space before subheaders */
            padding-bottom: 8px;
            border-bottom: 2px solid #ecf0f1;
            opacity: 0;
            animation: fadeInDown 0.5s ease-out 0.4s forwards; /* Delayed slightly */
        }

/* --- General Button Styling (Base for all st.button) --- */
        .stButton > button {
          border-radius: 8px;
          padding: 10px 18px;
          border: 1px solid transparent; /* Or 'border: none;' is also fine */
          background-color: #4F8BF9; /* Primary blue - Default for Search button */
          color: white; /* Text color is white */
          transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out, border-color 0.2s ease-in-out, transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
          box-shadow: 0 2px 4px rgba(0,0,0,0.15);
          font-weight: 600;
          cursor: pointer;
        }

        .stButton > button:hover {
          background-color: #3a70d5; /* Darker primary blue */
          color: white; /* Text remains white */
          /* border: 1px solid #3a70d5; */ /* Optional: if you want border to match darker bg */
          transform: translateY(-2px) scale(1.02); 
          box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }

        /* Ensure :active state also maintains white text if it was changed */
        .stButton > button:active {
          transform: translateY(0px) scale(1);
          box-shadow: 0 2px 3px rgba(0,0,0,0.1);
          background-color: #3566c2; /* Even darker or slightly different shade for active */
          color: white; /* Text remains white */
          /* border-color: #3566c2; */ /* Optional */
        }

        /* --- Styling for 'Add to my list' buttons (in search results) --- */
        .search-result-details .stButton > button {
          background-color: #28a745; /* Green */
          color: white; /* Text color is white */
          /* Other properties like font-size, padding from your existing style */
        }

        .search-result-details .stButton > button:hover {
          background-color: #218838; /* Darker green */
          color: white; /* Text remains white */
          /* border: 1px solid #218838; */ /* Optional */
          /* Inherits transform and box-shadow from general button hover if not overridden */
        }
        .search-result-details .stButton > button:active {
            background-color: #1e7e34; /* Even darker green on active */
            color: white; /* Text remains white */
            /* border-color: #1e7e34; */ /* Optional */
        }


        /* --- Styling for 'Add to My Anime' form submit button --- */
        form[data-testid="stForm"] .stButton > button {
          background-color: #0069d9; /* Form submit blue */
          color: white; /* Text color is white */
          /* Other properties like width, margin, padding from your existing style */
        }

        form[data-testid="stForm"] .stButton > button:hover {
          background-color: #0056b3; /* Darker shade of form blue */
          color: white; /* Text remains white */
          /* border: 1px solid #0056b3; */ /* Optional */
           /* Inherits transform and box-shadow if not overridden */
        }
        form[data-testid="stForm"] .stButton > button:active {
            background-color: #004c9b; /* Even darker form blue on active */
            color: white; /* Text remains white */
            /* border-color: #004c9b; */ /* Optional */
        }

        /* --- Original Styles (with animation/transition additions) --- */
        /* Style for the selected anime image (when one is chosen and form appears) */
        .anime-pic {
            width: 200px;
            height: 200px; 
            border-radius: 20px;
            object-fit: cover;
            border: 3px solid black;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            margin-bottom: 10px;
            margin-top: 20px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .anime-pic:hover { 
            transform: scale(1.03);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        }
        
        .anime-pic-search { /* Used for images in the search results list */
            width: 200px; 
            height: 250px;
            border-radius: 10px;
            object-fit: cover;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
            margin-top: 5px;
            margin-bottom: 5px;
        }
        .anime-pic-search:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }

        .centered { 
            display: flex;
            justify-content: left; 
        }

        .info-box { /* For "Selected Anime Details" section */
            background-color: #1f1f2e; 
            padding: 25px; 
            border-radius: 20px;
            color: white;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            margin-top: 20px; 
            margin-bottom: 25px;
            margin-left: 0px; 
            display: flex; 
            flex-direction: row; 
            align-items: flex-start; 
            transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
            opacity: 0; 
            animation: slideInUp 0.5s ease-out 0.2s forwards; 
        }
        .info-box:hover {
            transform: translateY(-5px); 
            box-shadow: 0 8px 20px rgba(0,0,0,0.25);
        }

        .info-box p {
            margin: 8px 0; 
            font-size: 16px;
            line-height: 1.6; 
        }
        .info-box h3 {
            margin-bottom: 20px; 
            color: #5DADE2; 
            margin-top: 0; 
            font-size: 22px; 
        }

        .anime-pic-in-info { 
            width: 180px; 
            height: auto;
            max-height: 250px; 
            border-radius: 15px; 
            object-fit: cover;
            margin-right: 25px; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            margin-top: 5px; 
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .anime-pic-in-info:hover {
            transform: scale(1.03);
            box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        }
        
        div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column"] > div[data-testid="stVerticalBlock"] {
            opacity: 0;
            animation: fadeInItem 0.4s ease-out forwards;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 8px;
            transition: background-color 0.2s ease;
        }
         div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column"] > div[data-testid="stVerticalBlock"]:hover {
            background-color: #f0f2f6; 
        }


        .search-result-details {
            flex-grow: 1;
            margin-left: 15px;
        }
        .search-result-details h4 {
            margin-top: 0;
            margin-bottom: 8px; 
            color: #333;
            font-size: 1.1em; 
        }
        .search-result-details p {
            font-size: 0.9em;
            color: #555; 
            margin-bottom: 8px;
            line-height: 1.5;
        }
        
        .stTextInput input {
            border-radius: 8px;
            border: 1px solid #ddd; 
            padding: 10px 12px;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05) inset;
        }
        .stTextInput input:focus {
            border-color: #4F8BF9;
            box-shadow: 0 0 0 0.2rem rgba(79, 139, 249, 0.25), 0 1px 2px rgba(0,0,0,0.05) inset;
        }

        hr[data-testid="stDivider"] {
            border-top: 1px solid #e0e0e0; 
            margin-top: 25px; 
            margin-bottom: 25px;
        }

        </style>
    """, unsafe_allow_html=True)

    # --- Page Setup ---
    image_path = "streamlit_app/assets/wallpaper.jpg" # Make sure this path is correct
    st.markdown(get_image_html(image_path, height="220px"), unsafe_allow_html=True) # Slightly taller wallpaper
    st.title("Add Anime")
    st.write("Search and log your watched/planned anime. Discover new series or revisit old favorites.") # Enhanced subtitle

    # --- Initialize Session State Variables ---
    if "search_results" not in st.session_state:
        st.session_state.search_results = None
    if "selected_anime" not in st.session_state:
        st.session_state.selected_anime = None
    if "show_search_results" not in st.session_state:
        st.session_state.show_search_results = False
    if "clear_search_input_on_next_run" not in st.session_state:
        st.session_state.clear_search_input_on_next_run = False
    if "anime_title_input" not in st.session_state:
        st.session_state.anime_title_input = ""
    if "genre_select" not in st.session_state: # For genre dropdown
        st.session_state.genre_select = "Select a genre..."

    if st.session_state.get("clear_search_input_on_next_run", False):
        st.session_state.anime_title_input = ""
        st.session_state.clear_search_input_on_next_run = False

    anime_title_from_input = st.text_input(
        "Search Anime Title",
        key="anime_title_input",
        placeholder="E.g., Attack on Titan, Naruto, Your Name..." # Added placeholder
    )

    col_search, col_spacer = st.columns([1, 3]) # Adjusted columns for search button

    with col_search:
        if st.button("🔍 Search", key="search_button"): # Added emoji to button
            if anime_title_from_input:
                st.session_state.genre_select = "Select a genre..." # Reset genre dropdown
                with st.spinner("Searching for anime... 📺"): # Enhanced spinner text
                    query = anime_title_from_input.strip()
                    search_url = f"https://api.jikan.moe/v4/anime?q={query}&limit=8&sfw"
                    try:
                        response = requests.get(search_url, timeout=10)
                        time.sleep(0.5) # Respect API rate limits

                        if response.status_code == 200:
                            data = response.json().get("data", [])
                            if isinstance(data, list) and data:
                                st.session_state.search_results = data
                                st.session_state.selected_anime = None
                                st.session_state.show_search_results = True
                                st.rerun() # Rerun to reflect changes and reset genre dropdown
                            else:
                                st.warning("No anime found for that title. Please try a different one! 🤔")
                                st.session_state.search_results = None
                                st.session_state.selected_anime = None
                                st.session_state.show_search_results = False
                                # No rerun needed, warning is shown
                        else:
                            st.error(f"API Error (Code: {response.status_code}). Please try again later. 😥")
                            st.session_state.search_results = None
                            st.session_state.selected_anime = None
                            st.session_state.show_search_results = False
                            # No rerun needed
                    except requests.exceptions.RequestException as e:
                        st.error(f"Network error: Could not connect to the anime database. 🌐 ({e})")
                        st.session_state.search_results = None
                        st.session_state.selected_anime = None
                        st.session_state.show_search_results = False
                        # No rerun needed
            else:
                st.warning("Please enter an anime title to search. 🎬")

    st.divider()
    st.subheader("Or Search by Genre")

    genres_dict = fetch_anime_genres()
    genre_names_options = ["Select a genre..."] + list(genres_dict.keys())

    selected_genre_name = st.selectbox(
        "Select Genre",
        options=genre_names_options,
        key="genre_select" # Uses the initialized session state key
    )

    col_genre_search, col_genre_spacer = st.columns([1, 3]) # Adjusted columns for search button
    with col_genre_search:
        if st.button("✨ Search by Genre", key="genre_search_button"):
            if selected_genre_name != "Select a genre..." and selected_genre_name in genres_dict:
                genre_id = genres_dict[selected_genre_name]
                st.session_state.clear_search_input_on_next_run = True # Set flag to clear title input on next run
                with st.spinner(f"Searching top anime in {selected_genre_name}... 📺"):
                    search_url = f"https://api.jikan.moe/v4/anime?genres={genre_id}&limit=10&order_by=score&sort=desc&sfw"
                    try:
                        response = requests.get(search_url, timeout=10)
                        time.sleep(0.5) # Respect API rate limits
                        response.raise_for_status()
                        data = response.json().get("data", [])
                        if isinstance(data, list) and data:
                            st.session_state.search_results = data
                            st.session_state.selected_anime = None
                            st.session_state.show_search_results = True
                            st.rerun() # Rerun to reflect changes and clear title input
                        else:
                            st.warning(f"No top anime found for the genre '{selected_genre_name}'. Try another genre! 🤔")
                            st.session_state.search_results = None
                            st.session_state.selected_anime = None
                            st.session_state.show_search_results = False
                    except requests.exceptions.RequestException as e:
                        st.error(f"API Error or Network issue during genre search (Code: {response.status_code if 'response' in locals() else 'N/A'}). Details: {e} 😥")
                        st.session_state.search_results = None
                        st.session_state.selected_anime = None
                        st.session_state.show_search_results = False
            else:
                st.warning("Please select a genre to search. 🎶")

    if st.session_state.show_search_results and st.session_state.search_results and not st.session_state.selected_anime:
        st.divider()
        st.subheader("Search Results:")
        for i, anime_result in enumerate(st.session_state.search_results):
            title = anime_result.get("title", "N/A")
            mal_id = anime_result.get("mal_id")
            image_url = anime_result.get("images", {}).get("jpg", {}).get("image_url", "https://via.placeholder.com/100x150?text=No+Image")
            year = anime_result.get("year", "N/A")
            anime_type = anime_result.get("type", "N/A")
            synopsis = anime_result.get("synopsis", "No synopsis available.")
            if synopsis and len(synopsis) > 120: # Shorter synopsis for list view
                synopsis = synopsis[:120] + "..."

            with st.container(): # Each result item
                col_img, col_details = st.columns([1, 4])

                with col_img:
                    # Corrected class to 'anime-pic-search'
                    st.markdown(f'<img src="{image_url}" class="anime-pic-search">', unsafe_allow_html=True)

                with col_details:
                    st.markdown(f'<div class="search-result-details">', unsafe_allow_html=True)
                    st.markdown(f"<h4>{title}</h4>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Type:</strong> {anime_type} | <strong>Year:</strong> {year}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p>{synopsis}</p>", unsafe_allow_html=True)

                    button_key = f"select_{mal_id}_{i}"
                    if st.button("➕ Add to my list", key=button_key): # Added emoji
                        st.session_state.selected_anime = anime_result
                        st.session_state.show_search_results = False
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<hr style='margin-top: 10px; margin-bottom:10px; border-color: #eee;'>", unsafe_allow_html=True) # Lighter separator


    if st.session_state.selected_anime:
        st.divider()
        st.subheader("Selected Anime Details:")
        anime = st.session_state.selected_anime

        title = anime.get("title", "N/A")
        genres_list = anime.get("genres", [])
        genres = ", ".join([g.get("name", "N/A") for g in genres_list]) if genres_list else "N/A"
        total_eps = anime.get("episodes")
        rating = anime.get("score", 0.0)
        year = anime.get("year", "Unknown")
        image_url = anime.get("images", {}).get("jpg", {}).get("image_url", "https://via.placeholder.com/200x200?text=No+Image")

        # Using st.columns within the markdown for info-box layout
        st.markdown('<div class="info-box">', unsafe_allow_html=True) # Start info-box
        col_img_info, col_text_info = st.columns([1, 2.5]) # Adjusted ratio

        with col_img_info:
            # The class "anime-pic" is currently defined for the image *inside* the info box
            # For consistency, let's use "anime-pic-in-info" as defined in CSS
            st.markdown(f'<img src="{image_url}" class="anime-pic-in-info">', unsafe_allow_html=True)

        with col_text_info:
            st.markdown(f"""
                <h3>📺 Anime Information</h3>
                <p><strong>Title:</strong> {title}</p>
                <p><strong>Genres:</strong> {genres}</p>
                <p><strong>Total Episodes:</strong> {total_eps if total_eps else 'Unknown'}</p>
                <p><strong>Rating (MAL):</strong> {rating if rating else 'N/A'}</p>
                <p><strong>Year:</strong> {year}</p>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True) # End info-box

        st.subheader("Log Your Progress:") # Changed subheader
        current_username = st.session_state.username

        with st.form("add_anime_form", clear_on_submit=True):
            max_episodes = total_eps if isinstance(total_eps, int) and total_eps > 0 else 5000
            min_episodes = 0

            episodes_watched = st.number_input(
                "Episodes Watched",
                min_value=min_episodes,
                max_value=max_episodes,
                value=0,
                step=1
            )

            default_status = "Watching"
            if isinstance(total_eps, int) and total_eps > 0 and episodes_watched >= total_eps:
                default_status = "Completed"
            elif episodes_watched == 0:
                default_status = "Plan to Watch"

            status_options = ["Watching", "Completed", "On-Hold", "Dropped", "Plan to Watch"]
            try:
                default_index = status_options.index(default_status)
            except ValueError:
                default_index = 0

            status_selected = st.selectbox(
                "Status",
                status_options,
                index=default_index
            )

            submitted = st.form_submit_button("💾 Add to My Anime List") # Added emoji

            if submitted:
                try:
                    final_episodes_watched = episodes_watched
                    if status_selected == "Completed" and isinstance(total_eps, int) and total_eps > 0 and episodes_watched < total_eps:
                        final_episodes_watched = total_eps
                    elif status_selected == "Plan to Watch": # If plan to watch, eps watched should be 0
                         final_episodes_watched = 0


                    db_status, db_msg = user.add_anime(
                        current_username,
                        title,
                        final_episodes_watched,
                        status_selected,
                        genres if genres != "N/A" else "",
                        total_eps if total_eps else None,
                        year if year != "Unknown" else None,
                        rating if rating else None
                    )
                except Exception as e:
                    st.error(f"Error interacting with database: {e}")
                    db_status = False
                    db_msg = f"Database error: {e}"

                if db_status:
                    st.success(f"🎉 '{title}' successfully added/updated in your list!")
                else:
                    st.error(db_msg if db_msg else "❌ Failed to add/update anime. Please try again.")

                time.sleep(2) # Show message briefly
                st.session_state.selected_anime = None
                st.session_state.search_results = None
                st.session_state.show_search_results = False
                st.session_state.clear_search_input_on_next_run = True
                st.rerun()
