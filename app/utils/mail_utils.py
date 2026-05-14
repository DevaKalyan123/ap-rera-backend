import smtplib
from email.mime.text import MIMEText
from flask import current_app
import logging


def send_otp_email(to_email, otp):

    try:

        subject = "OTP for Admin Login"

        body = f"""
Hello,

Your OTP is: {otp}

This OTP is valid for 5 minutes.
"""

        msg = MIMEText(body)

        msg["Subject"] = subject
        msg["From"] = current_app.config.get("FROM_EMAIL")
        msg["To"] = to_email

        logging.error("MAIL STARTED")

        server = smtplib.SMTP(
            current_app.config.get("SMTP_HOST"),
            int(current_app.config.get("SMTP_PORT"))
        )

        server.starttls()

        logging.error("SMTP CONNECTED")

        server.login(
            current_app.config.get("SMTP_USER"),
            current_app.config.get("SMTP_PASSWORD")
        )

        logging.error("SMTP LOGIN SUCCESS")

        server.sendmail(
            msg["From"],
            [to_email],
            msg.as_string()
        )

        logging.error("MAIL SENT SUCCESSFULLY")

        server.quit()

    except Exception as e:

        logging.error(f"MAIL ERROR: {str(e)}")
        raise e