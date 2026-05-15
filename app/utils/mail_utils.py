import os
import resend

# RESEND API KEY
resend.api_key = os.getenv("RESEND_API_KEY")


def send_email_otp(to_email, otp):

    try:

        params = {
            "from": "onboarding@resend.dev",
            "to": [to_email],
            "subject": "AP RERA OTP Verification",
            "html": f"""
                <h2>Your OTP is: {otp}</h2>

                <p>
                    This OTP is valid for 5 minutes.
                </p>

                <br>

                <p>
                    Regards,<br>
                    AP RERA
                </p>
            """,
        }

        resend.Emails.send(params)

        print("OTP MAIL SENT SUCCESSFULLY")
        print("MAIL SENT TO:", to_email)

    except Exception as e:

        print("MAIL ERROR:", str(e))