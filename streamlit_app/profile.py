import streamlit as st
import sys, os, io, base64
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

    # CSS styling for the profile image
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
    selected_option = selected_option = st.selectbox(
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
