import streamlit as st
from action import check_login

# Cấu hình trang
st.set_page_config(page_title="Login", page_icon="🔑")

st.title("🔐 Đăng nhập")

# Kiểm tra trạng thái đăng nhập
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

username = st.text_input("👤 Tên đăng nhập", key="login_user")
password = st.text_input("🔒 Mật khẩu", type="password", key="login_pass")

if st.button("Đăng nhập ✅"):
    if check_login(username, password):
        st.success(f"🎉 Chào mừng {username}! Bạn đã đăng nhập thành công.")
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        st.experimental_rerun()  # Reload lại trang
    else:
        st.error("❌ Sai tên đăng nhập hoặc mật khẩu!")

# Nếu chưa có tài khoản, chuyển đến trang đăng ký
st.markdown("Bạn chưa có tài khoản? [Đăng ký ngay](register.py)")

# Đăng xuất
if st.session_state.logged_in:
    if st.button("🚪 Đăng xuất"):
        st.session_state.logged_in = False
        st.experimental_rerun()  # Reload trang để quay lại giao diện đăng nhập
