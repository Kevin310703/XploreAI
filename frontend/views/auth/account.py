import streamlit as st
import webbrowser
import time
import requests
from datetime import datetime, timedelta

from utils.validator import Validator
from config import GOOGLE_CLIENT_ID, GOOGLE_REDIRECT_URI, API_BASE_URL_BACKEND_USER

if not API_BASE_URL_BACKEND_USER:
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

# Check if verification token is in the URL
query_params = st.query_params

# Token param for verification email
token = query_params.get("token", None)
if token:
    st.session_state["verification_token"] = token
    st.session_state["current_page"] = "verify_email"

# Code param for login with Google OAuth 2.0
auth_code = query_params.get("code", None)

if auth_code and "google_auth_code" not in st.session_state:
    st.session_state["google_auth_code"] = auth_code
    switch_page("google_login")

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
            response = requests.post(f"{API_BASE_URL_BACKEND_USER}/login/", json={
                "username": username,
                "password": password
            })

            if response.status_code == 403:
                st.error("⚠️ Your email has not been verified! Please check your inbox.")
            elif response.status_code == 400:
                error_message = response.json()
                st.error(f"❌ {error_message}")
            elif response.status_code == 200:
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

if st.session_state.current_page == "google_login" and not st.session_state.get("google_logged_in", False):
    st.subheader("🔄 Processing Google Login...")

    if "google_login_requested" not in st.session_state:
        st.session_state["google_login_requested"] = True
        st.rerun()

    response = requests.post(f"{API_BASE_URL_BACKEND_USER}/google-login/", 
                             json={"code": st.session_state["google_auth_code"]})

    if response.status_code == 200:
        user_data = response.json()

        if "access_token" in user_data and "refresh_token" in user_data:
            st.success("✅ Logged in successfully!")
            time.sleep(5)

            # Save token into session
            set_auth_cookies(user_data["username"], user_data["access_token"], user_data["refresh_token"])
            st.session_state["logged_in"] = True
            st.session_state["google_logged_in"] = True  # Flag processed status

            st.query_params.clear()
            del st.session_state["google_auth_code"]
            del st.session_state["google_login_requested"]

            st.rerun()
            st.stop()
    else:
        st.error("❌ Google Login Failed")
        del st.session_state["google_auth_code"]
        del st.session_state["google_login_requested"]
        time.sleep(2)
        switch_page("login")
        st.stop()  # Ngăn không cho script tiếp tục chạy

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
            response = requests.post(f"{API_BASE_URL_BACKEND_USER}/register/", json={
                "username": username,
                "email": email,
                "password": new_password,
                "first_name": first_name,
                "last_name": last_name
            })

            if response.status_code == 201:
                st.success("✅ Registration successful! Please check your email to verify your account before logging in.")
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

elif st.session_state.current_page == "verify_email":
    st.subheader("📩 Email Verification")
    
    # Lấy token từ session state
    token = st.session_state.get("verification_token", None)

    if token and "email_verified" not in st.session_state:
        with st.spinner("🔄 Verifying your email..."):
            response = requests.get(f"{API_BASE_URL_BACKEND_USER}/verify-email/{token}")

            if response.status_code == 200:
                del st.session_state["verification_token"]
                st.success("✅ Your email has been verified successfully! You can now log in.")
                st.session_state["email_verified"] = True  
            elif response.status_code == 400:
                del st.session_state["verification_token"]
                st.warning("⚠️ Your email is already verified. Please log in.")
                st.session_state["email_verified"] = True
            else:
                st.error("❌ Verification failed. Invalid or expired token.")
        
        time.sleep(5)

    st.query_params.clear()
    if st.button("🔙 Back to Login"):
        switch_page("login")

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
                response = requests.post(f"{API_BASE_URL_BACKEND_USER}/forgot-password/", json={"email": recovery_email})
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
