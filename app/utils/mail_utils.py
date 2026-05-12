import smtplib
from email.mime.text import MIMEText
from flask import current_app


def send_otp_email(to_email, otp):

    subject = "AP RERA Admin Login OTP"

    body = f"""
Hello,

Your OTP for AP RERA Admin Login is:

{otp}

This OTP is valid for 5 minutes.

Do not share this OTP with anyone.

Thank You,
AP RERA Team
"""

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = current_app.config.get("FROM_EMAIL")
    msg["To"] = to_email

    try:

        print("SMTP HOST:", current_app.config.get("SMTP_HOST"))
        print("SMTP USER:", current_app.config.get("SMTP_USER"))

        server = smtplib.SMTP(
            current_app.config.get("SMTP_HOST"),
            int(current_app.config.get("SMTP_PORT", 587))
        )

        server.starttls()

        server.login(
            current_app.config.get("SMTP_USER"),
            current_app.config.get("SMTP_PASSWORD")
        )

        server.sendmail(
            msg["From"],
            [to_email],
            msg.as_string()
        )

        print("OTP MAIL SENT SUCCESSFULLY")

    except Exception as e:

        print("MAIL ERROR:", str(e))

        raise e

    finally:
        try:
            server.quit()
        except:
            pass