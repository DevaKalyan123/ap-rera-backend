import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_otp_email(to_email, otp):

    sender_email = "devakalyaneepi@gmail.com"

    app_password = "qwhxwmwflunoslwn"

    subject = "AP RERA Admin OTP"

    body = f"""
Hello Admin,

Your OTP is: {otp}

Do not share this OTP with anyone.

Regards,
AP RERA Team
"""

    msg = MIMEMultipart()

    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:

        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()

        server.login(sender_email, app_password)

        server.sendmail(
            sender_email,
            to_email,
            msg.as_string()
        )

        server.quit()

        print("MAIL SENT SUCCESSFULLY")

    except Exception as e:

        print("MAIL ERROR:", str(e))
        raise e