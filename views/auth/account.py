import yaml
from yaml.loader import SafeLoader
import streamlit as st
import streamlit_authenticator as stauth
import webbrowser
from controllers.auth_controller import AuthController
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI

# Page configuration
st.set_page_config(page_title="Login", page_icon="🔑")

st.title("🌟 Welcome to X-AI!")

# Manage page state
if "current_page" not in st.session_state:
    st.session_state.current_page = "login"

# Function to switch pages
def switch_page(page_name):
    st.session_state.current_page = page_name
    st.rerun()

auth_controller = AuthController()

if st.session_state.current_page == "login":
    st.subheader("🔑 Login")
    st.write("Welcome back! Please enter your credentials to continue. 🚀")

    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    remember_me = st.checkbox("Remember Me", key="remember_me")
            
    if "forgot_password" in st.session_state and st.session_state.forgot_password:
        switch_page("forgot_password")

    if st.button("Login ✨"):
        if auth_controller.login_user(username, password):
            st.success(f"🎉 Welcome {username}! You have successfully logged in.")
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.rerun()
        else:
            st.error("❌ Incorrect username or password!")

    st.markdown("---")
    st.markdown("### 🌐 Or Sign in With")

    # Button to switch to the Register page
    col1, col2 = st.columns([1, 1.3])
    with col1:
        if st.button("👉 Don't have an account? Register now"):
            switch_page("register")
    with col2:
        if st.button("👉 Forgot Password?"):
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
        if new_password != confirm_password:
            st.warning("⚠️ Passwords do not match!")
        elif auth_controller.register_user(username, new_password):
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
    st.write("No worries! Enter your email or username, and we'll help you reset your password.")

    recovery_input = st.text_input("📧 Enter your email or username", key="forgot_email")

    if st.button("Reset Password 🔄"):
        if recovery_input:
            st.success("✅ If an account exists with this email/username, you will receive reset instructions.")
            st.info("📩 Please check your inbox (or spam folder) for further instructions.")
            switch_page("login")
        else:
            st.warning("⚠️ Please enter your email or username!")

    if st.button("🔙 Back to Login"):
        switch_page("login")
