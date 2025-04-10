import streamlit as st
import re
import os, sys, time

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

        st.markdown("---")
        with st.expander("⚠️ Delete My Account"):
            st.warning("This action is irreversible")
            confirm_delete = st.checkbox("I understand the consequences.")
            if st.button("Delete Account") and confirm_delete:
                with st.spinner("Deleting your account..."):
                    time.sleep(2)  # simulate deletion process
                    user.delete_user(st.session_state.username)
                    st.success("✅ Your account has been deleted.")
                time.sleep(1.5)  # brief pause before logging out
                st.session_state.logged_in = False
                st.session_state.username = None
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
                    st.error("Invalid email format")
                elif user.find_email(email):
                    st.error("Email already exists. Please choose a different one.")
                elif password != confirm_password:
                    st.error("Passwords do not match.")
                elif len(password) < 8 or not re.search(r"[A-Za-z]", password) or not re.search(r"[0-9]", password):
                    st.error("Password must be at least 8 characters long and contain both letters and numbers")
                else:
                    user.add_user(username, email, password)
                    st.success("Registration successful! You can now login.")
                    time.sleep(1.5)  # brief pause before redirecting
                    st.rerun()
