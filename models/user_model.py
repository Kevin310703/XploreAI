import mysql.connector
import bcrypt
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
from utils.email_sender import EmailSender

class UserModel:
    def __init__(self):
        self.host = MYSQL_HOST
        self.user = MYSQL_USER
        self.password = MYSQL_PASSWORD
        self.database = MYSQL_DATABASE

    def get_db_connection(self):
        """ Kết nối đến MySQL Database """
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            ssl_disabled=False  # Bật SSL để mã hóa kết nối
        )
        return conn, conn.cursor(dictionary=True)

    def hash_password(self, password):
        """ Mã hóa mật khẩu bằng bcrypt """
        salt = bcrypt.gensalt()  # Tạo salt ngẫu nhiên
        return bcrypt.hashpw(password.encode(), salt).decode()

    def check_password(self, stored_password, input_password):
        """ Kiểm tra mật khẩu với giá trị đã mã hóa """
        return bcrypt.checkpw(input_password.encode(), stored_password.encode())
    
    def is_password_unique(self, hashed_password):
        """Kiểm tra mật khẩu đã mã hóa có tồn tại trong database không"""
        conn, cursor = self.get_db_connection()
        cursor.execute("SELECT COUNT(*) as count FROM up_users WHERE password = %s", (hashed_password,))
        result = cursor.fetchone()
        conn.close()
        return result["count"] == 0  # Trả về True nếu mật khẩu là duy nhất
    
    def update_password_auto(self, email, new_password):
        """Tạo mật khẩu duy nhất, cập nhật vào database"""
        hashed_pw = self.hash_password(new_password)

        # Lặp cho đến khi tìm được mật khẩu duy nhất
        while not self.is_password_unique(hashed_pw):
            new_password = EmailSender.generate_password()
            hashed_pw = self.hash_password(new_password)

        conn, cursor = self.get_db_connection()
        cursor.execute("UPDATE up_users SET password = %s WHERE email = %s", (hashed_pw, email))
        conn.commit()
        conn.close()
        return new_password  # Trả về mật khẩu mới đã được đặt thành công

    def check_login(self, username, password):
        """ Xác thực đăng nhập """
        conn, cursor = self.get_db_connection()
        cursor.execute("SELECT password FROM up_users WHERE username = %s", (username,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return self.check_password(result["password"], password)
        return False

    def create_user(self, username, password):
        """ Tạo tài khoản mới """
        conn, cursor = self.get_db_connection()
        try:
            hashed_pw = self.hash_password(password)
            cursor.execute("INSERT INTO up_users (username, password) VALUES (%s, %s)", (username, hashed_pw))
            conn.commit()
            return True
        except mysql.connector.IntegrityError:
            return False
        finally:
            conn.close()

    def get_user_info(self, username):
        """ Truy vấn thông tin người dùng từ database """
        conn, cursor = self.get_db_connection()
        cursor.execute("SELECT username, email FROM up_users WHERE username = %s", (username,))
        user_info = cursor.fetchone()
        conn.close()
        return user_info
    
    def update_password(self, username, old_password, new_password):
        """ Cập nhật mật khẩu nếu mật khẩu cũ đúng """
        conn, cursor = self.get_db_connection()
        cursor.execute("SELECT password FROM up_users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and self.check_password(user["password"], old_password):
            hashed_pw = self.hash_password(new_password)
            cursor.execute("UPDATE up_users SET password = %s WHERE username = %s", (hashed_pw, username))
            conn.commit()
            conn.close()
            return True
        conn.close()
        return False
    
    def update_user_info(self, username, new_email):
        """ Update user information in the database """
        conn, cursor = self.get_db_connection()
        try:
            cursor.execute("UPDATE up_users SET email = %s WHERE username = %s", (new_email, username))
            conn.commit()
            return True
        except mysql.connector.Error as e:
            return False
        finally:
            conn.close()


