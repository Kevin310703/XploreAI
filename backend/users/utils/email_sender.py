import smtplib
import os
import random
import string
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

class EmailSender:
    def __init__(self):
        self.sender_email = os.getenv("EMAIL_USER")
        self.sender_password = os.getenv("EMAIL_PASS")
        self.smtp_server = os.getenv("EMAIL_HOST")
        self.smtp_port = int(os.getenv("EMAIL_PORT"))
        self.horizontal_logo = os.getenv("HORIZONTAL_LOGO_GITHUB_WEB")

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
    
    def send_email(self, to_email, subject, body):
        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Bảo mật kết nối
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, to_email, msg.as_string())
            return True, "✅ Email sent successfully!"
        except Exception as e:
            return False, f"❌ Error sending email: {str(e)}"
        
    def send_reset_email(self, to_email, new_password):
        subject = "Reset Your Password - XploreAI"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; text-align: center;">
            <div style="max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0,0,0,0.1);">
                <img src="{self.horizontal_logo}" alt="XploreAI Logo" style="max-width: 150px; margin-bottom: 20px;">
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

        return self.send_email(to_email, subject, body)
        
    def send_verification_email(self, to_email, verification_link):
        subject = "Confirm Your Email - XploreAI"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; text-align: center;">
            <div style="max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0,0,0,0.1);">
                <img src="{self.horizontal_logo}" alt="XploreAI Logo" style="max-width: 150px; margin-bottom: 20px;">
                <h2 style="color: #333;">✉️ Verify Your Email</h2>
                <p style="color: #555;">Thank you for signing up for XploreAI! Please confirm your email address by clicking the button below:</p>
                <a href="{verification_link}" style="display: inline-block; padding: 12px 24px; font-size: 16px; font-weight: bold; color: white; background-color: #008CBA; border-radius: 5px; text-decoration: none; margin-top: 15px;">Verify My Email</a>
                <p style="color: #888; margin-top: 20px;">If you did not create this account, you can ignore this email.</p>
                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                <p style="color: #777; font-size: 12px;">© 2024 XploreAI. All rights reserved.</p>
            </div>
        </body>
        </html>
        """

        return self.send_email(to_email, subject, body)
