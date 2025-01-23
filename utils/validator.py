import re

class PasswordValidator:
    @staticmethod
    def is_valid(password):
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
