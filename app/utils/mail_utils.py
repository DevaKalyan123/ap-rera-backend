import smtplib
from email.mime.text import MIMEText
from flask import current_app


def send_otp_email(to_email, otp):

    try:

        subject = "AP RERA Admin Login OTP"

        body = f"""
Hello Admin,

Your OTP for login is: {otp}

This OTP is valid for 5 minutes.

Do not share this OTP with anyone.

Thanks,
AP RERA Team
"""

        msg = MIMEText(body)

        msg["Subject"] = subject
        msg["From"] = current_app.config.get("FROM_EMAIL")
        msg["To"] = to_email

        smtp_host = current_app.config.get("SMTP_HOST")
        smtp_port = int(current_app.config.get("SMTP_PORT"))

        smtp_user = current_app.config.get("SMTP_USER")
        smtp_password = current_app.config.get("SMTP_PASSWORD")

        print("================================")
        print("SMTP HOST:", smtp_host)
        print("SMTP PORT:", smtp_port)
        print("SMTP USER:", smtp_user)
        print("TO EMAIL:", to_email)
        print("OTP:", otp)
        print("================================")

        server = smtplib.SMTP(smtp_host, smtp_port)

        server.starttls()

        server.login(smtp_user, smtp_password)

        server.sendmail(
            msg["From"],
            [to_email],
            msg.as_string()
        )

        server.quit()

        print("EMAIL SENT SUCCESSFULLY")

    except Exception as e:

        print("EMAIL ERROR:", str(e))
        raise e