import streamlit as st
st.set_page_config(page_title="XploreAI", page_icon="👋")

from controllers.auth_controller import AuthController

HORIZONTAL_LOGO = "assets/image/horizontal_logo.png"
ICON_LOGO = "assets/image/icon_logo.png"

st.logo(HORIZONTAL_LOGO, icon_image=ICON_LOGO)

# Chỉ tạo một AuthController duy nhất trong session_state
if "auth_controller" not in st.session_state:
    st.session_state.auth_controller = AuthController()

auth_controller = st.session_state.auth_controller

# Tải trạng thái đăng nhập
if "logged_in" not in st.session_state:
    st.session_state.logged_in, st.session_state.username = auth_controller.load_cookie()
    print(st.session_state.logged_in)
    print(st.session_state.username)

def logout():
    auth_controller.clear_cookie()
    st.session_state.logged_in = False
    st.session_state.username = None
    st.rerun()

if st.session_state.logged_in:
    with st.sidebar:
        st.write(f"👋 Hello, **{st.session_state.username}**")
        if st.button("🚪 Log out", key="logout_button"):
            logout()

login_page = st.Page("views/auth/account.py", title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

# Dashboard section
home_page = st.Page("views/dashboard/home.py", title="Home", icon=":material/home:", default=True)

# Model section
translation = st.Page("views/service/translation-language.py", title="Translation", icon=":material/translate:")
generate_image = st.Page("views/service/generate-image.py", title="Create Image", icon=":material/image:")
summarization_text = st.Page("views/service/summarization-text.py", title="Summarization", icon=":material/short_text:")

# Account section
profile_page = st.Page("views/auth/profile.py", title="Profile", icon=":material/person:")
change_password_page = st.Page("views/auth/change_password.py", title="Change Password", icon=":material/key:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Dashboard": [home_page],
            "Service": [translation, generate_image, summarization_text],
            "Account": [profile_page, change_password_page],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()