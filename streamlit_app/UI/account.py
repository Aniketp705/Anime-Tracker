import streamlit as st
import re
import os, sys, time

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import user

# Initialize the database
user.create_table()

st.markdown("""
        <style>
        .menu-box{
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


def my_account():
    st.title("👤 My Account")

    if st.session_state.get("logged_in"):
        st.success(f"Welcome, {st.session_state.username}!")

        col1, col2 = st.columns([1, 4])
        with col1:
            st.subheader("Menu")
            menu_option = st.radio("Choose:", ["Change Email", "Change Password", "Delete Account", "Logout"])
        
        with col2:
            if menu_option == "Change Email":
                st.subheader("✉️ Change Email")
                new_email = st.text_input("Enter your new email")
                if st.button("Update Email"):
                    if not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
                        st.error("Invalid email format.")
                    elif user.find_email(new_email):
                        st.error("Email already exists.")
                    else:
                        user.update_email(st.session_state.username, new_email)
                        st.success("Email updated successfully!")

            elif menu_option == "Change Password":
                st.subheader("🔑 Change Password")
                current_pw = st.text_input("Current Password", type="password")
                new_pw = st.text_input("New Password", type="password")
                confirm_pw = st.text_input("Confirm New Password", type="password")
                if st.button("Update Password"):
                    data = user.find_user(st.session_state.username)
                    if data[3] != current_pw:
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
                confirm = st.checkbox("I understand the consequences.")
                if st.button("Delete My Account") and confirm:
                    with st.spinner("Deleting account..."):
                        time.sleep(2)
                        user.delete_user(st.session_state.username)
                        st.success("Account deleted.")
                    time.sleep(1)
                    st.session_state.logged_in = False
                    st.session_state.username = None
                    st.rerun()
            
            elif menu_option == "Logout":
                st.subheader("🔒 Logout")
                st.write("Click the button below to log out.")
                if st.button("Logout"):
                    with st.spinner("Logging out..."):
                        time.sleep(2)
                        st.session_state.logged_in = False
                        st.session_state.username = None
                        st.success("Logged out successfully.")
                        st.rerun()
        

    else:
        option = st.radio("Choose an option:", ("Login", "Register"))

        if option == "Login":
            st.subheader("🔐 Login")
            input_username = st.text_input("Username")
            input_password = st.text_input("Password", type="password")
            if st.button("Login"):
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

        elif option == "Register":
            st.subheader("📝 Register")
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")

            if st.button("Register"):
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
                    user.add_user(username, email, password)
                    st.success("Registration successful! You can now login.")
                    time.sleep(1.5)
                    st.rerun()
