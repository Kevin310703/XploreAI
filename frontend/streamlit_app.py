import streamlit as st
import extra_streamlit_components as stx
import requests
from dotenv import load_dotenv
import os
import time

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")

# Config page
st.set_page_config(
    page_title="XploreAI",
    page_icon=":rocket:",
    layout="centered"
)

# Logo của ứng dụng
HORIZONTAL_LOGO = "assets/image/horizontal_logo.png"
ICON_LOGO = "assets/image/icon_logo.png"
st.logo(HORIZONTAL_LOGO, icon_image=ICON_LOGO)

def init_session():
    """Initial session state if not exist."""
    if "cookie_manager" not in st.session_state:
        st.session_state.cookie_manager = stx.CookieManager()
    if "auth" not in st.session_state:
        st.session_state.auth = {
            "logged_in": False,
            "username": None,
            "access_token": None,
            "refresh_token": None
        }
    load_auth_from_cookies()

def load_auth_from_cookies():
    """Update information from cookie to session state."""
    cookie_manager = st.session_state.cookie_manager
    cookies = cookie_manager.get_all()
    if cookies.get("access_token") and cookies.get("username"):
        st.session_state.auth = {
            "logged_in": True,
            "username": cookies.get("username"),
            "access_token": cookies.get("access_token"),
            "refresh_token": cookies.get("refresh_token")
        }

def clear_auth():
    """Delete information from session and cookie."""
    st.session_state.auth = {
        "logged_in": False,
        "username": None,
        "access_token": None,
        "refresh_token": None
    }
    cookie_manager = st.session_state.cookie_manager
    cookie_manager.delete("access_token", key="access_token_set")
    cookie_manager.delete("refresh_token", key="refresh_token_set")
    cookie_manager.delete("username", key="username_set")


def logout():
    """Logout with API and clear session, cookie."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/logout/",
            json={"refresh": st.session_state.auth["refresh_token"]},
            headers={"Authorization": f"Bearer {st.session_state.auth['access_token']}"}
        )

        if response.status_code == 200:
            clear_auth()
            st.success("✅ Logged out successfully.")
            st.experimental_rerun()
        else:
            st.error("❌ Logout failed! Please try again.")
    except Exception as e:
        st.error(f"Logout failed: {str(e)}")

init_session()
cookie_manager = st.session_state.cookie_manager

# Display in sidebar if logged in
if st.session_state.auth["logged_in"]:
    with st.sidebar:
        st.markdown(f"### Welcome, {st.session_state.auth['username']}!")
        if st.button("Logout", key="logout_btn"):
            logout()

st.write("Logged in:", st.session_state.auth["logged_in"])

# Account page
login_page = st.Page("views/auth/account.py", title="Log in", icon=":material/login:")
profile_page = st.Page("views/auth/profile.py", title="Profile", icon=":material/person:")
change_password_page = st.Page("views/auth/change_password.py", title="Change Password", icon=":material/key:")

# Dashboard page
home_page = st.Page("views/dashboard/home.py", title="Home", icon=":material/home:", default=True)

# Service page
translation_page = st.Page("views/service/translation-language.py", title="Translation", icon=":material/translate:")
generate_image_page = st.Page("views/service/generate-image.py", title="Create Image", icon=":material/image:")
summarization_page = st.Page("views/service/summarization-text.py", title="Summarization", icon=":material/short_text:")

# Navigation
if st.session_state.auth["logged_in"]:
    pg = st.navigation(
        {
            "Dashboard": [home_page],
            "Service": [translation_page, generate_image_page, summarization_page],
            "Account": [profile_page, change_password_page],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()
