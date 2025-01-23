import extra_streamlit_components as stx
from models.user_model import UserModel

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
