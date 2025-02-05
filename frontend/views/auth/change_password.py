import time
import streamlit as st
import os
import requests
from dotenv import load_dotenv
from utils.validator import Validator

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")

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

# Get cookie_manager from session state
cookie_manager = st.session_state.cookie_manager

if not st.session_state.auth.get("logged_in"):
    st.warning("⚠️ You need to log in to change your password.")
    st.stop()

st.write(f"👤 Logged in as **{st.session_state.auth["username"]}**")

# Input fields for changing password
old_password = st.text_input("🔒 Current Password", type="password")
new_password = st.text_input("🔑 New Password", type="password")
confirm_password = st.text_input("🔑 Confirm New Password", type="password")

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
            headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
            response = requests.post(f"{API_BASE_URL}/change-password/", headers=headers, json={
                "old_password": old_password,
                "new_password": new_password
            })

            if response.status_code == 200:
                st.success("🎉 Password changed successfully! Please log in again.")
                time.sleep(4)
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.access_token = None
                st.rerun()
            else:
                st.error(f"⚠ {response.json().get('error', 'Password change failed!')}")
