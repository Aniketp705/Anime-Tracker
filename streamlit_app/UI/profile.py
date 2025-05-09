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
    # Ensure st.session_state.username is set correctly before this page loads
    if "username" not in st.session_state or st.session_state.username is None:
        st.error("User not logged in. Please log in to view your profile.")
        return # Exit the function if user is not logged in

    user_data = user.find_user(st.session_state.username)

    if user_data is None:
        st.error("User data not found. Please try logging in again.")
        # Consider adding a logout action here
        return


    # Load the profile pic
    # Assuming user_data[4] is the profile picture data (BLOB)
    profile_pic_data = None
    if user_data and user_data[4]:
        profile_pic_data = user_data[4]

    # If no profile pic data, try loading the blank one
    if profile_pic_data is None:
        blank_profile_path = "streamlit_app/assets/profile_pics/blankprofile.png"
        if os.path.exists(blank_profile_path):
            try:
                with open(blank_profile_path, "rb") as f:
                    profile_pic_data = f.read()
            except Exception as e:
                st.warning(f"Could not load blank profile picture: {e}")
                profile_pic_data = b"" # Use empty bytes on error
        else:
            st.warning(f"Blank profile picture not found at {blank_profile_path}")
            profile_pic_data = b"" # Use empty bytes if file not found


    # Convert image to base64 for HTML embedding
    img_base64 = ""
    if profile_pic_data:
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
        }
        .centered {
            display: flex;
            justify-content: center;
        }
        /* Style for anime list items (used for Watching, Completed, Planned) */
        .anime-list-item {
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            display: flex;
            align-items: flex-start;
            background-color: #fce4ec; /* Light pink background */
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
         .anime-list-item:hover {
             background-color: #f0f0f0; /* Slightly lighter on hover */
         }
        .anime-list-image {
            height: 300px; /* Keep your desired height */
            border-radius: 10px;
            object-fit: cover;
            margin-right: 15px;
            margin-top: 10px;
            vertical-align: top; /* Align image with text */
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Subtle shadow */
        }
        .anime-list-details {
            flex-grow: 1;
            color: #333; /* Darker text for readability on light background */
        }
        .anime-list-details h4 {
            margin-top: 0;
            margin-bottom: 5px;
            color: #1f1f2e; /* Darker title */
        }
        .anime-list-details p {
            font-size: 0.9em;
            color: #555; /* Slightly darker details */
            margin-bottom: 3px;
        }
         /* Style for the update progress section */
        .update-progress-section {
            background-color: #ffffff; /* White background */
            padding: 10px;
            border-radius: 8px;
            margin-top: 10px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
         .update-progress-section h5 {
             color: #1f1f2e; /* Dark title for update section */
             margin-top: 0;
             margin-bottom: 10px;
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
    # Consolidating watched/planned/watching under "My Anime Lists"
    options = ["Change Profile Picture", "My Anime Lists", "My Stats"] # Removed "Get Watched Anime", "Get Planned Anime"
    selected_option = st.selectbox(
        "Select Action:",  # Added a clearer label
        options,
        index=0,
        placeholder="Select an option"
    )

    if selected_option == "Change Profile Picture":
        st.subheader("Update Profile Picture")
        uploaded_pic = st.file_uploader("Upload a new profile picture", type=["jpg", "jpeg", "png"])

        if uploaded_pic:
            if st.button("Confirm Update"):
                # Read the uploaded file content
                uploaded_file_bytes = uploaded_pic.read()
                # Assuming add_profile_pic handles the database update
                user.add_profile_pic(st.session_state.username, uploaded_file_bytes)
                st.success("Profile picture updated successfully!")
                time.sleep(0.2)
                st.rerun() # Rerun to display the new picture

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
        # Add conditions for "On-Hold" and "Dropped" if you have corresponding DB functions
        # elif list_type == "On-Hold":
        #      anime_list = user.get_on_hold_anime(st.session_state.username)
        # elif list_type == "Dropped":
        #      anime_list = user.get_dropped_anime(st.session_state.username)


        st.write(f"### {list_type} Anime") # Dynamic subheader for the list

        if anime_list:
            # Use a container for the list itself. No key needed for this container in older Streamlit.
            with st.container():
                for i, anime in enumerate(anime_list):
                    # Safely extract data using indices, check your database schema
                    try:
                        # Assuming the order matches your user_anime table columns:
                        # (id, username, anime_title, episodes_watched, status, genre, total_episodes, year, rating, added_at)
                        # Adjust indices if your table structure is different
                        anime_id = anime[0]
                        title = anime[2]
                        current_episodes_watched = anime[3]
                        status = anime[4] # This will be the status for the current list type (e.g., 'Watching', 'Completed')
                        genre = anime[5] if len(anime) > 5 and anime[5] is not None else "N/A"
                        total_episodes = anime[6] if len(anime) > 6 and anime[6] is not None else None
                        year = anime[7] if len(anime) > 7 and anime[7] is not None else "N/A"
                        rating = anime[8] if len(anime) > 8 and anime[8] is not None else None

                    except IndexError:
                        st.error(f"Error: Database row structure unexpected for anime {i}. Skipping display for this item.")
                        continue # Skip this anime if data structure is wrong


                    # --- Fetch anime details from Jikan API for image ---
                    # Use the title from the database to search Jikan
                    # Use requests.utils.quote to handle special characters in the title
                    search_url = f"https://api.jikan.moe/v4/anime?q={requests.utils.quote(title)}&limit=1&sfw"
                    image_url = "https://via.placeholder.com/150x200?text=No+Image" # Default placeholder image

                    try:
                        # Use a shorter timeout for quicker response or failure
                        response = requests.get(search_url, timeout=5)
                        # Add a small delay to respect API rate limits, especially in a loop
                        time.sleep(0.2) # Reduced sleep slightly, adjust if rate limited

                        if response.status_code == 200:
                            data = response.json().get("data", [])
                            if isinstance(data, list) and data:
                                # Get the image URL from the first result
                                # Using image_url for potentially higher res, fallback to small_image_url if needed
                                found_image_url = data[0].get("images", {}).get("jpg", {}).get("image_url")
                                if not found_image_url:
                                     found_image_url = data[0].get("images", {}).get("jpg", {}).get("small_image_url")

                                if found_image_url:
                                     image_url = found_image_url
                                else:
                                     st.warning(f"Image URL not found in Jikan API response for '{title}'.")
                            else:
                                # No results found for the title
                                st.info(f"No detailed anime data found on Jikan for title: '{title}'. Displaying basic info from your list.", icon="🔍")


                        elif response.status_code == 429:
                             st.warning(f"Rate limited by Jikan API while fetching image for '{title}'. Please wait a moment and try again.", icon="⏳")
                             # Consider adding more robust rate limit handling if this is common
                             image_url = "https://via.placeholder.com/150x200?text=Rate+Limited"

                        else:
                            st.warning(f"Could not fetch image for '{title}' from Jikan API. Status: {response.status_code}", icon="⚠️")
                            # Log the error response content for debugging if needed
                            # print(f"Jikan API Error Response for '{title}': {response.text}")


                    except requests.exceptions.RequestException as e:
                         st.warning(f"Network error fetching image for '{title}': {e}", icon="❌")
                    except KeyError:
                        st.warning(f"Unexpected data structure in Jikan API response for '{title}'.", icon="⚠️")
                    except Exception as e:
                         st.warning(f"An unexpected error occurred fetching image for '{title}': {e}", icon="❗")


                    # --- Display each anime item ---
                    st.markdown('<div class="anime-list-item">', unsafe_allow_html=True) # Using general anime-list-item class
                    # Adjust column ratios based on whether update controls are shown
                    if list_type == "Watching":
                         # Columns for [image, details, update controls]
                         col_img, col_details, col_update = st.columns([1, 3, 1.5])
                    else:
                         # Columns for [image, details] - no update column for Completed/Planned/etc.
                         col_img, col_details = st.columns([1, 4])


                    with col_img:
                        # Display the anime image
                        st.markdown(f'<img src="{image_url}" class="anime-list-image" alt="{title} thumbnail">', unsafe_allow_html=True)


                    with col_details:
                        st.markdown(f'<div class="anime-list-details">', unsafe_allow_html=True)
                        st.markdown(f"<h4>{title}</h4>", unsafe_allow_html=True)
                        st.markdown(f"<p><strong>Status:</strong> {status}</p>", unsafe_allow_html=True)

                        # Only show episodes watched if it's a Watching or Completed list
                        if list_type in ["Watching", "Completed", "On-Hold", "Dropped"]: # Display episodes for statuses that track progress
                             episodes_display = f"{current_episodes_watched}"
                             if total_episodes is not None and total_episodes > 0:
                                 episodes_display += f" / {total_episodes}"
                             st.markdown(f"<p><strong>Episodes:</strong> {episodes_display}</p>", unsafe_allow_html=True)

                        # Display other details
                        if genre != "N/A":
                            st.markdown(f"<p><strong>Genre:</strong> {genre}</p>", unsafe_allow_html=True)
                        if year != "N/A":
                            st.markdown(f"<p><strong>Year:</strong> {year}</p>", unsafe_allow_html=True)
                        # Display rating if available and greater than 0
                        if rating is not None and rating > 0:
                             st.markdown(f"<p><strong>Rating (MAL):</strong> {rating}</p>", unsafe_allow_html=True)

                        st.markdown('</div>', unsafe_allow_html=True) # End anime-list-details


                    # --- Conditional Update and Delete Controls (Only for "Watching" list) ---
                    if list_type == "Watching":
                         with col_update: # Column for update controls
                              st.markdown("<h5>Update Progress</h5>", unsafe_allow_html=True)
                              # Use a unique key based on anime_id and list type for uniqueness across reruns and items
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

                              # Use a unique key for the Update button
                              update_button_key = f"update_btn_{anime_id}_{list_type}"
                              update_button = st.button("Update", key=update_button_key)

                              # --- Handle update logic ---
                              if update_button:
                                   new_status = status # Start with the current status

                                   # Logic to determine new status when updating from "Watching"
                                   if isinstance(total_episodes, int) and total_episodes is not None and total_episodes > 0 and new_episodes >= total_episodes:
                                       new_status = "Completed"
                                   elif new_episodes > 0 and status == "Plan to Watch":
                                       new_status = "Watching"
                                   elif new_episodes > 0 and status == "Completed":
                                       if isinstance(total_episodes, int) and total_episodes is not None and total_episodes > 0 and new_episodes < total_episodes:
                                           new_status = "Watching"
                                   # If episodes become 0, user might intend to Plan to Watch or Drop, keep current status unless completed
                                   elif new_episodes == 0 and status != "Plan to Watch":
                                        pass # Keep status unless it was Plan to Watch

                                   # Call the database function to update the record
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
                              # Place it within the update column below the update button
                              delete_button_key = f"delete_btn_{anime_id}_{list_type}"
                              delete_button = st.button("Drop Anime", key=delete_button_key)

                              # --- Handle delete logic ---
                              if delete_button:
                                   # Call a delete function in database.py (you'll need to create this)
                                   # It's best to delete by a unique identifier like anime_id and username
                                   # Assuming user.delete_user_anime exists and takes (username, anime_id) or (username, anime_title)
                                   # Using anime_id is more reliable if titles aren't guaranteed unique per user
                                   # Assuming your delete function is user.delete_user_anime(username, anime_title) based on previous
                                   success, message = user.delete_user_anime(st.session_state.username, title) # Pass username and title

                                   if success:
                                       st.success(f"Removed '{title}' from your list.", icon="🗑️")
                                       st.rerun()
                                   else:
                                       st.error(f"Failed to remove '{title}': {message}", icon="❌")


                    st.markdown('</div>', unsafe_allow_html=True) # End anime-list-item container
                    st.markdown("---") # Separator between results

        else:
            st.info(f"No {list_type.lower()} anime found in your list.", icon="ℹ️")
    
    elif selected_option == "My Stats":
        st.subheader("📊 Your Anime Stats")

        # Fetch user anime data
        user_data = user.get_all_anime(st.session_state.username)

        # store genres in a dictionary
        genres = defaultdict(int)

        # user_data is a list of tuples (anime_title, episodes_watched, genre, added_at)
        for anime in user_data:
            genre_list = anime[2].split(",")
            for genre in genre_list:
                genres[genre.strip()] += 1

        # get total episodes watched
        total_episodes_watched = sum([anime[1] for anime in user_data ])
        # get total anime watched
        total_anime_watched = len(user_data)

        # store the data in a dataframe
        genre_df = pd.DataFrame(list(genres.items()), columns=["Genre", "Count"])
        genre_df = genre_df.sort_values(by="Count", ascending=False)

        if user_data:
            # total_watched = len(user_data)
            # genre_items = ""
            # for genre, count in genres.items():
            #     genre_items += f"<li>{genre}: {count}</li>"


            # st.markdown(f"""
            #     <div style='background-color:#1f1f2e; padding:20px; border-radius:10px; color:white;'>
            #         <h3>📈 Summary</h3>
            #         <h3><strong>Genres:</strong></h3>
            #         <ul style = padding-left: 20px;>
            #             {genre_items}
            #         </ul>
            #     </div>
            # """, unsafe_allow_html=True)

            # Plotting the genre distribution
            fig = px.bar(
                genre_df,
                x = "Genre",
                y = "Count",
                color = "Genre",
                title = "Anime Genre Distribution",
                labels = {"Genre": "Genre", "Count": "Number of Anime"},
                template = "plotly_dark",
            )
            st.plotly_chart(fig, use_container_width=True)

            # Display total episodes watched
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                    <div ">
                        <h5>Total Episodes Watched</h5>
                        <p>{total_episodes_watched}</p>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                    <div ">
                        <h5>Total Anime Watched</h5>
                        <p>{total_anime_watched}</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No anime data found for your account.")


