from models.user_model import UserModel

class AuthController:
    def __init__(self):
        self.user_model = UserModel()

    def register_user(self, username, password):
        return self.user_model.create_user(username, password)

    def login_user(self, username, password):
        return self.user_model.check_login(username, password)
