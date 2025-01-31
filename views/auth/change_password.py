import streamlit as st
from controllers.auth_controller import AuthController
from utils.validator import Validator

st.title("🔑 Change Password")

if "auth_controller" not in st.session_state:
    st.session_state.auth_controller = AuthController()

auth_controller = st.session_state.auth_controller

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("You need to log in to change your password.")
    st.stop()

st.write(f"👤 Logged in as **{st.session_state.username}**")

# Input fields for changing password
old_password = st.text_input("🔒 Current Password", type="password")
new_password = st.text_input("🔑 New Password", type="password")
confirm_password = st.text_input("🔑 Confirm New Password", type="password")

if st.button("✅ Change Password"):
    if not old_password or not new_password or not confirm_password:
        st.error("Please fill in all required fields.")

    elif new_password != confirm_password:
        st.error("New password and confirmation do not match. Please try again.")
    
    else:
        is_valid, message = Validator.is_valid_password(new_password)
        if not is_valid:
            st.error(f"⚠ {message}")  # Show validation error
        else:
            # Proceed with password change
            success = auth_controller.change_password(st.session_state.username, old_password, new_password)
            if success:
                st.success("🎉 Password changed successfully! Please log in again.")
                auth_controller.clear_cookie()
                st.session_state.logged_in = False
                st.session_state.username = None
                st.rerun()
            else:
                st.error("⚠ Incorrect current password. Please try again.")
