import streamlit as st
import sys, os, io, base64
from PIL import Image
import requests
import time

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import database
from database import user


def show_profile():

    # Find the user
    user_data = user.find_user(st.session_state.username)

    # Load the profile pic
    if user_data and user_data[4]:
        profile_pic_data = user_data[4]
    else:
        with open("streamlit_app/assets/profile_pics/blankprofile.png", "rb") as f:
            profile_pic_data = f.read()

    # Convert image to base64 for HTML embedding
    img_base64 = base64.b64encode(profile_pic_data).decode()

    # CSS styling for the profile image and watched anime list
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
        /* Style for watched anime list items */
        .watched-anime-item {
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            display: flex;
            align-items: flex-start;
            background-color: #fce4ec;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        .watched-anime-image {
        height: 300px;
        border-radius: 10px;
        object-fit: cover;
        margin-right: 15px;
        margin-top: 10px;
        vertical-align: top; /* Align image with text */
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Subtle shadow */
        }
        .watched-anime-details {
            flex-grow: 1;
        }
        .watched-anime-details h4 {
            margin-top: 0;
            margin-bottom: 5px;
            color: #333;
        }
        .watched-anime-details p {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 3px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Display profile picture and info side by side
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.markdown(f"""
            <div class="centered">
                <img src="data:image/png;base64,{img_base64}" class="profile-pic">
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

    # Section to update profile picture
    st.markdown("---")
    options = ["Change Profile Picture", "Get Watched Anime", "Get Planned Anime"]
    selected_option = st.selectbox(
        " ",  # Hide label
        options,
        index=0,
        placeholder="Select an option"
    )

    if selected_option == "Change Profile Picture":
        st.subheader("Update Profile Picture")
        uploaded_pic = st.file_uploader("Upload a new profile picture", type=["jpg", "jpeg", "png"])

        if uploaded_pic:
            if st.button("Confirm Update"):
                user.add_profile_pic(st.session_state.username, uploaded_pic.read())
                st.success("Profile picture updated successfully!")
                st.rerun()

    elif selected_option == "Get Watched Anime":
        st.subheader("Watched Anime")
        watched_anime = user.get_watched_anime(st.session_state.username)
        if watched_anime:
            for anime in watched_anime:
                title = anime[2]
                episodes_watched = anime[3]
                status = anime[4]
                genre = anime[5]
                total_episodes = anime[6]
                year = anime[7]
                rating = anime[8]

                # Fetch anime details from Jikan API for image
                search_url = f"https://api.jikan.moe/v4/anime?q={title}&limit=1&sfw"
                try:
                    response = requests.get(search_url, timeout=10)
                    time.sleep(0.3)  # Be mindful of API rate limits
                    if response.status_code == 200:
                        data = response.json().get("data", [])
                        image_url = data[0].get("images", {}).get("jpg", {}).get("image_url", "https://via.placeholder.com/80x120?text=No+Image") if data else "https://via.placeholder.com/80x120?text=No+Image"
                    else:
                        image_url = "https://via.placeholder.com/80x120?text=No+Image"
                except requests.exceptions.RequestException as e:
                    st.error(f"Error fetching image for {title}: {e}")
                    image_url = "https://via.placeholder.com/80x120?text=No+Image"

                with st.container():
                    st.markdown('<div class="watched-anime-item">', unsafe_allow_html=True)
                    col_img, col_details = st.columns([1, 4])

                    with col_img:
                        st.markdown(f'<img src="{image_url}" class="watched-anime-image">', unsafe_allow_html=True)

                    with col_details:
                        st.markdown(f'<div class="watched-anime-details">', unsafe_allow_html=True)
                        st.markdown(f"<h4>{title}</h4>", unsafe_allow_html=True)
                        st.markdown(f"<p><strong>Status:</strong> {status}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p><strong>Episodes Watched:</strong> {episodes_watched}{f'/{total_episodes}' if total_episodes else ''}</p>", unsafe_allow_html=True)
                        if genre:
                            st.markdown(f"<p><strong>Genre:</strong> {genre}</p>", unsafe_allow_html=True)
                        if year:
                            st.markdown(f"<p><strong>Year:</strong> {year}</p>", unsafe_allow_html=True)
                        if rating:
                            st.markdown(f"<p><strong>Rating:</strong> {rating}</p>", unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("---")
        else:
            st.info("No watched anime found.")

    elif selected_option == "Get Planned Anime":
        st.subheader("Planned Anime")
        planned_anime = user.get_planned_anime(st.session_state.username)
        if planned_anime:
            for anime in planned_anime:
                st.write(f"**Title:** {anime[2]}")
                st.write(f"**Genre:** {anime[5]}")
                st.write(f"**Total Episodes:** {anime[6]}")
                st.write(f"**Year of Release:** {anime[7]}")
                st.write(f"**Rating:** {anime[8]}")
                st.markdown("---")
        else:
            st.info("No planned anime found.")