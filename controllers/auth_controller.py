import extra_streamlit_components as stx
from models.user_model import UserModel
from utils.email_sender import EmailSender

class AuthController:
    _cookie_manager = None  # Biến static để quản lý cookie

    def __init__(self):
        self.user_model = UserModel()
        if AuthController._cookie_manager is None:
            AuthController._cookie_manager = stx.CookieManager(key="auth_cookie")  # Chỉ tạo một lần
        self.cookie_manager = AuthController._cookie_manager

    def save_cookie(self, username):
        """ Lưu trạng thái đăng nhập vào cookie """
        self.cookie_manager.set("logged_in", "true", key=f"auth_logged_in_{username}")
        self.cookie_manager.set("username", username, key=f"auth_username_{username}")

    def load_cookie(self):
        """ Tải trạng thái đăng nhập từ cookie """
        logged_in = self.cookie_manager.get("logged_in") == "true"
        username = self.cookie_manager.get("username")
        return logged_in, username

    def clear_cookie(self):
        """ Xóa cookie khi logout """
        self.cookie_manager.delete("logged_in", key="auth_logged_in")
        self.cookie_manager.delete("username", key="auth_username")

    def register_user(self, username, password):
        """ Đăng ký người dùng """
        return self.user_model.create_user(username, password)

    def login_user(self, username, password):
        """ Kiểm tra đăng nhập """
        if self.user_model.check_login(username, password):
            self.save_cookie(username)  # Lưu thông tin đăng nhập
            return True
        return False

    def get_profile(self, username):
        return self.user_model.get_user_info(username)
    
    def change_password(self, username, old_password, new_password):
        """ Đổi mật khẩu người dùng """
        return self.user_model.update_password(username, old_password, new_password)

    def update_profile(self, username, new_email):
        """ Calls the UserModel to update profile information """
        return self.user_model.update_user_info(username, new_email)
    
    def reset_password(self, email):
        """Tạo mật khẩu mới, đảm bảo nó là duy nhất, sau đó gửi qua email"""
        new_password = EmailSender.generate_password()  # Tạo mật khẩu trước

        updated_password = self.user_model.update_password_auto(email, new_password)

        if updated_password:
            email_sent, msg = EmailSender.send_reset_email(email, updated_password)
            return email_sent, msg
        return False, "❌ Failed to update password."
