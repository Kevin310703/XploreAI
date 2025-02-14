from datetime import datetime, timedelta
import time
import streamlit as st
import requests
from utils.validator import Validator
from config import API_BASE_URL_BACKEND_USER

if not API_BASE_URL_BACKEND_USER:
    raise ValueError("🚨 API_BASE_URL is not set in the environment variables!")

st.title("🔑 Change Password")

if "cookie_manager" not in st.session_state:
    import extra_streamlit_components as stx
    st.session_state.cookie_manager = stx.CookieManager()

if "auth" not in st.session_state:
    st.session_state.auth = {
        "logged_in": False,
        "username": None,
        "access_token": None,
        "refresh_token": None
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
        
# Get cookie_manager from session state
cookie_manager = st.session_state.cookie_manager

if not st.session_state.auth.get("logged_in"):
    st.warning("⚠️ You need to log in to change your password.")
    st.stop()

access_token = st.session_state.auth.get("access_token")
if not access_token:
    st.error("❌ Access token not found!")
    st.stop()

st.write(f"👤 Logged in as **{st.session_state.auth["username"]}**")

# Input fields for changing password
old_password = st.text_input("Current Password", type="password")
new_password = st.text_input("New Password", type="password")
confirm_password = st.text_input("Confirm New Password", type="password")

if st.button("✅ Change Password"):
    if not old_password or not new_password or not confirm_password:
        st.error("❌ Please fill in all required fields.")

    elif new_password != confirm_password:
        st.error("❌ New password and confirmation do not match. Please try again.")
    
    else:
        is_valid, message = Validator.is_valid_password(new_password)
        if not is_valid:
            st.error(f"⚠ {message}")  # Show validation error
        else:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(f"{API_BASE_URL_BACKEND_USER}/change-password/", headers=headers, json={
                "old_password": old_password,
                "new_password": new_password
            })

            if response.status_code == 200:
                st.success("🎉 Password changed successfully! Please log in again.")
                time.sleep(4)
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.access_token = None
                logout()
                st.rerun()
            else:
                st.error(f"⚠ {response.json().get('error', 'Password change failed!')}")
