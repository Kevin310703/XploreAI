import streamlit as st
from utils.validator import Validator
from controllers.auth_controller import AuthController
import urllib.parse

st.set_page_config(page_title="Reset Password", page_icon="🔑")

auth_controller = AuthController()

# Lấy email từ URL (nếu có)
query_params = st.experimental_get_query_params()
email = query_params.get("email", [None])[0]

st.title("🔒 Reset Password")

if email:
    st.write(f"🔹 Reset password for: **{email}**")
else:
    st.warning("⚠️ Invalid reset link! Please check your email again.")

# Nhập mật khẩu mới
new_password = st.text_input("🔑 Enter new password", type="password", key="new_pass")
confirm_password = st.text_input("🔑 Confirm new password", type="password", key="confirm_pass")

if st.button("🔄 Reset Password"):
    if not email:
        st.error("❌ Invalid reset request!")
    elif not new_password or not confirm_password:
        st.warning("⚠️ Please enter and confirm your new password.")
    elif new_password != confirm_password:
        st.error("❌ Passwords do not match!")
    else:
        # Kiểm tra mật khẩu hợp lệ
        valid, msg = Validator.is_valid_password(new_password)
        if not valid:
            st.warning(msg)
        else:
            # Cập nhật mật khẩu trong database
            success = auth_controller.update_password(email, new_password)
            if success:
                st.success("✅ Password reset successful! Please log in with your new password.")
                st.button("🔙 Go to Login", on_click=lambda: st.switch_page("views/auth/account.py"))
            else:
                st.error("❌ Failed to reset password! Try again later.")
