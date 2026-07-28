import os
from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr

from app.core.config import settings

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME or os.getenv("MAIL_USERNAME", ""),
    MAIL_PASSWORD=settings.MAIL_PASSWORD or os.getenv("MAIL_PASSWORD", ""),
    MAIL_FROM=settings.MAIL_FROM or os.getenv("MAIL_FROM", os.getenv("MAIL_USERNAME", "noreply@example.com")),
    MAIL_PORT=settings.MAIL_PORT or int(os.getenv("MAIL_PORT", "587")),
    MAIL_SERVER=settings.MAIL_SERVER or os.getenv("MAIL_SERVER", "smtp.gmail.com"),
    MAIL_STARTTLS=settings.MAIL_STARTTLS if settings.MAIL_STARTTLS is not None else os.getenv("MAIL_STARTTLS", "True").lower() in ("true", "1", "t"),
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS if settings.MAIL_SSL_TLS is not None else os.getenv("MAIL_SSL_TLS", "False").lower() in ("true", "1", "t"),
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_otp_email(email_to: EmailStr, otp_code: str) -> None:
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f4f6f8;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 550px;
                margin: 0 auto;
                background: #ffffff;
                border-radius: 8px;
                padding: 30px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
                border: 1px solid #e1e4e8;
            }}
            .header {{
                text-align: center;
                border-bottom: 2px solid #0047AB;
                padding-bottom: 15px;
                margin-bottom: 20px;
            }}
            .header h2 {{
                color: #0047AB;
                margin: 0;
                font-size: 24px;
            }}
            .otp-box {{
                background-color: #f0f4f8;
                border: 1px dashed #0047AB;
                border-radius: 6px;
                padding: 15px;
                text-align: center;
                margin: 25px 0;
            }}
            .otp-code {{
                font-size: 32px;
                font-weight: bold;
                letter-spacing: 6px;
                color: #0047AB;
            }}
            .footer {{
                margin-top: 30px;
                font-size: 12px;
                color: #888888;
                text-align: center;
                border-top: 1px solid #eee;
                padding-top: 15px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>SZABIST FYP Portal</h2>
            </div>
            <p>Hello,</p>
            <p>Your one-time password (OTP) for account verification and password setup is:</p>
            <div class="otp-box">
                <span class="otp-code">{otp_code}</span>
            </div>
            <p>This verification code will expire in <strong>15 minutes</strong>. Please enter this code in the portal to verify your account.</p>
            <div class="footer">
                <p>If you did not request this email, please ignore this message.</p>
            </div>
        </div>
    </body>
    </html>
    """

    message = MessageSchema(
        subject="Your FYP Portal OTP Verification Code",
        recipients=[email_to],
        body=html_content,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message)