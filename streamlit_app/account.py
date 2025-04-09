import streamlit as st
import re
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import user

# Create the database and table if it doesn't exist
user.create_table()

def my_account():
    st.title("👤 My Account")

    # If user is already logged in
    if st.session_state.get("logged_in"):
        st.success(f"Welcome, {st.session_state.username}!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.success("You have been logged out.")
            st.rerun()
        return  # Don't show login/register options if already logged in

    option = st.radio("Choose an option:", ("Login", "Register"))

    with st.container():

        if option == "Login":
            st.subheader("🔐 Login")
            input_username = st.text_input("Username")
            input_password = st.text_input("Password", type="password")
            if st.button("Login"):
                if input_username and input_password:
                    user_data = user.find_user(input_username)
                    if user_data and user_data[1] == input_username and user_data[3] == input_password:
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

            # Username availability check
            if username:
                existing_user = user.find_user(username)
                if existing_user:
                    st.error("Username already exists. Please choose a different one.")
                else:
                    st.success("Username is available.")

            # Email validation
            if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                st.error("Invalid email format")

            # Password validation
            if password and (len(password) < 8 or not re.search(r"[A-Za-z]", password) or not re.search(r"[0-9]", password)):
                st.error("Password must be at least 8 characters long and contain both letters and numbers")

            if st.button("Register"):
                if not username or not email or not password:
                    st.error("Please fill in all fields.")
                elif password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    user.add_user(username, email, password)
                    st.success("Registration successful! You can now login.")
                    st.rerun()
