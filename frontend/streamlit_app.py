import streamlit as st
import time
from session_manager import init_session, load_auth_from_cookies, logout

# Config page
st.set_page_config(
    page_title="XploreAI",
    page_icon=":rocket:",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        'About': """
        # 🚀 Welcome to XploreAI!
        
        **XploreAI** is your ultimate AI-powered companion, designed to unlock the full potential of artificial intelligence for your needs.  
        
        🧠 **Key Features**:
        - 🌍 AI-driven language translation and text summarization  
        - 🎨 AI-generated images with cutting-edge diffusion models  
        - 🤖 Smart chatbot that understands natural conversations  
        - 📊 Data processing and visualization for insightful analytics  

        Whether you're an AI enthusiast, researcher, or developer, **XploreAI** empowers you with state-of-the-art machine learning tools at your fingertips.  

        🔗 *Stay curious. Explore more. Innovate with AI!*  
        """
    }
)

# Logo app
HORIZONTAL_LOGO = "assets/image/horizontal_logo.png"
ICON_LOGO = "assets/image/icon_logo.png"
st.logo(HORIZONTAL_LOGO, icon_image=ICON_LOGO)

init_session()
cookie_manager = st.session_state.cookie_manager

# Display in sidebar if logged in
if "cookies_loaded" not in st.session_state:
    load_auth_from_cookies()

if st.session_state.auth["logged_in"]:
    with st.sidebar:
        st.markdown(f"### Welcome, {st.session_state.auth['username']}!")
        if st.button("Logout", key="logout_btn"):
            logout()

print("Logged in:", st.session_state.auth["logged_in"])

# Account page
login_page = st.Page("views/auth/account.py", title="Log in", icon=":material/login:")
profile_page = st.Page("views/auth/profile.py", title="Profile", icon=":material/person:")
change_password_page = st.Page("views/auth/change_password.py", title="Change Password", icon=":material/key:")

# Dashboard page
home_page = st.Page("views/dashboard/home.py", title="Home", icon=":material/home:", default=True)

# Service page
translation_page = st.Page("views/service/translation-language.py", title="Translation", icon=":material/translate:")
generate_image_page = st.Page("views/service/generate-image.py", title="Generate Image", icon=":material/image:")
summarization_page = st.Page("views/service/summarization-text.py", title="Summarization", icon=":material/short_text:")
vqa_page = st.Page("views/service/visual-question-answer.py", title="Q&A", icon=":material/visibility:")
generate_text_page = st.Page("views/service/generate-text.py", title="Generate Text", icon=":material/chat:")
image_to_text_page = st.Page("views/service/image-read.py", title="Image Read", icon=":material/imagesmode:")

# Navigation
if st.session_state.auth["logged_in"]:
    pg = st.navigation(
        {
            "Dashboard": [home_page],
            "Text": [translation_page, generate_text_page, summarization_page],
            "Image": [generate_image_page, vqa_page, image_to_text_page],
            "Account": [profile_page, change_password_page],
        }
    )
else:
    time.sleep(2)
    pg = st.navigation([login_page])

pg.run()
