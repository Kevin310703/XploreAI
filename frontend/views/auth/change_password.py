import streamlit as st
import time
import requests

from session_manager import logout
from utils.validator import Validator
from config import API_BASE_URL_BACKEND_USER

if not API_BASE_URL_BACKEND_USER:
    raise ValueError("🚨 API_BASE_URL is not set in the environment variables!")

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
        
# Get cookie_manager from session state
cookie_manager = st.session_state.cookie_manager

if not st.session_state.auth.get("logged_in"):
    st.warning("⚠️ You need to log in to change your password.")
    st.stop()

access_token = st.session_state.auth.get("access_token")
if not access_token:
    st.error("❌ Access token not found!")
    st.stop()

with st.form("change_password_form", enter_to_submit =True, border=False):
    st.title("🔑 Change Password")
    st.write(f"👤 Logged in as **{st.session_state.auth['username']}**")

    # Input fields for changing password
    old_password = st.text_input("Current Password", type="password")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")

    submitted = st.form_submit_button("✅ Change Password")
    if submitted:
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
                    time.sleep(1)

                    @st.dialog("Notification")
                    def notification():
                        st.write("The system will automatically log you out, and you need to log in again.")
                        if st.button("OK"):
                            logout()
                            st.rerun()

                    notification()
                else:
                    st.error(f"⚠ {response.json().get('error', 'Password change failed!')}")
