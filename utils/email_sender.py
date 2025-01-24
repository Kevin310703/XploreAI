import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load biến môi trường
load_dotenv()

class EmailSender:
    @staticmethod
    def send_reset_email(to_email, reset_link):
        sender_email = os.getenv("EMAIL_USER")
        sender_password = os.getenv("EMAIL_PASS")
        smtp_server = os.getenv("EMAIL_HOST")
        smtp_port = int(os.getenv("EMAIL_PORT"))

        HORIZONTAL_LOGO = "http://localhost:8501/media/5d6da876718ec3ae41b5086b8d7826c77e9881e651246617b52b6cfe.png"

        subject = "Reset Your Password - XploreAI"

        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; text-align: center;">
            <div style="max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0,0,0,0.1);">
                <img src="{HORIZONTAL_LOGO}" alt="XploreAI Logo" style="max-width: 150px; margin-bottom: 20px;">
                <h2 style="color: #333;">🔑 Reset Your Password</h2>
                <p style="color: #555;">You requested to reset your password. Click the button below to reset it:</p>
                <a href="{reset_link}" style="
                    background-color: #008CBA; 
                    color: white; 
                    padding: 12px 20px; 
                    text-decoration: none; 
                    font-size: 16px; 
                    font-weight: bold; 
                    border-radius: 5px; 
                    display: inline-block;
                    margin: 20px 0;">
                    Reset Password
                </a>
                <p style="color: #888;">If you didn't request this, you can safely ignore this email.</p>
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
