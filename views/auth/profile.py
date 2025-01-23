import streamlit as st
from controllers.auth_controller import AuthController

st.title("👤 User Profile")

# Initialize AuthController
if "auth_controller" not in st.session_state:
    st.session_state.auth_controller = AuthController()

auth_controller = st.session_state.auth_controller

# Check if the user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ You need to log in to view your profile.")
    st.stop()

# Get current user info
username = st.session_state.get("username")
user_info = auth_controller.get_profile(username)

if user_info:
    col1, col2 = st.columns([1, 3])

    with col1:
        st.image("assets/image/default_avatar.jpg", width=150, caption="Default Avatar")

    with col2:
        st.markdown(f"### Welcome, **{user_info['username']}**")
        st.write(f"📧 **Email:** {user_info['email']}")

    # Enable Edit Mode
    st.markdown("---")
    st.subheader("✏ Edit Profile")

    new_email = st.text_input("📧 Update Email", value=user_info['email'])
    
    if st.button("💾 Save Changes"):
        if new_email.strip() == "":
            st.error("❌ Email cannot be empty.")
        else:
            success = auth_controller.update_profile(username, new_email)
            if success:
                st.success("✅ Profile updated successfully!")
                st.session_state["updated_email"] = new_email  # Temporary update before refresh
                st.rerun()
            else:
                st.error("⚠ Unable to update profile. Please try again later.")

    st.markdown("---")
    if st.button("🔙 Back to Home"):
        st.switch_page("views/dashboard/home.py")

else:
    st.error("❌ Unable to load profile information.")
