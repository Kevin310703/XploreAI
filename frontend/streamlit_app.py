import streamlit as st
st.set_page_config(page_title="XploreAI", page_icon="👋")

import extra_streamlit_components as stx
import requests
from dotenv import load_dotenv
import os
load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")

HORIZONTAL_LOGO = "assets/image/horizontal_logo.png"
ICON_LOGO = "assets/image/icon_logo.png"

st.logo(HORIZONTAL_LOGO, icon_image=ICON_LOGO)

cookie_manager = stx.CookieManager()

# Tải trạng thái đăng nhập
if "logged_in" not in st.session_state:
    access_token = cookie_manager.get("access_token")
    username = cookie_manager.get("username")

    if access_token and username:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.access_token = access_token
    else:
        st.session_state.logged_in = False
        st.session_state.username = None

def logout():
    access_token = st.session_state.get("access_token", None)

    if access_token:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.post(f"{API_BASE_URL}/logout/", headers=headers)

        if response.status_code == 200:
            st.success("✅ Logged out successfully.")
            cookie_manager.delete("access_token")
            cookie_manager.delete("username")
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
        else:
            st.error("❌ Logout failed! Please try again.")
    else:
        st.warning("⚠️ You are not logged in!")

if st.session_state.logged_in:
    with st.sidebar:
        st.write(f"👋 Hello, **{st.session_state.username}**")
        if st.button("🚪 Log out", key="logout_button"):
            logout()

login_page = st.Page("views/auth/account.py", title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

# Dashboard section
home_page = st.Page("views/dashboard/home.py", title="Home", icon=":material/home:", default=True)

# Model section
translation = st.Page("views/service/translation-language.py", title="Translation", icon=":material/translate:")
generate_image = st.Page("views/service/generate-image.py", title="Create Image", icon=":material/image:")
summarization_text = st.Page("views/service/summarization-text.py", title="Summarization", icon=":material/short_text:")

# Account section
profile_page = st.Page("views/auth/profile.py", title="Profile", icon=":material/person:")
change_password_page = st.Page("views/auth/change_password.py", title="Change Password", icon=":material/key:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Dashboard": [home_page],
            "Service": [translation, generate_image, summarization_text],
            "Account": [profile_page, change_password_page],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()