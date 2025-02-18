import streamlit as st
import time
import extra_streamlit_components as stx
import requests
from datetime import datetime, timedelta
from config import API_BASE_URL_BACKEND_USER

def init_session():
    """Khởi tạo session state nếu chưa tồn tại."""
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
    """Cập nhật thông tin từ cookie vào session state."""
    cookie_manager = st.session_state.cookie_manager
    cookies = cookie_manager.get_all()

    if cookies.get("access_token") and cookies.get("username"):
        st.session_state.auth = {
            "logged_in": True,
            "username": cookies.get("username"),
            "access_token": cookies.get("access_token"),
            "refresh_token": cookies.get("refresh_token")
        }

    st.session_state["cookies_loaded"] = True

def set_auth_cookies(username, access_token, refresh_token, days_valid=7):
    """Lưu thông tin đăng nhập vào cookies và session."""
    expires_at = datetime.utcnow() + timedelta(days=days_valid)
    cookie_manager = st.session_state.cookie_manager

    cookie_manager.set("access_token", access_token, key="access_token_set", expires_at=expires_at)
    cookie_manager.set("refresh_token", refresh_token, key="refresh_token_set", expires_at=expires_at)
    cookie_manager.set("username", username, key="username_set", expires_at=expires_at)

    st.session_state.auth = {
        "logged_in": True,
        "username": username,
        "access_token": access_token,
        "refresh_token": refresh_token
    }

def clear_auth():
    """Xóa thông tin đăng nhập khỏi session và cookies."""
    st.session_state.auth = {
        "logged_in": False,
        "username": None,
        "access_token": None,
        "refresh_token": None
    }

    cookie_manager = st.session_state.cookie_manager
    expires_at = datetime.utcnow() - timedelta(days=1)
    
    cookie_manager.set("access_token", "", key="access_token_set", expires_at=expires_at)
    cookie_manager.set("refresh_token", "", key="refresh_token_set", expires_at=expires_at)
    cookie_manager.set("username", "", key="username_set", expires_at=expires_at)

    if "cookies_loaded" in st.session_state:
        del st.session_state["cookies_loaded"]

    time.sleep(1)  # Chờ để đảm bảo cookies được xóa hoàn toàn

def logout():
    """Gửi yêu cầu logout API và xóa session."""
    try:
        response = requests.post(
            f"{API_BASE_URL_BACKEND_USER}/logout/",
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

if "input_active" not in st.session_state:
    st.session_state.input_active = False
