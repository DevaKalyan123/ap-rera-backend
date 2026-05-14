import smtplib
from email.mime.text import MIMEText


def send_otp_email(to_email, otp):

    sender_email = "devakalyaneepi@gmail.com"

    smtp_password = ""

    subject = "AP RERA OTP Verification"

    body = f"""
Hello,

Your OTP is: {otp}

Do not share this OTP with anyone.

Thank You,
AP RERA
"""

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    print("CONNECTING BREVO SMTP")

    server = smtplib.SMTP(
        "smtp-relay.brevo.com",
        587
    )

    server.starttls()

    print("LOGIN SMTP")

    server.login(
        sender_email,
        smtp_password
    )

    print("SENDING EMAIL")

    server.sendmail(
        sender_email,
        to_email,
        msg.as_string()
    )

    server.quit()

    print("MAIL SENT SUCCESSFULLY")