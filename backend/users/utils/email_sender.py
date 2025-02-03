import smtplib
import os
import random
import string
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

class EmailSender:
    @staticmethod
    def generate_password():
        """Tạo mật khẩu ngẫu nhiên có độ dài tối thiểu 8 ký tự, có ít nhất 1 chữ hoa, 1 số, 1 ký tự đặc biệt"""
        special_chars = "!@#$%^&*()_+"
        password = (
            random.choice(string.ascii_uppercase) +
            random.choice(string.digits) +
            random.choice(special_chars) +
            "".join(random.choices(string.ascii_letters + string.digits + special_chars, k=5))
        )
        return "".join(random.sample(password, len(password)))
    
    @staticmethod
    def send_reset_email(to_email, new_password):
        sender_email = os.getenv("EMAIL_USER")
        sender_password = os.getenv("EMAIL_PASS")
        smtp_server = os.getenv("EMAIL_HOST")
        smtp_port = int(os.getenv("EMAIL_PORT"))

        HORIZONTAL_LOGO = os.getenv("HORIZONTAL_LOGO_GITHUB_WEB")

        subject = "Reset Your Password - XploreAI"

        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; text-align: center;">
            <div style="max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0,0,0,0.1);">
                <img src="{HORIZONTAL_LOGO}" alt="XploreAI Logo" style="max-width: 150px; margin-bottom: 20px;">
                <h2 style="color: #333;">🔑 Reset Your Password</h2>
                <p style="color: #555;">We have generated a new password for your account:</p>
                <p style="font-size: 20px; font-weight: bold; color: #008CBA;">{new_password}</p>
                <p style="color: #888;">Please log in using this new password and change it in your profile settings.</p>
                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                <p style="color: #777; font-size: 12px;">© 2024 XploreAI. All rights reserved.</p>
            </div>
        </body>
        </html>
        """

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  # Bảo mật kết nối
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, to_email, msg.as_string())

            return True, "✅ Email sent successfully!"
        except Exception as e:
            return False, f"❌ Error sending email: {str(e)}"
