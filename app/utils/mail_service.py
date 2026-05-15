import os
import resend

# =========================================
# RESEND API KEY
# =========================================

resend.api_key = os.getenv("RESEND_API_KEY")


# =========================================
# COMMON SEND EMAIL FUNCTION
# =========================================

def send_email(to_email, subject, body):

    try:

        params = {

            "from": "onboarding@resend.dev",

            "to": [to_email],

            "subject": subject,

            "html": f"""
                <div style="font-family: Arial; padding: 20px;">
                    <pre style="font-size:16px;">{body}</pre>
                </div>
            """
        }

        resend.Emails.send(params)

        print("EMAIL SENT SUCCESSFULLY")
        print("MAIL SENT TO:", to_email)

        return True

    except Exception as e:

        print("EMAIL ERROR:", str(e))

        return False


# =========================================
# OTP EMAIL
# =========================================

def send_email_otp(to_email, otp):

    subject = "AP RERA OTP Verification"

    body = f"""
Dear Applicant,

Your OTP for verification is:

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
# CHANGE REQUEST APPROVAL
# =========================================

def send_change_request_approval_email(
    to_email,
    application_no
):

    body = f"""
Dear Applicant,

Your change request for application
{application_no}
has been approved.

Regards,
AP RERA
"""

    return send_email(
        to_email,
        "Change Request Approved",
        body
    )


# =========================================
# RENEWAL APPROVAL
# =========================================

def send_approval_email(
    to_email,
    application_no,
    expiry_date,
    certificate_path=None
):

    body = f"""
Dear Applicant,

Your renewal application has been APPROVED.

Application Number : {application_no}

Expiry Date : {expiry_date}

Regards,
AP RERA
"""

    return send_email(
        to_email,
        "AP RERA Renewal Approved",
        body
    )


# =========================================
# RENEWAL REJECTION
# =========================================

def send_rejection_email(
    to_email,
    application_no,
    remarks
):

    body = f"""
Dear Applicant,

Your renewal application has been REJECTED.

Application Number : {application_no}

Remarks:
{remarks}

Regards,
AP RERA
"""

    return send_email(
        to_email,
        "AP RERA Renewal Rejected",
        body
    )


# =========================================
# PROJECT APPROVAL
# =========================================

def send_project_approval_email(
    to_email,
    application_no,
    project_name,
    certificate_path=None
):

    body = f"""
Dear Applicant,

Your PROJECT REGISTRATION has been APPROVED.

Application Number : {application_no}

Project Name : {project_name}

Congratulations!

Regards,
AP RERA
"""

    return send_email(
        to_email,
        "AP RERA Project Approved",
        body
    )


# =========================================
# PROJECT REJECTION
# =========================================

def send_project_rejection_email(
    to_email,
    application_no,
    project_name,
    remarks
):

    body = f"""
Dear Applicant,

Your PROJECT REGISTRATION has been REJECTED.

Application Number : {application_no}

Project Name : {project_name}

Reason:
{remarks}

Regards,
AP RERA
"""

    return send_email(
        to_email,
        "AP RERA Project Rejected",
        body
    )


# =========================================
# AGENT CHANGE APPROVAL
# =========================================

def send_agent_change_request_approval_email(
    to_email,
    application_no,
    changed_fields=None
):

    changed_fields = changed_fields or []

    fields_text = "\n".join(changed_fields)

    body = f"""
Dear Applicant,

Your agent change request has been APPROVED.

Application Number : {application_no}

Updated Fields:
{fields_text}

Regards,
AP RERA
"""

    return send_email(
        to_email,
        f"Agent Change Request Approved - {application_no}",
        body
    )


# =========================================
# AGENT CHANGE REJECTION
# =========================================

def send_agent_change_request_rejection_email(
    to_email,
    application_no
):

    body = f"""
Dear Applicant,

Your agent change request has been REJECTED.

Application Number : {application_no}

Regards,
AP RERA
"""

    return send_email(
        to_email,
        f"Agent Change Request Rejected - {application_no}",
        body
    )


# =========================================
# COMPLAINT REJECTION
# =========================================

def send_complaint_rejection_email(
    email,
    name,
    subject_text,
    complaint_desc,
    admin_remark
):

    body = f"""
Dear {name},

Your complaint has been REJECTED.

Subject:
{subject_text}

Remarks:
{admin_remark}

Regards,
AP RERA
"""

    return send_email(
        email,
        f"Complaint Rejected - {subject_text}",
        body
    )


# =========================================
# COMPLAINT APPROVAL - COMPLAINANT
# =========================================

def send_complaint_approval_mail_complainant(
    email,
    name,
    subject_text,
    complaint_desc,
    admin_remark
):

    body = f"""
Dear {name},

Your complaint has been ACCEPTED.

Subject:
{subject_text}

Remarks:
{admin_remark}

Regards,
AP RERA
"""

    return send_email(
        email,
        f"Complaint Accepted - {subject_text}",
        body
    )


# =========================================
# COMPLAINT APPROVAL - RESPONDENT
# =========================================

def send_complaint_approval_mail_respondent(
    email,
    respondent_name,
    complainant_name,
    subject_text,
    complaint_desc,
    admin_remark
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


# =========================================
# COMPLAINT APPROVAL RESPONDENT WITH PDF
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


# =========================================
# COMPLAINT CLOSED - COMPLAINANT
# =========================================

def send_complaint_closed_mail_complainant(
    email,
    name,
    subject_text,
    complaint_desc,
    admin_remark
):

    body = f"""
Dear {name},

Your complaint has been CLOSED.

Subject:
{subject_text}

Final Remarks:
{admin_remark}

Regards,
AP RERA
"""

    return send_email(
        email,
        f"Complaint Closed - {subject_text}",
        body
    )


# =========================================
# COMPLAINT CLOSED - RESPONDENT
# =========================================

def send_complaint_closed_mail_respondent(
    email,
    respondent_name,
    complainant_name,
    subject_text,
    complaint_desc,
    admin_remark
):

    body = f"""
Dear {respondent_name},

The complaint filed against you has been CLOSED.

Complainant:
{complainant_name}

Subject:
{subject_text}

Final Remarks:
{admin_remark}

Regards,
AP RERA
"""

    return send_email(
        email,
        f"Complaint Closed - {subject_text}",
        body
    )