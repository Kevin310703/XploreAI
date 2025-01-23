import streamlit as st
from auth import create_user  # Import hàm từ auth.py

# Cấu hình trang
st.set_page_config(page_title="Register", page_icon="📝")

st.title("📝 Đăng ký tài khoản mới")

new_username = st.text_input("👤 Chọn tên đăng nhập", key="register_user")
new_password = st.text_input("🔒 Chọn mật khẩu", type="password", key="register_pass")
confirm_password = st.text_input("🔑 Nhập lại mật khẩu", type="password", key="confirm_pass")

if st.button("Tạo tài khoản ✨"):
    if new_password != confirm_password:
        st.warning("⚠️ Mật khẩu không khớp!")
    elif create_user(new_username, new_password):
        st.success("✅ Đăng ký thành công! Hãy đăng nhập ngay.")
        st.stop()
    else:
        st.error("❌ Tên đăng nhập đã tồn tại!")

# Nếu đã có tài khoản, chuyển đến trang đăng nhập
st.markdown("Bạn đã có tài khoản? [Đăng nhập tại đây](login.py)")
