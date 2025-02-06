import streamlit as st
import os
import webbrowser
import time
import requests
from datetime import datetime, timedelta
from utils.validator import Validator
from config import GOOGLE_CLIENT_ID, GOOGLE_REDIRECT_URI, API_BASE_URL

if not API_BASE_URL:
    raise ValueError("🚨 API_BASE_URL is not set in the environment variables!")

st.title("🌟 Welcome to XploreAI!")

# Get cookie manager from session state (in streamlit_app.py)
cookie_manager = st.session_state.cookie_manager

def set_auth_cookies(username, access_token, refresh_token, days_valid=7):
    expires_at = datetime.utcnow() + timedelta(days=days_valid)
    cookie_manager.set("access_token", access_token, key="access_token_set", expires_at=expires_at)
    cookie_manager.set("refresh_token", refresh_token, key="refresh_token_set", expires_at=expires_at)
    cookie_manager.set("username", username, key="username_set", expires_at=expires_at)

    st.session_state.auth = {
        "logged_in": True,
        "username": username,
        "access_token": access_token,
        "refresh_token": refresh_token
    }

# Management page: login, register, forgot_password
if "current_page" not in st.session_state:
    st.session_state.current_page = "login"

def switch_page(page_name):
    st.session_state.current_page = page_name
    st.rerun()

if st.session_state.current_page == "login":
    st.subheader("🔑 Login")
    st.write("Welcome back! Please enter your credentials to continue. 🚀")

    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    remember_me = st.checkbox("Remember Me", key="remember_me")

    if st.button("Login ✨"):
        if not username.strip():
            st.warning("⚠️ Please enter your username!")
        elif not Validator.is_valid_username(username):
            st.error("⚠️ Invalid username!")
        elif not password.strip():
            st.warning("⚠️ Please enter your password!")
        else:
            response = requests.post(f"{API_BASE_URL}/login/", json={
                "username": username,
                "password": password
            })
            if response.status_code == 200:
                data = response.json()
                set_auth_cookies(username, data["access"], data["refresh"])
                st.success(f"🎉 Welcome {username}! You have successfully logged in.")
                time.sleep(2)
                st.rerun()
            else:
                st.error("❌ Incorrect username or password!")

    st.markdown("---")
    st.markdown("### 🌐 Don't have an account?")
    col1, col2 = st.columns([1, 3.4])
    with col1:
        if st.button("👉 Register now"):
            switch_page("register")
    with col2:
        if st.button("👉 Forgot Password"):
            switch_page("forgot_password")

elif st.session_state.current_page == "register":
    st.subheader("📝 Register User")
    st.write("Join us today! Create an account to get started. 🚀")

    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First name", key="register_first_name")
    with col2:
        last_name = st.text_input("Last name", key="register_last_name")

    email = st.text_input("Email", key="register_email")
    username = st.text_input("Username", key="register_user")
    new_password = st.text_input("Password", type="password", key="register_pass")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm_pass")

    if st.button("Create Account ✨"):
        errors = []
        if not first_name.strip() or not last_name.strip():
            errors.append("⚠️ First name and Last name cannot be empty!")
        elif not Validator.is_valid_name(first_name) or not Validator.is_valid_name(last_name):
            errors.append("⚠️ Name should only contain letters and spaces.")

        if not email.strip():
            errors.append("⚠️ Email cannot be empty!")
        elif not Validator.is_valid_email(email):
            errors.append("❌ Invalid email format!")

        if not username.strip():
            errors.append("⚠️ Username cannot be empty!")
        elif not Validator.is_valid_username(username):
            errors.append("❌ Invalid username format!")

        is_valid_pass, pass_message = Validator.is_valid_password(new_password)
        if not new_password.strip():
            errors.append("⚠️ Password cannot be empty!")
        elif not is_valid_pass:
            errors.append(pass_message)

        if new_password != confirm_password:
            errors.append("⚠️ Passwords do not match!")

        if errors:
            for error in errors:
                st.warning(error)
        else:
            response = requests.post(f"{API_BASE_URL}/register/", json={
                "username": username,
                "email": email,
                "password": new_password,
                "first_name": first_name,
                "last_name": last_name
            })

            if response.status_code == 201:
                st.success("✅ Registration successful! Please log in.")
                time.sleep(2)
                switch_page("login")
            elif response.status_code == 400:
                st.error(response.json().get("error", "Registration failed!"))
            else:
                st.error("❌ Unexpected error! Please try again.")

    st.markdown("---")
    st.markdown("### 🌐 Or Sign in With")
    col1, col2 = st.columns([1, 1.5])
    with col1:
        if st.button("👉 Already have an account? Log in"):
            switch_page("login")
    with col2:
        if GOOGLE_CLIENT_ID:
            google_url = (
                f"https://accounts.google.com/o/oauth2/auth?client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&response_type=code&scope=email%20profile"
            )
            if st.button("👉 Sign in with Google"):
                webbrowser.open(google_url)

elif st.session_state.current_page == "forgot_password":
    st.subheader("🔑 Forgot Password?")
    st.write("Enter your email and we'll help you reset your password.")

    recovery_email = st.text_input("Enter your email", key="forgot_email")
    if st.button("Reset Password 🔄"):
        if not recovery_email.strip():
            st.warning("⚠️ Please enter your email!")
        elif not Validator.is_valid_email(recovery_email):
            st.error("❌ Invalid email format!")
        else:
            try:
                response = requests.post(f"{API_BASE_URL}/forgot-password/", json={"email": recovery_email})
                if response.status_code == 200:
                    st.success("✅ A new password has been sent to your email.")
                    time.sleep(2)
                    switch_page("login")
                else:
                    try:
                        error_message = response.json().get("error", "❌ Error processing request!")
                    except Exception:
                        error_message = f"❌ API Error: {response.status_code} - {response.text}"
                    st.error(error_message)
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Connection Error: {str(e)}")

    if st.button("🔙 Back to Login"):
        switch_page("login")
