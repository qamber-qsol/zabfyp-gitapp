import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from dotenv import load_dotenv

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_otp_email(email_to: str, otp_code: str):
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2>SZABIST FYP Portal Verification</h2>
        <p>Your one-time password (OTP) is: <strong style="font-size: 24px; color: #0047AB;">{otp_code}</strong></p>
        <p>This code will expire in 10 minutes. Please enter it in the portal to verify your account and set your password.</p>
        <hr style="border: 1px solid #eee;" />
        <p style="font-size: 12px; color: #888;">If you did not request this, please contact the Computer Science department.</p>
    </div>
    """
    
    message = MessageSchema(
        subject="Your FYP Portal Verification Code",
        recipients=[email_to],
        body=html,
        subtype=MessageType.html
    )
    
    fm = FastMail(conf)
    await fm.send_message(message)