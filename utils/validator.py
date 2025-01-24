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
    def is_valid_username(username):
        """
        Kiểm tra username hợp lệ:
        - Chỉ chứa chữ cái, số, dấu gạch dưới (_), dấu gạch ngang (-), và khoảng trắng.
        - Độ dài từ 4-20 ký tự.
        - Không chứa khoảng trắng ở đầu hoặc cuối.
        - Không có nhiều khoảng trắng liên tiếp.
        """
        pattern = r"^(?!\s)(?!.*\s{2})[a-zA-Z0-9 _-]{4,20}(?<!\s)$"
        return bool(re.match(pattern, username))

