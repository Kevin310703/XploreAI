import re

class Validator:
    @staticmethod
    def is_valid_password(password):
        """
        Validates the password based on the following criteria:
        - At least 8 characters long
        - Contains at least one uppercase letter
        - Contains at least one digit
        - Contains at least one special character (!@#$%^&*()_+)
        
        Returns:
        - Tuple (bool, str): (True, "Password is valid.") if the password meets all requirements.
                             (False, "Error message") if any requirement is not met.
        """

        if len(password) < 8:
            return False, "Password must be at least 8 characters long."

        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter."

        if not re.search(r"\d", password):
            return False, "Password must contain at least one number."

        if not re.search(r"[!@#$%^&*()_+]", password):
            return False, "Password must contain at least one special character (!@#$%^&*()_+)."

        return True, "Password is valid."
    
    @staticmethod
    def is_valid_email(email):
        """
        Kiểm tra định dạng email hợp lệ
        """
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return bool(re.match(pattern, email))
    
    @staticmethod
    def is_valid_name(name):
        """
        Kiểm tra tên hợp lệ:
        - Chỉ chứa chữ cái (không số, không ký tự đặc biệt)
        - Không có khoảng trắng thừa ở đầu/cuối
        - Độ dài từ 2-30 ký tự
        """
        return bool(re.match(r"^[A-Za-zÀ-Ỹà-ỹ\s]{2,30}$", name.strip()))

    @staticmethod
    def is_valid_username(username):
        """
        Kiểm tra username hợp lệ:
        - Tối đa 150 ký tự.
        - Chỉ chứa chữ cái, số, @, ., +, -, _
        """
        pattern = r"^[a-zA-Z0-9@.+\-_]{1,150}$"
        return bool(re.match(pattern, username))

