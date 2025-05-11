import streamlit as st
import sys, os, io, base64
from collections import defaultdict
import pandas as pd
import plotly.express as px
from PIL import Image
import requests
import time
from database import user


def show_profile():

    # Find the user
    if "username" not in st.session_state or st.session_state.username is None:
        st.error("User not logged in. Please log in to view your profile.")
        return

    user_data = user.find_user(st.session_state.username)

    if user_data is None:
        st.error("User data not found. Please try logging in again.")
        return


    # Load the profile pic
    profile_pic_data = None
    if user_data and len(user_data) > 4 and user_data[4]:
        profile_pic_data = user_data[4]

    # If no profile pic data, try loading the blank one
    if profile_pic_data is None or profile_pic_data == b"":
        blank_profile_path = "streamlit_app/assets/profile_pics/blankprofile.png"
        if os.path.exists(blank_profile_path):
            try:
                with open(blank_profile_path, "rb") as f:
                    profile_pic_data = f.read()
            except Exception as e:
                st.warning(f"Could not load blank profile picture: {e}")
                profile_pic_data = b""
        else:
            st.warning(f"Blank profile picture not found at {blank_profile_path}")
            profile_pic_data = b""


    # Convert image to base64 for HTML embedding
    img_base64 = ""
    if profile_pic_data and profile_pic_data != b"":
        try:
            img_base64 = base64.b64encode(profile_pic_data).decode()
        except Exception as e:
            st.error(f"Error encoding profile picture for display: {e}")
            img_base64 = ""


    # CSS styling for the profile image, watched anime list, and update controls
    st.markdown("""
        <style>
        .profile-pic {
            width: 200px;
            height: 200px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid #4F8BF9;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            margin-bottom: 10px;
        }
        .profile-pic:hover {
            transform: scale(1.05);
            transition: transform 0.2s;
        }
        .profile-box{
            background-color: #1f1f2e;
            padding: 20px;
            border-radius: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-top: 10px;
             color: white;
        }
        .profile-box h3 {
             color: #fce4ec;
             margin-top: 0;
             margin-bottom: 15px;
        }
        .profile-box p strong {
             color: #fce4ec;
        }
        .centered {
            display: flex;
            justify-content: center;
        }
        /* Style for anime list items */
        .anime-list-item {
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            display: flex;
            align-items: flex-start;
            background-color: #fce4ec;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
         .anime-list-item:hover {
             background-color: #f0f0f0;
         }
        .anime-list-image {
            height: 300px;
            border-radius: 10px;
            object-fit: cover;
            margin-right: 15px;
            margin-top: 10px;
            vertical-align: top;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .anime-list-details {
            flex-grow: 1;
            color: #333;
        }
        .anime-list-details h4 {
            margin-top: 0;
            margin-bottom: 5px;
            color: #1f1f2e;
        }
        .anime-list-details p {
            font-size: 0.9em;
            color: #555;
            margin-bottom: 3px;
        }
        /* Style for the update progress section */
        .update-progress-section {
            padding: 10px;
            border-radius: 8px;
            margin-top: 0px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
         .update-progress-section h5 {
             color: #1f1f2e;
             margin-top: 0;
             margin-bottom: 10px;
         }

        .stSelectbox label {
            font-size: 1.1em; /* Increase label font size */
            font-weight: bold; /* Make labels bold for prominence */
            color: #fce4ec; /* Optional: Match your theme's accent color */
        }

        /* Target the container that displays the selected value */
        /* This selector targets the div within the selectbox that shows the currently chosen option */
        /* You might need to inspect the HTML in your browser's developer tools if this selector doesn't work */
        .stSelectbox div[data-baseweb="select"] > div:first-child {
             font-size: 1.1em; /* Increase font size of the selected value */
             /* You can add other styles here like color if needed */
        }
        .anime-list-item .stButton button[key^="delete_btn_"]:hover {
            background-color: #d32f2f;
            color: white !important;
        }

        /* Adjust styling for Streamlit number input within the update column */
         .anime-list-item .stNumberInput {
             margin-bottom: 10px;
         }

         /* Adjust styling for Streamlit update button within the update column */
         .anime-list-item .stButton button[key^="update_btn_"] {
              background-color: #4CAF50;
              color: white !important;
              font-weight: bold;
              padding: 8px 15px;
              border-radius: 5px;
              border: none;
              transition: background-color 0.3s ease;
              margin-top: 5px;
              width: 100%;
              display: inline-block;
              text-align: center;
         }
         .anime-list-item .stButton button[key^="update_btn_"]:hover {
             background-color: #45a049;
             color: white !important;
         }

        </style>
    """, unsafe_allow_html=True)

    # Display profile picture and info side by side
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        # Display profile picture or placeholder
        if img_base64:
             st.markdown(f"""
                 <div class="centered">
                     <img src="data:image/png;base64,{img_base64}" class="profile-pic" alt="Profile Picture">
                 </div>
             """, unsafe_allow_html=True)
        else:
             st.markdown(f"""
                 <div class="centered">
                     <div style="width: 200px; height: 200px; border-radius: 50%; background-color: grey; display: flex; align-items: center; justify-content: center; color: white; font-size: 1em;">No Pic</div>
                 </div>
             """, unsafe_allow_html=True)


    with col2:
        st.markdown("""
            <div class="profile-box">
                <h3>👤 Profile Information</h3>
                <p><strong>Username:</strong> {}</p>
                <p><strong>Email:</strong> {}</p>
            </div>
        """.format(user_data[1], user_data[2]), unsafe_allow_html=True)

    # Section for profile actions
    st.markdown("---")
    options = ["Change Profile Picture", "My Anime Lists", "My Stats"]
    selected_option = st.selectbox(
        "Select Action:",
        options,
        index=0,
        placeholder="Select an option"
    )

    if selected_option == "Change Profile Picture":
        st.subheader("Update Profile Picture")
        uploaded_pic = st.file_uploader("Upload a new profile picture", type=["jpg", "jpeg", "png"])

        if uploaded_pic:
            if st.button("Confirm Update"):
                uploaded_file_bytes = uploaded_pic.read()
                user.add_profile_pic(st.session_state.username, uploaded_file_bytes)
                st.success("Profile picture updated successfully!")
                time.sleep(0.2)
                st.rerun()

    elif selected_option == "My Anime Lists":
        st.subheader("Your Anime Lists")

        # Use a selectbox to choose the list type (Watching, Completed, Plan to Watch)
        list_type = st.selectbox("Select List Type:", ["Watching", "Completed", "On-Hold", "Dropped", "Plan to Watch"], key="anime_list_type_select")

        anime_list = []
        # Fetch anime based on the selected list type
        if list_type == "Watching":
            anime_list = user.get_watching_anime(st.session_state.username)
        elif list_type == "Completed":
            anime_list = user.get_watched_anime(st.session_state.username)
        elif list_type == "Plan to Watch":
             anime_list = user.get_planned_anime(st.session_state.username)


        st.write(f"### {list_type} Anime")

        if anime_list:
            # Use a container for the list itself.
            with st.container():
                for i, anime in enumerate(anime_list):
                    # Safely extract data using indices
                    try:
                        # Assuming the order matches your user_anime table columns for these specific functions:
                        # (id, username, anime_title, episodes_watched, status, genre, total_episodes, year, rating, added_at)
                        anime_id = anime[0]
                        title = anime[2]
                        current_episodes_watched = anime[3]
                        status = anime[4]
                        genre = anime[5] if len(anime) > 5 and anime[5] is not None else "N/A"
                        total_episodes = anime[6] if len(anime) > 6 and anime[6] is not None else None
                        year = anime[7] if len(anime) > 7 and anime[7] is not None else "N/A"
                        rating = anime[8] if len(anime) > 8 and anime[8] is not None else None

                    except IndexError:
                        st.error(f"Error: Database row structure unexpected for anime {i}. Skipping display for this item.")
                        continue


                    # --- Fetch anime details from Jikan API for image ---
                    search_url = f"https://api.jikan.moe/v4/anime?q={requests.utils.quote(title)}&limit=1&sfw"
                    image_url = "https://via.placeholder.com/150x200?text=No+Image"

                    try:
                        response = requests.get(search_url, timeout=5)
                        time.sleep(0.2)

                        if response.status_code == 200:
                            data = response.json().get("data", [])
                            if isinstance(data, list) and data:
                                found_image_url = data[0].get("images", {}).get("jpg", {}).get("image_url")
                                if not found_image_url:
                                     found_image_url = data[0].get("images", {}).get("jpg", {}).get("small_image_url")

                                if found_image_url:
                                     image_url = found_image_url
                                else:
                                     st.warning(f"Image URL not found in Jikan API response for '{title}'.")
                            else:
                                 st.info(f"No detailed anime data found on Jikan for title: '{title}'. Displaying basic info from your list.", icon="🔍")

                        elif response.status_code == 429:
                             st.warning(f"Rate limited by Jikan API while fetching image for '{title}'. Please wait a moment and try again.", icon="⏳")
                             image_url = "https://via.placeholder.com/150x200?text=Rate+Limited"

                        else:
                            st.warning(f"Could not fetch image for '{title}' from Jikan API. Status: {response.status_code}", icon="⚠️")


                    except requests.exceptions.RequestException as e:
                         st.warning(f"Network error fetching image for '{title}': {e}", icon="❌")
                    except KeyError:
                        st.warning(f"Unexpected data structure in Jikan API response for '{title}'.", icon="⚠️")
                    except Exception as e:
                         st.warning(f"An unexpected error occurred fetching image for '{title}': {e}", icon="❗")


                    # --- Display each anime item ---
                    st.markdown('<div class="anime-list-item">', unsafe_allow_html=True)
                    # Adjust column ratios based on whether update controls are shown
                    if list_type == "Watching":
                         col_img, col_details, col_update = st.columns([1, 3, 1.5])
                    else:
                         col_img, col_details = st.columns([1, 4])


                    with col_img:
                        st.markdown(f'<img src="{image_url}" class="anime-list-image" alt="{title} thumbnail">', unsafe_allow_html=True)


                    with col_details:
                        st.markdown(f'<div class="anime-list-details">', unsafe_allow_html=True)
                        st.markdown(f"<h4>{title}</h4>", unsafe_allow_html=True)
                        st.markdown(f"<p><strong>Status:</strong> {status}</p>", unsafe_allow_html=True)

                        # Only show episodes watched if it's a Watching or Completed list
                        if list_type in ["Watching", "Completed", "On-Hold", "Dropped"]:
                             episodes_display = f"{current_episodes_watched}"
                             if total_episodes is not None and total_episodes > 0:
                                 episodes_display += f" / {total_episodes}"
                             st.markdown(f"<p><strong>Episodes:</strong> {episodes_display}</p>", unsafe_allow_html=True)

                        # Display other details
                        if genre != "N/A":
                            st.markdown(f"<p><strong>Genre:</strong> {genre}</p>", unsafe_allow_html=True)
                        if year != "N/A":
                            st.markdown(f"<p><strong>Year:</strong> {year}</p>", unsafe_allow_html=True)
                        if rating is not None and rating > 0:
                             st.markdown(f"<p><strong>Rating (MAL):</strong> {rating}</p>", unsafe_allow_html=True)

                        st.markdown('</div>', unsafe_allow_html=True)


                    # --- Conditional Update and Delete Controls (Only for "Watching" list) ---
                    if list_type == "Watching":
                         with col_update:
                              st.markdown("<h5>Update Progress</h5>", unsafe_allow_html=True)
                              update_key = f"ep_input_{anime_id}_{list_type}"
                              current_episodes_watched_safe = current_episodes_watched if current_episodes_watched is not None else 0

                              new_episodes = st.number_input(
                                  "Episodes",
                                  min_value=0,
                                  max_value=total_episodes if isinstance(total_episodes, int) and total_episodes is not None and total_episodes > 0 else 5000,
                                  value=current_episodes_watched_safe,
                                  step=1,
                                  key=update_key
                              )

                              update_button_key = f"update_btn_{anime_id}_{list_type}"
                              update_button = st.button("Update", key=update_button_key)

                              if update_button:
                                   new_status = status

                                   if isinstance(total_episodes, int) and total_episodes is not None and total_episodes > 0 and new_episodes >= total_episodes:
                                       new_status = "Completed"
                                   elif new_episodes > 0 and status == "Plan to Watch":
                                       new_status = "Watching"
                                   elif new_episodes > 0 and status == "Completed":
                                       if isinstance(total_episodes, int) and total_episodes is not None and total_episodes > 0 and new_episodes < total_episodes:
                                           new_status = "Watching"
                                   elif new_episodes == 0 and status != "Plan to Watch":
                                        pass

                                   success, message = user.update_watched_anime(
                                       st.session_state.username,
                                       title,
                                       new_episodes,
                                       new_status
                                   )

                                   if success:
                                       st.success(f"Updated progress for '{title}' to {new_episodes} episodes. Status: {new_status}.", icon="✅")
                                       st.rerun()
                                   else:
                                       st.error(f"Failed to update progress for '{title}': {message}", icon="❌")

                              # --- Add the Delete button ---
                              delete_button_key = f"delete_btn_{anime_id}_{list_type}"
                              delete_button = st.button("Drop Anime", key=delete_button_key)

                              if delete_button:
                                   success, message = user.delete_user_anime(st.session_state.username, title)

                                   if success:
                                       st.success(f"Removed '{title}' from your list.", icon="🗑️")
                                       st.rerun()
                                   else:
                                       st.error(f"Failed to remove '{title}': {message}", icon="❌")


                    st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown("---")

        else:
            st.info(f"No {list_type.lower()} anime found in your list.", icon="ℹ️")

    # --- My Stats Section ---
    elif selected_option == "My Stats":
        st.subheader("📊 Your Anime Stats")

        with st.spinner("Loading your stats..."):
            # Fetch all user anime data
            # IMPORTANT: Verify that your get_all_anime function in database.py
            # returns the columns in the order (anime_title, episodes_watched, genre, ...)
            user_anime_data_for_stats = user.get_all_anime(st.session_state.username)


            if user_anime_data_for_stats:
                genres = defaultdict(int)
                total_episodes_watched = 0
                total_anime_count = len(user_anime_data_for_stats)


                for anime_entry in user_anime_data_for_stats:
                    # Accessing title (index 0), episodes_watched (index 1), and genre (index 2)
                    # Adjust indices if your get_all_anime returns a different format!
                    try:
                        title_for_stats = anime_entry[0] if len(anime_entry) > 0 else "Unknown Title"
                        episodes_watched = anime_entry[1] if len(anime_entry) > 1 and isinstance(anime_entry[1], (int, float)) else 0
                        genre_string = anime_entry[2] if len(anime_entry) > 2 and anime_entry[2] is not None else ""

                    except IndexError:
                        st.error(f"Error processing anime data for stats. Row structure unexpected: {anime_entry}. Skipping.")
                        continue


                    # Process genres
                    if genre_string:
                         genre_list = [g.strip() for g in genre_string.split(",") if g.strip()]
                         for genre in genre_list:
                             genres[genre] += 1

                    # Sum episodes watched
                    total_episodes_watched += episodes_watched


                # store the data in a dataframe for plotting
                genre_df = pd.DataFrame(list(genres.items()), columns=["Genre", "Count"])
                genre_df = genre_df[genre_df["Count"] > 0].sort_values(by="Count", ascending=False)


                # --- Display Stats Summary and Chart ---
                # Make sure your CSS for stat-metric-box and chart-container is included
                st.markdown("""
                    <style>
                    /* Your existing CSS for profile pic, profile box, anime list items, update/delete controls */
                    /* ... (keep all the CSS from your previous profile.py code here) ... */

                    /* New CSS for the Stats Section */
                    .stat-metric-box {
                        background-color: #2c2c3d;
                        color: white;
                        padding: 15px;
                        border-radius: 10px;
                        margin-bottom: 15px;
                        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                        text-align: center;
                    }
                    .stat-metric-box h4 {
                        color: #fce4ec;
                        margin-top: 0;
                        margin-bottom: 5px;
                        font-size: 1.1em;
                    }
                    .stat-metric-box h5 {
                        color: aliceblue;
                        margin-top: 0;
                        font-size: 1.4em;
                        font-weight: bold;
                    }
                    .chart-container {
                         background-color: #2c2c3d;
                         padding: 15px;
                         border-radius: 10px;
                         box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                         margin-top: 20px;
                    }
                    .chart-container h3 {
                        color: #fce4ec;
                        margin-top: 0;
                        margin-bottom: 15px;
                        text-align: center;
                    }
                    </style>
                """, unsafe_allow_html=True)


                # Display total episodes watched and total anime watched in columns
                col_stats1, col_stats2 = st.columns(2)
                with col_stats1:
                    st.markdown(f"""
                        <div class="stat-metric-box">
                            <h4>Total Episodes Watched</h4>
                            <h5>{total_episodes_watched}</h5>
                        </div>
                    """, unsafe_allow_html=True)
                with col_stats2:
                    st.markdown(f"""
                        <div class="stat-metric-box">
                            <h4>Total Anime Entries</h4>
                            <h5>{total_anime_count}</h5>
                        </div>
                    """, unsafe_allow_html=True)


                # Display the genre distribution chart in a styled container
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                st.markdown("<h3>Anime Genre Distribution</h3>", unsafe_allow_html=True)

                if not genre_df.empty:
                    fig = px.bar(
                        genre_df,
                        x="Genre",
                        y="Count",
                        color="Genre",
                        labels={"Genre": "Genre", "Count": "Number of Anime"},
                        template="plotly_dark",
                    )
                    fig.update_layout(
                        xaxis={'categoryorder':'total descending'},
                        margin=dict(l=20, r=20, t=10, b=20),
                        plot_bgcolor="#2c2c3d",
                        paper_bgcolor="#2c2c3d",
                        font_color="white"
                    )
                    fig.update_xaxes(tickangle=45, tickfont=dict(size=10))


                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No genre data available to display chart. Add some anime with genre information to see the distribution.", icon="ℹ️")


                st.markdown("</div>", unsafe_allow_html=True)


            else:
                st.warning("No anime data found for your account to generate stats. Add some anime to your list!", icon="⚠️")