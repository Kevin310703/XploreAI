import streamlit as st
import requests
import os
from dotenv import load_dotenv
from utils.validator import Validator

# Load env variable
load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")

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
response = requests.get(f"{API_BASE_URL}/profile/", headers=headers)

if response.status_code == 200:
    user_info = response.json()
    col1, col2 = st.columns([1, 3])

    with col1:
        st.image("assets/image/default_avatar.jpg", width=150, caption="Default Avatar")

    with col2:
        st.markdown(f"### Welcome, **{user_info['username']}**")
        st.write(f"📧 **Email:** {user_info['email']}")

    # Input field
    st.markdown("---")
    st.subheader("✏ Edit Profile")

    new_first_name = st.text_input("📝 First Name", value=user_info.get('first_name', ''))
    new_last_name = st.text_input("📝 Last Name", value=user_info.get('last_name', ''))
    new_username = st.text_input("👤 Username", value=user_info.get('username', ''))
    new_email = st.text_input("📧 Email", value=user_info.get('email', ''))

    if st.button("💾 Save Changes"):
        errors = []

        # Check input with validator
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
                f"{API_BASE_URL}/profile/",
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
                st.experimental_rerun()
            else:
                st.error("⚠️ Unable to update profile. Please try again later.")

    st.markdown("---")
    if st.button("🔙 Back to Home"):
        st.switch_page("views/dashboard/home.py")
else:
    st.error("❌ Unable to load profile information.")
