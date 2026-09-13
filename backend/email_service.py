import os
import smtplib
import ssl
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()


def send_verification_email(
    recipient: str,
    first_name: str,
    verification_url: str
):
    host = os.getenv("SMTP_HOST", "").strip()
    port = int(os.getenv("SMTP_PORT", "587"))
    username = os.getenv("SMTP_USERNAME", "").strip()
    password = os.getenv("SMTP_PASSWORD", "")
    sender = os.getenv("SMTP_FROM", "").strip() or username

    if not host or not username or not password or not sender:
        raise RuntimeError(
            "Email delivery is not configured. Set SMTP_HOST, SMTP_PORT, "
            "SMTP_USERNAME, SMTP_PASSWORD and SMTP_FROM in .env."
        )

    message = EmailMessage()
    message["Subject"] = "Verify your GatherUp email"
    message["From"] = sender
    message["To"] = recipient

    message.set_content(
        f"""Hi {first_name},

Welcome to GatherUp.

Please verify that you own this email address by opening the link below:

{verification_url}

This verification link expires in 30 minutes.

If you did not create a GatherUp account, you can safely ignore this email.

— GatherUp
"""
    )

    context = ssl.create_default_context()

    if port == 465:
        with smtplib.SMTP_SSL(host, port, context=context, timeout=20) as smtp:
            smtp.login(username, password)
            smtp.send_message(message)
        return

    with smtplib.SMTP(host, port, timeout=20) as smtp:
        smtp.ehlo()
        smtp.starttls(context=context)
        smtp.ehlo()
        smtp.login(username, password)
        smtp.send_message(message)
