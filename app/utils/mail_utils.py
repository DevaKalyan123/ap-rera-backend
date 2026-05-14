import smtplib
from email.mime.text import MIMEText
from flask import current_app


def send_otp_email(to_email, otp):

    try:

        print("===================================")
        print("MAIL FUNCTION STARTED")
        print("TO EMAIL:", to_email)
        print("OTP:", otp)
        print("===================================")

        subject = "AP RERA Admin Login OTP"

        body = f"""
Hello,

Your OTP is: {otp}

Thank You,
AP RERA Team
"""

        msg = MIMEText(body)

        msg["Subject"] = subject
        msg["From"] = current_app.config.get("FROM_EMAIL")
        msg["To"] = to_email

        smtp_host = current_app.config.get("SMTP_HOST")
        smtp_port = int(current_app.config.get("SMTP_PORT", 587))
        smtp_user = current_app.config.get("SMTP_USER")
        smtp_password = current_app.config.get("SMTP_PASSWORD")

        print("SMTP HOST:", smtp_host)
        print("SMTP PORT:", smtp_port)
        print("SMTP USER:", smtp_user)

        server = smtplib.SMTP(smtp_host, smtp_port)

        server.starttls()

        server.login(smtp_user, smtp_password)

        print("SMTP LOGIN SUCCESS")

        server.sendmail(
            msg["From"],
            [to_email],
            msg.as_string()
        )

        print("EMAIL SENT SUCCESSFULLY")

        server.quit()

    except Exception as e:

        print("MAIL ERROR:", str(e))
        raise e