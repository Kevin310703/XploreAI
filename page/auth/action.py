import sqlite3
import hashlib

# Hàm kết nối database
def get_db_connection():
    conn = sqlite3.connect("users.db", check_same_thread=False)
    return conn, conn.cursor()

# Tạo bảng users nếu chưa có
def init_db():
    conn, cursor = get_db_connection()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Hàm băm mật khẩu
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Hàm kiểm tra đăng nhập
def check_login(username, password):
    conn, cursor = get_db_connection()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result and result[0] == hash_password(password)

# Hàm tạo tài khoản mới
def create_user(username, password):
    conn, cursor = get_db_connection()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                       (username, hash_password(password)))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

# Khởi tạo database khi chạy file
init_db()
