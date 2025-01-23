import streamlit as st
from controllers.auth_controller import AuthController

auth_controller = AuthController()

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ You need to log in to view your profile.")
    st.stop()

username = st.session_state.get("username")
user_info = auth_controller.get_profile(username)

if user_info:
    st.title("👤 User Profile")
    st.markdown("### Welcome, " + user_info["username"])

    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image("assets/image/default_avatar.jpg", width=150, caption="Default Avatar")

    with col2:
        st.write(f"**📧 Email:** {user_info['email']}")
        st.write("**📅 Joined:** 2023-10-01")

    st.markdown("---")
    if st.button("🔙 Back to Home"):
        st.switch_page("views/dashboard/home.py")

else:
    st.error("❌ Unable to load profile information.")
