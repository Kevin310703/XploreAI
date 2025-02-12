import streamlit as st
import time
import requests
from datetime import datetime, timedelta

from config import API_BASE_URL_BACKEND
from utils.validator import Validator

if not API_BASE_URL_BACKEND:
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

st.title("👤 User Profile")

# Get cookie_manager from session state
cookie_manager = st.session_state.cookie_manager

if not st.session_state.auth.get("logged_in"):
    st.warning("⚠️ You need to log in to view your profile.")
    st.stop()

access_token = st.session_state.auth.get("access_token")
if not access_token:
    st.error("❌ Access token not found!")
    st.stop()

headers = {"Authorization": f"Bearer {access_token}"}
response = requests.get(f"{API_BASE_URL_BACKEND}/profile/", headers=headers)

if response.status_code == 200:
    user_info = response.json()
    
    avatar_url = f"http://127.0.0.1:8000{user_info['avatar']}" if user_info.get("avatar") else "assets/image/default_avatar.jpg"

    col1, col2 = st.columns([1, 3])

    with col1:
        html_code = f"""
            <style>
            .round-img {{
                width: 150px;
                height: 150px;
                border-radius: 50%;
                object-fit: cover;
                border: 2px solid #blue;
            }}
            </style>
            <img src="{avatar_url}" class="round-img" alt="Avatar">
        """

        st.markdown(html_code, unsafe_allow_html=True)

    with col2:
        st.markdown(f"### Welcome, **{user_info['username']}**")
        st.write(f"📧 **Email:** {user_info['email']}")

    # Upload Avatar
    st.markdown("---")
    st.subheader("🖼️ Upload New Avatar")
    uploaded_file = st.file_uploader("Choose a profile picture", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        if st.button("Upload Avatar"):
            files = {"avatar": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            response = requests.put(f"{API_BASE_URL_BACKEND}/profile/avatar/", headers=headers, files=files)

            if response.status_code == 200:
                st.success("✅ Avatar updated successfully!")
                time.sleep(4)
                st.rerun()
            else:
                st.error(f"⚠️ Unable to update avatar. Error: {response.text}")

    # Upload information
    st.markdown("---")
    st.subheader("✏ Edit Profile")

    new_first_name = st.text_input("First Name", value=user_info.get('first_name', ''))
    new_last_name = st.text_input("Last Name", value=user_info.get('last_name', ''))
    new_username = st.text_input("Username", value=user_info.get('username', ''))
    new_email = st.text_input("Email", value=user_info.get('email', ''))

    if st.button("💾 Save Changes"):
        errors = []

        if not Validator.is_valid_name(new_first_name):
            errors.append("❌ First Name is invalid. Only letters and spaces (2-30 characters) are allowed.")
        
        if not Validator.is_valid_name(new_last_name):
            errors.append("❌ Last Name is invalid. Only letters and spaces (2-30 characters) are allowed.")
        
        if not Validator.is_valid_username(new_username):
            errors.append("❌ Username must be 150 characters or fewer. Only letters, numbers, and @/./+/-/_ are allowed.")
        
        if not Validator.is_valid_email(new_email):
            errors.append("❌ Email format is invalid.")

        if errors:
            for error in errors:
                st.error(error)
        else:
            update_response = requests.put(
                f"{API_BASE_URL_BACKEND}/profile/",
                headers=headers,
                json={
                    "first_name": new_first_name,
                    "last_name": new_last_name,
                    "username": new_username,
                    "email": new_email
                }
            )
            if update_response.status_code == 200:
                st.success("✅ Profile updated successfully!")
                st.session_state.auth["username"] = new_username
                cookie_manager.set("username", new_username, key="username_set", 
                                   expires_at=datetime.utcnow() + timedelta(days=7))
                time.sleep(4)
                st.rerun()
            else:
                st.error("⚠️ Unable to update profile. Please try again later.")

    st.markdown("---")
else:
    st.error("❌ Unable to load profile information.")
