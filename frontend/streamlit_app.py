import streamlit as st
import time
import extra_streamlit_components as stx
import requests
from datetime import datetime, timedelta
from config import API_BASE_URL_BACKEND

# Config page
st.set_page_config(
    page_title="XploreAI",
    page_icon=":rocket:",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        'About': """
        # 🚀 Welcome to XploreAI!
        
        **XploreAI** is your ultimate AI-powered companion, designed to unlock the full potential of artificial intelligence for your needs.  
        
        🧠 **Key Features**:
        - 🌍 AI-driven language translation and text summarization  
        - 🎨 AI-generated images with cutting-edge diffusion models  
        - 🤖 Smart chatbot that understands natural conversations  
        - 📊 Data processing and visualization for insightful analytics  

        Whether you're an AI enthusiast, researcher, or developer, **XploreAI** empowers you with state-of-the-art machine learning tools at your fingertips.  

        🔗 *Stay curious. Explore more. Innovate with AI!*  
        """
    }
)

# Logo app
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
    if "cookies_loaded" in st.session_state:
        return  # Tránh gọi lại nhiều lần gây lỗi

    cookie_manager = st.session_state.cookie_manager
    cookies = cookie_manager.get_all(key="load_auth")  # Đặt key duy nhất để tránh lỗi

    if cookies.get("access_token") and cookies.get("username"):
        st.session_state.auth = {
            "logged_in": True,
            "username": cookies.get("username"),
            "access_token": cookies.get("access_token"),
            "refresh_token": cookies.get("refresh_token")
        }

    st.session_state["cookies_loaded"] = True

def clear_auth():
    """Delete information from session and cookie."""
    st.session_state.auth = {
        "logged_in": False,
        "username": None,
        "access_token": None,
        "refresh_token": None
    }

    cookie_manager = st.session_state.cookie_manager
    cookie_manager.set("access_token", "", key="access_token_set", expires_at=datetime.utcnow() - timedelta(days=1))
    cookie_manager.set("refresh_token", "", key="refresh_token_set", expires_at=datetime.utcnow() - timedelta(days=1))
    cookie_manager.set("username", "", key="username_set", expires_at=datetime.utcnow() - timedelta(days=1))

    # Xóa dữ liệu session state
    if "cookies_loaded" in st.session_state:
        del st.session_state["cookies_loaded"]

    time.sleep(1)  # Chờ một chút để đảm bảo cookie thực sự được xóa
    st.rerun()


def logout():
    """Logout with API and clear session, cookie."""
    try:
        response = requests.post(
            f"{API_BASE_URL_BACKEND}/logout/",
            json={"refresh": st.session_state.auth["refresh_token"]},
            headers={"Authorization": f"Bearer {st.session_state.auth['access_token']}"}
        )

        if response.status_code == 200:
            st.success("✅ Logged out successfully.")

            clear_auth()
            time.sleep(2)
            st.rerun()
        else:
            st.error("❌ Logout failed! Please try again.")
    except Exception as e:
        st.error(f"Logout failed: {str(e)}")

init_session()
cookie_manager = st.session_state.cookie_manager

# Display in sidebar if logged in
if "cookies_loaded" not in st.session_state:  # Đảm bảo chỉ load một lần
    load_auth_from_cookies()

if st.session_state.auth["logged_in"]:
    with st.sidebar:
        st.markdown(f"### Welcome, {st.session_state.auth['username']}!")
        if st.button("Logout", key="logout_btn"):
            logout()

print("Logged in:", st.session_state.auth["logged_in"])

# Account page
login_page = st.Page("views/auth/account.py", title="Log in", icon=":material/login:")
profile_page = st.Page("views/auth/profile.py", title="Profile", icon=":material/person:")
change_password_page = st.Page("views/auth/change_password.py", title="Change Password", icon=":material/key:")

# Dashboard page
home_page = st.Page("views/dashboard/home.py", title="Home", icon=":material/home:", default=True)

# Service page
translation_page = st.Page("views/service/translation-language.py", title="Translation", icon=":material/translate:")
generate_image_page = st.Page("views/service/generate-image.py", title="Generate Image", icon=":material/image:")
summarization_page = st.Page("views/service/summarization-text.py", title="Summarization", icon=":material/short_text:")
vqa_page = st.Page("views/service/visual-question-answer.py", title="Q&A", icon=":material/visibility:")
generate_text_page = st.Page("views/service/generate-text.py", title="Generate Text", icon=":material/chat:")

# Navigation
if st.session_state.auth["logged_in"]:
    pg = st.navigation(
        {
            "Dashboard": [home_page],
            "Service": [translation_page, generate_image_page, 
                        generate_text_page, summarization_page, 
                        vqa_page],
            "Account": [profile_page, change_password_page],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()
