import resend

# RESEND API KEY
resend.api_key = "re_GoPMuG7Q_DK8Z1LPZw21PMhrnfvdWTWhM"


def send_otp_email(to_email, otp):

    try:

        params = {
            "from": "onboarding@resend.dev",
            "to": [to_email],
            "subject": "Your OTP Code",
            "html": f"""
                <h2>Your OTP is: {otp}</h2>
                <p>Do not share this OTP.</p>
            """,
        }

        resend.Emails.send(params)

        print("OTP MAIL SENT SUCCESSFULLY")

    except Exception as e:

        print("MAIL ERROR:", str(e))