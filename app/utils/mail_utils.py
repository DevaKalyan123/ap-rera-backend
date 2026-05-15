import os
import resend

# =========================================
# RESEND API KEY
# =========================================

resend.api_key = os.getenv("RESEND_API_KEY")


# =========================================
# COMMON SEND EMAIL
# =========================================

def send_email(to_email, subject, body):

    try:

        params = {

            "from": "onboarding@resend.dev",

            "to": [to_email],

            "subject": subject,

            "html": f"""
                <div style="font-family: Arial;">

                    <pre style="font-size:16px;">
{body}
                    </pre>

                </div>
            """,
        }

        resend.Emails.send(params)

        print("EMAIL SENT SUCCESSFULLY")
        print("MAIL SENT TO:", to_email)

        return True

    except Exception as e:

        print("MAIL ERROR:", str(e))

        return False


# =========================================
# OTP EMAIL
# =========================================

def send_email_otp(to_email, otp):

    subject = "AP RERA OTP Verification"

    body = f"""
Dear Applicant,

Your OTP is:

{otp}

This OTP is valid for 5 minutes.

Regards,
AP RERA
"""

    return send_email(
        to_email,
        subject,
        body
    )


# =========================================
# COMPLAINT APPROVAL MAIL
# =========================================

def send_complaint_approval_mail_respondent_with_pdf(
    email,
    respondent_name,
    complainant_name,
    subject_text,
    complaint_desc,
    admin_remark,
    pdf_file,
):

    body = f"""
Dear {respondent_name},

A complaint has been ACCEPTED against you.

Complainant:
{complainant_name}

Subject:
{subject_text}

Description:
{complaint_desc}

Remarks:
{admin_remark}

Regards,
AP RERA
"""

    return send_email(
        email,
        f"Complaint Against You - {subject_text}",
        body
    )