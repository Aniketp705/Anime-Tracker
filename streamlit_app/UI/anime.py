import streamlit as st
import base64
import requests
import os
import time
# Assuming 'user' object with 'add_anime' method is available globally
from database import user

# --- Helper Function (Using your provided version) ---
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


def show_anime_page():
    # --- Custom CSS Styling (Combined from original and multi-result needs) ---
    st.markdown("""
        <style>
        /* Style for the selected anime image (from original) */
        .anime-pic {
            width: 200px;
            height: 200px; /* Adjust height as needed */
            border-radius: 20px;
            object-fit: cover;
            border: 3px solid black;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            margin-bottom: 10px;
            margin-top: 20px;
        }
        /* Style for search results images (from multi-result) */
        .anime-pic-search {
            width: 100px;
            height: 150px;
            border-radius: 10px;
            object-fit: cover;
            margin-right: 15px;
            vertical-align: top; /* Align image with text */
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Subtle shadow */
        }
        .centered {
            display: flex;
            justify-content: left; /* Keep left alignment for consistency */
        }
        /* Style for info box (from original) */
        .info-box {
            background-color: #1f1f2e;
            padding: 20px;
            border-radius: 20px;
            color: white;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-top: 10px; /* Adjusted margin */
            margin-bottom: 20px;
            margin-left: 10px;
            display: flex; /* Enable flexbox for potential adjustments */
            flex-direction: row; /* Arrange items in a row */
            align-items: flex-start; /* Align items to the top */
        }
        .info-box p {
            margin: 5px 0;
            font-size: 16px;
        }
        .info-box h3 {
            margin-bottom: 15px;
            color: #4F8BF9;
            margin-top: 0; /* Remove default top margin */
        }
        /* New style for the image inside the info box */
        .anime-pic-in-info {
            width: 150px; /* Adjust width as needed */
            height: auto;
            border-radius: 10px;
            object-fit: cover;
            margin-right: 15px; /* Space between image and text */
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-top: 20px; /* Space above the image */
        }
        /* Style for search result items (from multi-result) */
        .search-result-item {
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            display: flex; /* Use flexbox for layout */
            align-items: flex-start; /* Align items to the top */
            background-color: #fce4ec; /* Light background */
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05); /* Very subtle shadow */
        }
        .search-result-details {
            flex-grow: 1; /* Allow details to take remaining space */
            margin-left: 15px; /* Space between image and text */
        }
        .search-result-details h4 { /* Using h4 for result titles */
            margin-top: 0;
            margin-bottom: 5px;
            color: #333; /* Darker title */
        }
        .search-result-details p { /* Smaller text for result details */
            font-size: 0.9em;
            color: #666; /* Slightly darker details */
            margin-bottom: 5px; /* Reduced bottom margin */
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Page Setup ---
    # Make sure this path is correct relative to where you run streamlit
    image_path = "streamlit_app/assets/wallpaper.jpg"
    st.markdown(get_image_html(image_path), unsafe_allow_html=True)
    st.title("Add Watched Anime") # Using your title
    st.write("Search and log your watched anime.")

    # --- Initialize Session State Variables ---
    # For storing the list of results from API
    if "search_results" not in st.session_state:
        st.session_state.search_results = None
    # For storing the anime dictionary selected by the user
    if "selected_anime" not in st.session_state:
        st.session_state.selected_anime = None
     # To control whether the search results section is visible
    if "show_search_results" not in st.session_state:
        st.session_state.show_search_results = False
    # Flag to signal clearing the input box on the next run
    if "clear_search_input_on_next_run" not in st.session_state:
         st.session_state.clear_search_input_on_next_run = False
    # Initialize the input state key if it doesn't exist
    if "anime_title_input" not in st.session_state:
        st.session_state.anime_title_input = ""


    # --- Check Flag and Clear Input State BEFORE Widget Instantiation ---
    if st.session_state.get("clear_search_input_on_next_run", False):
        st.session_state.anime_title_input = ""  # Clear the state value
        st.session_state.clear_search_input_on_next_run = False # Reset the flag


    # --- Search Input Widget ---
    # Reads initial value from st.session_state.anime_title_input
    anime_title_from_input = st.text_input(
        "Search Anime Title",
        key="anime_title_input"
    )

    # --- Search and Clear Buttons ---
    col_search, col_clear = st.columns([1, 1]) # Using col_clear now

    with col_search:
        if st.button("Search"):
            if anime_title_from_input: # Check if input is not empty
                with st.spinner("Searching..."):
                    query = anime_title_from_input.strip()
                    # Fetch multiple results (changed limit=1 to limit=5)
                    search_url = f"https://api.jikan.moe/v4/anime?q={query}&limit=8&sfw"
                    try:
                        response = requests.get(search_url, timeout=10) # Added timeout
                        # Use a shorter sleep, Jikan's rate limit is usually per second
                        time.sleep(0.5)

                        if response.status_code == 200:
                            # Check if 'data' key exists and is a list
                            data = response.json().get("data", [])
                            if isinstance(data, list) and data:
                                st.session_state.search_results = data
                                st.session_state.selected_anime = None # Clear previous selection
                                st.session_state.show_search_results = True # Show results list
                            else:
                                st.warning("Anime not found. Try another title.")
                                st.session_state.search_results = None
                                st.session_state.selected_anime = None
                                st.session_state.show_search_results = False
                        else:
                            st.error(f"API Error: Status Code {response.status_code}")
                            # Clear state on API error
                            st.session_state.search_results = None
                            st.session_state.selected_anime = None
                            st.session_state.show_search_results = False

                    except requests.exceptions.RequestException as e:
                        st.error(f"Network error: {e}")
                        # Clear state on network error
                        st.session_state.search_results = None
                        st.session_state.selected_anime = None
                        st.session_state.show_search_results = False
            else:
                st.warning("Please enter an anime title to search.")

    # --- Display Search Results (if available and nothing selected yet) ---
    if st.session_state.show_search_results and st.session_state.search_results and not st.session_state.selected_anime:
        st.divider()
        st.subheader("Search Results:")
        # Loop through the results stored in session state
        for i, anime_result in enumerate(st.session_state.search_results):
            # Safely get data with .get()
            title = anime_result.get("title", "N/A")
            mal_id = anime_result.get("mal_id") # Needed for unique key
            image_url = anime_result.get("images", {}).get("jpg", {}).get("image_url", "https://via.placeholder.com/100x150?text=No+Image")
            year = anime_result.get("year", "N/A")
            anime_type = anime_result.get("type", "N/A")
            synopsis = anime_result.get("synopsis", "No synopsis available.")
            # Truncate synopsis if needed
            if synopsis and len(synopsis) > 150:
                 synopsis = synopsis[:150] + "..."

            # Use columns inside a container for each result
            with st.container():
                 st.markdown('<div class="search-result-item">', unsafe_allow_html=True) # Start item container
                 col_img, col_details = st.columns([1, 4]) # Image column, Details column

                 with col_img:
                      st.markdown(f'<img src="{image_url}" class="anime-pic">', unsafe_allow_html=True)

                 with col_details:
                      st.markdown(f'<div class="search-result-details">', unsafe_allow_html=True) # Start details container
                      st.markdown(f"<h4>{title}</h4>", unsafe_allow_html=True) # Use h4 for title
                      st.markdown(f"<p>Type: {anime_type}, Year: {year}</p>", unsafe_allow_html=True)
                      st.markdown(f"<p>{synopsis}</p>", unsafe_allow_html=True) # Show short synopsis

                      # Unique key for each button is essential
                      button_key = f"select_{mal_id}_{i}"
                      if st.button("Add to my list", key=button_key):
                           st.session_state.selected_anime = anime_result # Store the chosen anime
                           st.session_state.show_search_results = False # Hide the results list
                           st.rerun() # Rerun to show the selected anime details/form
                      st.markdown('</div>', unsafe_allow_html=True) # End details container

                 st.markdown('</div>', unsafe_allow_html=True) # End item container
            st.markdown("---") # Separator between results

    # --- Display Selected Anime Details and Add Form (if an anime is selected) ---
    if st.session_state.selected_anime:
        st.divider() # Visual separator
        st.subheader("Selected Anime Details:")
        anime = st.session_state.selected_anime # Get selected anime data

        # Extract data from selected anime (using .get for safety)
        title = anime.get("title", "N/A")
        genres_list = anime.get("genres", [])
        genres = ", ".join([g.get("name", "N/A") for g in genres_list]) if genres_list else "N/A"
        total_eps = anime.get("episodes") # Can be None
        rating = anime.get("score", 0.0)
        year = anime.get("year", "Unknown")
        image_url = anime.get("images", {}).get("jpg", {}).get("image_url", "https://via.placeholder.com/200x200?text=No+Image")

        # Layout using columns inside the info-box
        with st.markdown('<div class="info-box">', unsafe_allow_html=True):
            col_img, col_info = st.columns([1, 3]) # Adjust ratio as needed

            with col_img:
                st.markdown(f"""
                    <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
                        <img src="{image_url}" class="anime-pic-in-info">
                    </div>
                """, unsafe_allow_html=True)

            with col_info:
                st.markdown(f"""
                    <h3>📺 Anime Information</h3>
                    <p><strong>Title:</strong> {title}</p>
                    <p><strong>Genres:</strong> {genres}</p>
                    <p><strong>Total Episodes:</strong> {total_eps if total_eps else 'Unknown'}</p>
                    <p><strong>Rating (MAL):</strong> {rating if rating else 'N/A'}</p>
                    <p><strong>Year:</strong> {year}</p>
                """, unsafe_allow_html=True)

        # --- Add Anime Form ---
        st.subheader("Add to Your List:")
        # Assume st.session_state.username is set correctly before this page loads
        current_username = st.session_state.username

        with st.form("add_anime_form", clear_on_submit=True): # clear_on_submit helps reset form fields
            # Handle cases where total_eps is None or 0
            max_episodes = total_eps if isinstance(total_eps, int) and total_eps > 0 else 5000 # Default max if unknown
            min_episodes = 0

            episodes_watched = st.number_input(
                "Episodes Watched",
                min_value=min_episodes,
                max_value=max_episodes,
                value=0, # Default value
                step=1
            )

            # Determine default status based on episodes watched
            default_status = "Watching" # Default status
            if isinstance(total_eps, int) and total_eps > 0 and episodes_watched >= total_eps:
                default_status = "Completed"
            elif episodes_watched == 0:
                default_status = "Plan to Watch" # If 0 episodes, default to Plan to Watch


            status_options = ["Watching", "Completed", "On-Hold", "Dropped", "Plan to Watch"]
            # Find the index of the default status to pre-select the selectbox
            # Use try-except in case default_status is not in status_options (unlikely with current logic but safe)
            try:
                default_index = status_options.index(default_status)
            except ValueError:
                 default_index = 0 # Default to the first option if status is unexpected


            status_selected = st.selectbox(
                "Status",
                status_options,
                index=default_index # Pre-select based on episodes watched
            )
            submitted = st.form_submit_button("Add to My Anime")

            if submitted:
                # Removed explicit login check here as per previous discussion
                try:
                    # Call your database function - **Using your return structure**
                    db_status, db_msg = user.add_anime(
                        current_username,
                        title, # Use title from selected anime
                        episodes_watched,
                        status_selected, # Use the selected status (which is pre-selected but can be changed)
                        genres if genres != "N/A" else "", # Pass cleaned genres
                        total_eps if total_eps else None, # Pass None if unknown
                        year if year != "Unknown" else None, # Pass None if unknown
                        rating if rating else None # Pass None if no rating
                    )
                except Exception as e:
                     st.error(f"Error interacting with database: {e}")
                     print(f"Database Interaction Error: {e}") # Log the error
                     db_status = False
                     db_msg = f"Database error: {e}"

                # Handle success/error based on db_status from your function
                if db_status:
                    st.success(f"'{title}' added to your list!") # Use standard success message or db_msg if preferred
                else:
                    # Show the error message returned by your add_anime function
                    st.error(db_msg if db_msg else "Failed to add anime.") # Display DB message

                # Common actions after submit (success or fail)
                time.sleep(2) # Pause for user to see message
                # Reset state for a new search
                st.session_state.selected_anime = None
                st.session_state.search_results = None
                st.session_state.show_search_results = False
                # Set the flag to clear input on the next run
                st.session_state.clear_search_input_on_next_run = True
                st.rerun() # Rerun to apply state changes

