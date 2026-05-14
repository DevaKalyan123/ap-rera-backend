import smtplib
from email.mime.text import MIMEText


def send_otp_email(to_email, otp):

    subject = "Your OTP Code"

    body = f"""
Your OTP is: {otp}

Do not share this OTP.
"""

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = "devakalyaneepi@gmail.com"
    msg["To"] = to_email

    # Gmail SMTP
    server = smtplib.SMTP("smtp.gmail.com", 587)

    # Start TLS Security
    server.starttls()

    # Login using Gmail + App Password
    server.login(
        "devakalyaneepi@gmail.com",
        "qwhxwmwflunoslwn"
    )

    # Send Mail
    server.sendmail(
        "devakalyaneepi@gmail.com",
        to_email,
        msg.as_string()
    )

    # Close Connection
    server.quit()

    print("OTP EMAIL SENT SUCCESSFULLY")