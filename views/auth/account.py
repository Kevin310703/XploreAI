import streamlit as st
import webbrowser
import time
from utils.validator import Validator
from utils.email_sender import EmailSender
import urllib.parse
from config import GOOGLE_CLIENT_ID, GOOGLE_REDIRECT_URI

st.title("🌟 Welcome to XploreAI!")

# Manage page state
if "current_page" not in st.session_state:
    st.session_state.current_page = "login"

# Function to switch pages
def switch_page(page_name):
    st.session_state.current_page = page_name
    st.rerun()

auth_controller = st.session_state.auth_controller

if st.session_state.current_page == "login":
    st.subheader("🔑 Login")
    st.write("Welcome back! Please enter your credentials to continue. 🚀")

    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    remember_me = st.checkbox("Remember Me", key="remember_me")
            
    if "forgot_password" in st.session_state and st.session_state.forgot_password:
        switch_page("forgot_password")

    if st.button("Login ✨"):
        is_valid, message = Validator.is_valid_password(password)

        if not username.strip():
            st.warning("⚠️ Please enter your username!")
        elif not Validator.is_valid_username(username):
            st.error("⚠️ Invalid username! Username must be 4-20 characters long and can only contain letters, numbers, spaces, underscores (_), or dashes (-). It cannot start or end with a space, nor have consecutive spaces.")
        elif not password.strip():
            st.warning("⚠️ Please enter your password!")
        elif not is_valid:
            st.error(f"⚠️ {message}")
        else:
            if auth_controller.login_user(username, password):
                st.success(f"🎉 Welcome {username}! You have successfully logged in.")
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("❌ Incorrect username or password!")

    st.markdown("---")
    st.markdown("### 🌐 Don't have an account? ")

    # Button to switch to the Register page
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

        # Kiểm tra tên
        if not first_name.strip() or not last_name.strip():
            errors.append("⚠️ First name and Last name cannot be empty!")
        elif not Validator.is_valid_name(first_name) or not Validator.is_valid_name(last_name):
            errors.append("⚠️ Name should only contain letters and spaces, no numbers or special characters.")

        # Kiểm tra email
        if not email.strip():
            errors.append("⚠️ Email cannot be empty!")
        elif not Validator.is_valid_email(email):
            errors.append("❌ Invalid email format!")

        # Kiểm tra username
        if not username.strip():
            errors.append("⚠️ Username cannot be empty!")
        elif not Validator.is_valid_username(username):
            errors.append("❌ Username must be 4-20 characters long and can only contain letters, numbers, spaces, underscores (_), or dashes (-). It cannot start or end with a space, nor have consecutive spaces.")

        # Kiểm tra mật khẩu
        is_valid_pass, pass_message = Validator.is_valid_password(new_password)
        if not new_password.strip():
            errors.append("⚠️ Password cannot be empty!")
        elif not is_valid_pass:
            errors.append(pass_message)

        # Kiểm tra mật khẩu nhập lại
        if new_password != confirm_password:
            errors.append("⚠️ Passwords do not match!")

        # Hiển thị tất cả lỗi nếu có
        if errors:
            for error in errors:
                st.warning(error)
        else:
            if auth_controller.register_user(username, new_password):
                st.success("✅ Registration successful! Please log in.")
                switch_page("login")
            else:
                st.error("❌ Username already exists!")

    st.markdown("---")

    # 🌐 **OAuth2 Đăng Nhập (Google)**
    st.markdown("### 🌐 Or Sign in With")
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        if st.button("👉 Already have an account? Log in"):
            switch_page("login")

    with col2:
        if GOOGLE_CLIENT_ID:
            google_url = f"https://accounts.google.com/o/oauth2/auth?client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&response_type=code&scope=email%20profile"
            if st.button("👉 Sign in with Google"):
                webbrowser.open(google_url)

elif st.session_state.current_page == "forgot_password":
    st.subheader("🔑 Forgot Password?")
    st.write("No worries! Enter your email, and we'll help you reset your password.")

    recovery_email = st.text_input("Enter your email", key="forgot_email")

    if st.button("Reset Password 🔄"):
        if not recovery_email.strip():
            st.warning("⚠️ Please enter your email!")
        elif not Validator.is_valid_email(recovery_email):
            st.error("❌ Invalid email format!")
        else:
            success, message = auth_controller.reset_password(recovery_email)

            if success:
                st.success("✅ A new password has been sent to your email. Please check your inbox.")
                time.sleep(5)
                switch_page("login")
            else:
                st.error(message)

    st.markdown("---")
    if st.button("🔙 Back to Login"):
        switch_page("login")
