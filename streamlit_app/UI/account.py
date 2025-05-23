import streamlit as st
import re
import os, sys, time

from database import user

user.create_table()


def my_account():
    st.markdown("""
        <style>
        .stApp h1 {
            color: #fce4ec; /* Accent color for main title */
            text-align: center;
            margin-bottom: 30px;
        }
        .stApp h2, .stApp h3 {
            color: #b3e5fc; /* Lighter accent color for subheaders */
            margin-bottom: 15px;
            border-bottom: 2px solid #2c2c3d; /* Subtle underline */
            padding-bottom: 5px;
        }
        .stTextInput > label, .stRadio > label {
            font-weight: bold;
            color: #fce4ec; /* Label color */
        }
         .stTextInput input[type="text"], .stTextInput input[type="password"] {
             background-color: #3a3a4e; /* Darker input background */
             color: white; /* Input text color */
             border: 1px solid #5a5a78; /* Input border */
             border-radius: 5px;
             padding: 10px;
         }
         .stButton > button {
             background-color: #4CAF50; /* Green primary button */
             color: white !important; /* Ensure text is white */
             font-weight: bold;
             padding: 10px 20px;
             border-radius: 5px;
             border: none;
             margin-top: 10px;
             transition: background-color 0.3s ease;
             cursor: pointer;
         }
         .stButton > button:hover {
             background-color: #45a049;
             color: white !important; /* Ensure text is white on hover */
         }
         /* Style for Delete button - targeted by key prefix */
         .stButton > button[key^="delete_account_button"] {
             background-color: #f44336; /* Red color for delete */
             color: white !important; /* Ensure text is white */
         }
          .stButton > button[key^="delete_account_button"]:hover {
              background-color: #d32f2f;
              color: white !important; /* Ensure text is white on hover */
          }


        /* Style for the radio menu when logged in */
        .stRadio > div > label {
            padding: 8px 0;
        }
        .stRadio div[data-baseweb="radio"] {
             background-color: #3a3a4e;
             border-radius: 5px;
             padding: 5px;
             margin-bottom: 5px;
             border: 1px solid #5a5a78;
        }
        .stRadio div[data-baseweb="radio"]:hover {
            background-color: #4a4a5e;
        }
        .stRadio div[data-baseweb="radio"][aria-checked="true"] {
            background-color: #4F8BF9;
            border-color: #4F8BF9;
        }

        </style>
    """, unsafe_allow_html=True)

    st.title("👤 My Account")

    if st.session_state.get("logged_in"):
        st.success(f"Welcome, {st.session_state.username}!")

        col1, col2 = st.columns([1, 3])
        with col1:
            st.subheader("Menu")
            menu_option = st.radio("Choose:", ["Change Email", "Change Password", "Delete Account", "Logout"], key="account_menu_radio")

        with col2:
            st.markdown('<div class="content-container">', unsafe_allow_html=True) # Container for the content area

            if menu_option == "Change Email":
                st.subheader("✉️ Change Email")
                new_email = st.text_input("Enter your new email", key="new_email_input")
                if st.button("Update Email", key="update_email_button"):
                    if not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
                        st.error("Invalid email format.")
                    elif user.find_email(new_email):
                        st.error("Email already exists.")
                    else:
                        user.update_email(st.session_state.username, new_email)
                        st.success("Email updated successfully!")

            elif menu_option == "Change Password":
                st.subheader("🔑 Change Password")
                current_pw = st.text_input("Current Password", type="password", key="current_pw_input")
                new_pw = st.text_input("New Password", type="password", key="new_pw_input")
                confirm_pw = st.text_input("Confirm New Password", type="password", key="confirm_pw_input")
                if st.button("Update Password", key="update_pw_button"):
                    data = user.find_user(st.session_state.username)
                    if data and data[3] != current_pw:
                        st.error("Incorrect current password.")
                    elif new_pw != confirm_pw:
                        st.error("Passwords do not match.")
                    elif len(new_pw) < 8 or not re.search(r"[A-Za-z]", new_pw) or not re.search(r"[0-9]", new_pw):
                        st.error("Password must be 8+ characters and include letters and numbers.")
                    else:
                        user.update_password(st.session_state.username, new_pw)
                        st.success("Password updated successfully!")

            elif menu_option == "Delete Account":
                st.subheader("⚠️ Delete Account")
                st.warning("This action is irreversible. Proceed with caution.")
                confirm = st.checkbox("I understand the consequences.", key="delete_confirm_checkbox")
                if st.button("Delete My Account", key="delete_account_button", help="Permanently delete your account"):
                    if confirm:
                         with st.spinner("Deleting account..."):
                             time.sleep(2)
                             delete_user_success, delete_user_message = user.delete_user(st.session_state.username)
                             if delete_user_success:
                                 delete_anime_success, delete_anime_message = user.delete_all_anime(st.session_state.username)
                                 if delete_anime_success:
                                      st.success("Account and all associated data deleted.")
                                      time.sleep(1)
                                      st.session_state.logged_in = False
                                      st.session_state.username = None
                                      st.rerun()
                                 else:
                                     st.error(f"Account deleted, but failed to delete associated anime data: {delete_anime_message}")
                             else:
                                st.error(f"Failed to delete account: {delete_user_message}")
                    else:
                         st.warning("Please confirm you understand the consequences.")


            elif menu_option == "Logout":
                st.subheader("🔒 Logout")
                st.write("Click the button below to log out.")
                if st.button("Logout", key="logout_button"):
                    with st.spinner("Logging out..."):
                        time.sleep(2)
                        st.session_state.logged_in = False
                        st.session_state.username = None
                        st.success("Logged out successfully.")
                        time.sleep(1)
                        st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)


    else: # Not logged in
        st.markdown('<div class="content-container">', unsafe_allow_html=True)

        option = st.radio("Choose an option:", ("Login", "Register"), key="login_register_radio")

        if option == "Login":
            st.subheader("🔐 Login")
            input_username = st.text_input("Username", key="login_username_input")
            input_password = st.text_input("Password", type="password", key="login_password_input")
            if st.button("Login", key="login_button"):
                if input_username and input_password:
                    user_data = user.find_user(input_username)
                    if user_data and user_data[1] == input_username and user_data[3] == input_password:
                        with st.spinner("Logging in..."):
                            time.sleep(2)
                            st.success("Login successful!")
                            st.session_state.logged_in = True
                            st.session_state.username = input_username
                            st.rerun()
                    else:
                        st.error("Invalid username or password.")
                else:
                     st.warning("Please enter username and password.")


        elif option == "Register":
            st.subheader("📝 Register")
            username = st.text_input("Username", key="register_username_input")
            email = st.text_input("Email", key="register_email_input")
            password = st.text_input("Password", type="password", key="register_password_input")
            confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm_password_input")

            if st.button("Register", key="register_button"):
                if not username or not email or not password:
                    st.error("Please fill in all fields.")
                elif user.find_user(username):
                    st.error("Username already exists. Please choose a different one.")
                elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    st.error("Invalid email format.")
                elif user.find_email(email):
                    st.error("Email already exists. Please choose a different one.")
                elif password != confirm_password:
                    st.error("Passwords do not match.")
                elif len(password) < 8 or not re.search(r"[A-Za-z]", password) or not re.search(r"[0-9]", password):
                    st.error("Password must be 8+ characters and contain both letters and numbers.")
                else:
                    add_user_success, add_user_message = user.add_user(username, email, password)
                    if add_user_success:
                         st.success("Registration successful! You can now login.")
                         time.sleep(1)
                         st.rerun()
                    else:
                         st.error(f"Registration failed: {add_user_message}")
        st.markdown('</div>', unsafe_allow_html=True)