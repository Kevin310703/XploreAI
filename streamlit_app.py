import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page("views/auth/account.py", title="Log in", icon=":material/login:", default=True)
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

# Model section
translation = st.Page(
    "views/service/translation-language.py", title="Translation", icon=":material/translate:"
)
generate_image = st.Page(
    "views/service/generate-image.py", title="Create Image", icon=":material/image:"
)
summarization_text = st.Page(
    "views/service/summarization-text.py", title="Summarization", icon=":material/short_text:"
)

home_page = st.Page("views/dashboard/home.py", title="Home", icon=":material/home:")
# search = st.Page("tools/search.py", title="Search", icon=":material/search:")
# history = st.Page("tools/history.py", title="History", icon=":material/history:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Dashboard": [home_page],
            "Models": [translation, generate_image, summarization_text],
            "Account": [logout_page],
            # "Tools": [search, history],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()