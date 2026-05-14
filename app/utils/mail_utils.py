import smtplib
from email.mime.text import MIMEText


def send_otp_email(to_email, otp):

    sender_email = "devakalyaneepi@gmail.com"

    app_password = "qwhxwmwflunoslwn"

    subject = "AP RERA OTP"

    body = f"Your OTP is: {otp}"

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:

        print("CONNECTING TO SMTP")

        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()

        print("LOGIN TO GMAIL")

        server.login(sender_email, app_password)

        print("SENDING MAIL")

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