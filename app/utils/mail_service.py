# import smtplib
# import os
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.application import MIMEApplication


# def send_email_otp(to_email, otp):
#     smtp_host = os.getenv("SMTP_HOST")
#     smtp_port = int(os.getenv("SMTP_PORT"))
#     smtp_user = os.getenv("SMTP_USER")
#     smtp_password = os.getenv("SMTP_PASSWORD")
#     from_email = os.getenv("FROM_EMAIL")

#     subject = "AP RERA OTP Verification"
#     body = f"""
# Dear Applicant,

# Your OTP for verification is: {otp}

# This OTP is valid for 5 minutes.

# Regards,
# AP RERA
# """

#     msg = MIMEMultipart()
#     msg["From"] = from_email
#     msg["To"] = to_email
#     msg["Subject"] = subject
#     msg.attach(MIMEText(body, "plain"))

#     server = smtplib.SMTP(smtp_host, smtp_port)
#     server.starttls()
#     server.login(smtp_user, smtp_password)
#     server.sendmail(from_email, to_email, msg.as_string())
#     server.quit()

# def send_change_request_approval_email(to_email, application_no):
#     send_email(
#         to_email,
#         "Change Request Approved",
#         f"Your change request for application {application_no} has been approved."
#     )    

#     #code addded by ravi 

# def send_approval_email(to_email, application_no, expiry_date, certificate_path):

#     try:

#         smtp_host = os.getenv("SMTP_HOST")
#         smtp_port = int(os.getenv("SMTP_PORT"))
#         smtp_user = os.getenv("SMTP_USER")
#         smtp_password = os.getenv("SMTP_PASSWORD")
#         from_email = os.getenv("FROM_EMAIL")

#         print("===== MAIL DEBUG =====")
#         print("SMTP HOST:", smtp_host)
#         print("SMTP PORT:", smtp_port)
#         print("SMTP USER:", smtp_user)
#         print("TO EMAIL:", to_email)
#         print("CERTIFICATE:", certificate_path)

#         subject = "AP RERA Renewal Approved"

#         body = f"""
# Dear Applicant,

# Your renewal application has been APPROVED.

# Application Number : {application_no}
# Expiry Date : {expiry_date}

# Please find your certificate attached.

# Regards,
# AP RERA
# """

#         msg = MIMEMultipart()
#         msg["From"] = from_email
#         msg["To"] = to_email
#         msg["Subject"] = subject

#         msg.attach(MIMEText(body, "plain"))

#         with open(certificate_path, "rb") as f:
#             part = MIMEApplication(f.read(), Name=os.path.basename(certificate_path))
#             part["Content-Disposition"] = f'attachment; filename="{os.path.basename(certificate_path)}"'
#             msg.attach(part)

#         print("Connecting SMTP...")

#         server = smtplib.SMTP(smtp_host, smtp_port)
#         server.starttls()

#         print("Logging in SMTP...")

#         server.login(smtp_user, smtp_password)

#         print("Sending email...")

#         server.sendmail(from_email, to_email, msg.as_string())

#         print("EMAIL SENT SUCCESSFULLY")

#         server.quit()

#     except Exception as e:

#         print("EMAIL ERROR:", str(e))



    
# def send_rejection_email(to_email, application_no, remarks):

#     smtp_host = os.getenv("SMTP_HOST")
#     smtp_port = int(os.getenv("SMTP_PORT"))
#     smtp_user = os.getenv("SMTP_USER")
#     smtp_password = os.getenv("SMTP_PASSWORD")
#     from_email = os.getenv("FROM_EMAIL")

#     subject = "AP RERA Renewal Rejected"

#     body = f"""
# Dear Applicant,

# Your renewal application has been REJECTED.

# Application Number : {application_no}

# Remarks:
# {remarks}

# Regards,
# AP RERA
# """

#     msg = MIMEMultipart()
#     msg["From"] = from_email
#     msg["To"] = to_email
#     msg["Subject"] = subject

#     msg.attach(MIMEText(body, "plain"))

#     server = smtplib.SMTP(smtp_host, smtp_port)
#     server.starttls()
#     server.login(smtp_user, smtp_password)
#     server.sendmail(from_email, to_email, msg.as_string())
#     server.quit()
    
    
    
# def send_project_approval_email(to_email, application_no, project_name, certificate_path):

#     try:

#         smtp_host = os.getenv("SMTP_HOST")
#         smtp_port = int(os.getenv("SMTP_PORT"))
#         smtp_user = os.getenv("SMTP_USER")
#         smtp_password = os.getenv("SMTP_PASSWORD")
#         from_email = os.getenv("FROM_EMAIL")

#         subject = "AP RERA Project Approved"

#         body = f"""
# Dear Applicant,

# Your PROJECT REGISTRATION has been APPROVED.

# Application Number : {application_no}
# Project Name       : {project_name}

# Please find your APPROVAL CERTIFICATE attached.

# Congratulations! Your project is now registered under AP RERA.

# Regards,
# AP RERA
# """

#         msg = MIMEMultipart()
#         msg["From"] = from_email
#         msg["To"] = to_email
#         msg["Subject"] = subject

#         msg.attach(MIMEText(body, "plain"))

#         # ✅ Attach certificate
#         with open(certificate_path, "rb") as f:
#             part = MIMEApplication(f.read(), Name=os.path.basename(certificate_path))
#             part["Content-Disposition"] = f'attachment; filename="{os.path.basename(certificate_path)}"'
#             msg.attach(part)

#         print("Sending Project Approval Email...")

#         server = smtplib.SMTP(smtp_host, smtp_port)
#         server.starttls()
#         server.login(smtp_user, smtp_password)
#         server.sendmail(from_email, to_email, msg.as_string())
#         server.quit()

#         print("PROJECT APPROVAL EMAIL SENT ✅")

#     except Exception as e:
#         print("PROJECT APPROVAL EMAIL ERROR:", str(e))
        
        


# def send_project_rejection_email(to_email, application_no, project_name, remarks):

#     try:

#         smtp_host = os.getenv("SMTP_HOST")
#         smtp_port = int(os.getenv("SMTP_PORT"))
#         smtp_user = os.getenv("SMTP_USER")
#         smtp_password = os.getenv("SMTP_PASSWORD")
#         from_email = os.getenv("FROM_EMAIL")

#         subject = "AP RERA Project Rejected"

#         body = f"""
# Dear Applicant,

# Your PROJECT REGISTRATION has been REJECTED.

# Application Number : {application_no}
# Project Name       : {project_name}

# Reason for Rejection:
# {remarks}

# Please review the remarks and re-apply after corrections.

# Regards,
# AP RERA
# """

#         msg = MIMEMultipart()
#         msg["From"] = from_email
#         msg["To"] = to_email
#         msg["Subject"] = subject

#         msg.attach(MIMEText(body, "plain"))

#         print("Sending Project Rejection Email...")

#         server = smtplib.SMTP(smtp_host, smtp_port)
#         server.starttls()
#         server.login(smtp_user, smtp_password)
#         server.sendmail(from_email, to_email, msg.as_string())
#         server.quit()

#         print("PROJECT REJECTION EMAIL SENT ❌")

#     except Exception as e:
#         print("PROJECT REJECTION EMAIL ERROR:", str(e))
        
# def send_email(to_email, subject, body):

#     try:
#         smtp_host = os.getenv("SMTP_HOST")
#         smtp_port = int(os.getenv("SMTP_PORT"))
#         smtp_user = os.getenv("SMTP_USER")
#         smtp_password = os.getenv("SMTP_PASSWORD")
#         from_email = os.getenv("FROM_EMAIL")

#         msg = MIMEMultipart()
#         msg["From"] = from_email
#         msg["To"] = to_email
#         msg["Subject"] = subject

#         msg.attach(MIMEText(body, "plain"))

#         print("Sending reminder email...")

#         server = smtplib.SMTP(smtp_host, smtp_port)
#         server.starttls()
#         server.login(smtp_user, smtp_password)
#         server.sendmail(from_email, to_email, msg.as_string())
#         server.quit()

#         print("✅ Reminder email sent")

#     except Exception as e:
#         print("❌ Reminder email error:", str(e))

# def send_approval_email(to_email, application_no, expiry_date, certificate_path):

#     try:

#         smtp_host = os.getenv("SMTP_HOST")
#         smtp_port = int(os.getenv("SMTP_PORT"))
#         smtp_user = os.getenv("SMTP_USER")
#         smtp_password = os.getenv("SMTP_PASSWORD")
#         from_email = os.getenv("FROM_EMAIL")

#         print("===== MAIL DEBUG =====")
#         print("SMTP HOST:", smtp_host)
#         print("SMTP PORT:", smtp_port)
#         print("SMTP USER:", smtp_user)
#         print("TO EMAIL:", to_email)
#         print("CERTIFICATE:", certificate_path)

#         subject = "AP RERA Renewal Approved"

#         body = f"""
# Dear Applicant,

# Your renewal application has been APPROVED.

# Application Number : {application_no}
# Expiry Date : {expiry_date}

# Please find your certificate attached.

# Regards,
# AP RERA
# """

#         msg = MIMEMultipart()
#         msg["From"] = from_email
#         msg["To"] = to_email
#         msg["Subject"] = subject

#         msg.attach(MIMEText(body, "plain"))

#         with open(certificate_path, "rb") as f:
#             part = MIMEApplication(f.read(), Name=os.path.basename(certificate_path))
#             part["Content-Disposition"] = (
#                 f'attachment; filename="{os.path.basename(certificate_path)}"'
#             )
#             msg.attach(part)

#         print("Connecting SMTP...")

#         server = smtplib.SMTP(smtp_host, smtp_port)
#         server.starttls()

#         print("Logging in SMTP...")

#         server.login(smtp_user, smtp_password)

#         print("Sending email...")

#         server.sendmail(from_email, to_email, msg.as_string())

#         print("EMAIL SENT SUCCESSFULLY")

#         server.quit()

#     except Exception as e:

#         print("EMAIL ERROR:", str(e))


# def send_rejection_email(to_email, application_no, remarks):

#     smtp_host = os.getenv("SMTP_HOST")
#     smtp_port = int(os.getenv("SMTP_PORT"))
#     smtp_user = os.getenv("SMTP_USER")
#     smtp_password = os.getenv("SMTP_PASSWORD")
#     from_email = os.getenv("FROM_EMAIL")

#     subject = "AP RERA Renewal Rejected"

#     body = f"""
# Dear Applicant,

# Your renewal application has been REJECTED.

# Application Number : {application_no}

# Remarks:
# {remarks}

# Regards,
# AP RERA
# """

#     msg = MIMEMultipart()
#     msg["From"] = from_email
#     msg["To"] = to_email
#     msg["Subject"] = subject

#     msg.attach(MIMEText(body, "plain"))

#     server = smtplib.SMTP(smtp_host, smtp_port)
#     server.starttls()
#     server.login(smtp_user, smtp_password)
#     server.sendmail(from_email, to_email, msg.as_string())
#     server.quit()


# def send_change_request_approval_email(email, ref_no, changes):

#     smtp_host = os.getenv("SMTP_HOST")
#     smtp_port = int(os.getenv("SMTP_PORT"))
#     smtp_user = os.getenv("SMTP_USER")
#     smtp_password = os.getenv("SMTP_PASSWORD")
#     from_email = os.getenv("FROM_EMAIL")

#     subject = f"Change Request Approved - {ref_no}"

#     change_text = ""
#     for i, c in enumerate(changes, 1):
#         change_text += f"""
# {i}. {c['field']}
#    Old: {c['old']}
#    New: {c['new']}
# """

#     body = f"""
# Dear User,

# Your change request ({ref_no}) has been APPROVED.

# Changed Details:
# {change_text}

# Regards,
# AP RERA
# """

#     msg = MIMEMultipart()
#     msg["From"] = from_email
#     msg["To"] = email
#     msg["Subject"] = subject

#     msg.attach(MIMEText(body, "plain"))

#     server = smtplib.SMTP(smtp_host, smtp_port)
#     server.starttls()
#     server.login(smtp_user, smtp_password)
#     server.sendmail(from_email, email, msg.as_string())
#     server.quit()


# def send_complaint_rejection_email(
#     email, name, subject_text, complaint_desc, admin_remark
# ):

#     smtp_host = os.getenv("SMTP_HOST")
#     smtp_port = int(os.getenv("SMTP_PORT"))
#     smtp_user = os.getenv("SMTP_USER")
#     smtp_password = os.getenv("SMTP_PASSWORD")
#     from_email = os.getenv("FROM_EMAIL")

#     subject = f"Complaint Rejected - {subject_text}"

#     body = f"""
# Dear {name},

# Your complaint has been REJECTED.

# ----------------------------------------
# Complaint Details
# ----------------------------------------

# Subject:
# {subject_text}

# Description:
# {complaint_desc}

# Admin Remarks:
# {admin_remark}

# ----------------------------------------

# If you have any queries, please contact support.

# Regards,
# AP RERA Team
# """

#     msg = MIMEMultipart()
#     msg["From"] = from_email
#     msg["To"] = email
#     msg["Subject"] = subject

#     msg.attach(MIMEText(body, "plain"))

#     server = smtplib.SMTP(smtp_host, smtp_port)
#     server.starttls()
#     server.login(smtp_user, smtp_password)
#     server.sendmail(from_email, email, msg.as_string())
#     server.quit()


# def send_complaint_approval_mail_complainant(
#     email, name, subject_text, complaint_desc, admin_remark
# ):

#     smtp_host = os.getenv("SMTP_HOST")
#     smtp_port = int(os.getenv("SMTP_PORT"))
#     smtp_user = os.getenv("SMTP_USER")
#     smtp_password = os.getenv("SMTP_PASSWORD")
#     from_email = os.getenv("FROM_EMAIL")

#     subject = f"Complaint Accepted - {subject_text}"

#     body = f"""
# Dear {name},

# We are pleased to inform you that your complaint has been ACCEPTED by AP RERA.

# ----------------------------------------
# Complaint Details
# ----------------------------------------

# Subject:
# {subject_text}

# Description:
# {complaint_desc}

# Authority Remarks:
# {admin_remark}

# ----------------------------------------

# Further proceedings will be initiated, and you will be notified accordingly.

# Regards,
# AP RERA Authority
# """

#     msg = MIMEMultipart()
#     msg["From"] = from_email
#     msg["To"] = email
#     msg["Subject"] = subject

#     msg.attach(MIMEText(body, "plain"))

#     server = smtplib.SMTP(smtp_host, smtp_port)
#     server.starttls()
#     server.login(smtp_user, smtp_password)
#     server.sendmail(from_email, email, msg.as_string())
#     server.quit()


# def send_complaint_approval_mail_respondent(
#     email, respondent_name, complainant_name, subject_text, complaint_desc, admin_remark
# ):

#     smtp_host = os.getenv("SMTP_HOST")
#     smtp_port = int(os.getenv("SMTP_PORT"))
#     smtp_user = os.getenv("SMTP_USER")
#     smtp_password = os.getenv("SMTP_PASSWORD")
#     from_email = os.getenv("FROM_EMAIL")

#     subject = f"Notice: Complaint Filed Against You - {subject_text}"

#     body = f"""
# Dear {respondent_name},

# This is to inform you that a complaint has been ACCEPTED by AP RERA against you.

# ----------------------------------------
# Complaint Details
# ----------------------------------------

# Complainant Name:
# {complainant_name}

# Subject:
# {subject_text}

# Description:
# {complaint_desc}

# Authority Remarks:
# {admin_remark}

# ----------------------------------------

# You are requested to respond as per AP RERA guidelines.

# Regards,
# AP RERA Authority
# """

#     msg = MIMEMultipart()
#     msg["From"] = from_email
#     msg["To"] = email
#     msg["Subject"] = subject

#     msg.attach(MIMEText(body, "plain"))

#     server = smtplib.SMTP(smtp_host, smtp_port)
#     server.starttls()
#     server.login(smtp_user, smtp_password)
#     server.sendmail(from_email, email, msg.as_string())
#     server.quit()


# def send_complaint_approval_mail_respondent_with_pdf(
#     email,
#     respondent_name,
#     complainant_name,
#     subject_text,
#     complaint_desc,
#     admin_remark,
#     pdf_file,
# ):

#     smtp_host = os.getenv("SMTP_HOST")
#     smtp_port = int(os.getenv("SMTP_PORT"))
#     smtp_user = os.getenv("SMTP_USER")
#     smtp_password = os.getenv("SMTP_PASSWORD")
#     from_email = os.getenv("FROM_EMAIL")

#     subject = f"Notice: Complaint Filed Against You - {subject_text}"

#     body = f"""
# Dear {respondent_name},

# This is to inform you that a complaint has been ACCEPTED by AP RERA against you.

# ----------------------------------------
# Complaint Details
# ----------------------------------------

# Complainant Name:
# {complainant_name}

# Subject:
# {subject_text}

# Description:
# {complaint_desc}

# Authority Remarks:
# {admin_remark}

# ----------------------------------------

# Please find the attached notice.

# Regards,
# AP RERA Authority
# """

#     msg = MIMEMultipart()
#     msg["From"] = from_email
#     msg["To"] = email
#     msg["Subject"] = subject

#     msg.attach(MIMEText(body, "plain"))

#     # ✅ attach PDF from request directly
#     if pdf_file:
#         part = MIMEApplication(pdf_file.read(), Name=pdf_file.filename)
#         part["Content-Disposition"] = f'attachment; filename="{pdf_file.filename}"'
#         msg.attach(part)

#     server = smtplib.SMTP(smtp_host, smtp_port)
#     server.starttls()
#     server.login(smtp_user, smtp_password)
#     server.sendmail(from_email, email, msg.as_string())
#     server.quit()


# def send_complaint_closed_mail_complainant(
#     email, name, subject_text, complaint_desc, admin_remark
# ):
#     smtp_host = os.getenv("SMTP_HOST")
#     smtp_port = int(os.getenv("SMTP_PORT"))
#     smtp_user = os.getenv("SMTP_USER")
#     smtp_password = os.getenv("SMTP_PASSWORD")
#     from_email = os.getenv("FROM_EMAIL")

#     subject = f"Complaint Closed - {subject_text}"

#     body = f"""
# Dear {name},

# Your complaint has been CLOSED by AP RERA.

# ----------------------------------------
# Complaint Details
# ----------------------------------------

# Subject:
# {subject_text}

# Description:
# {complaint_desc}

# Final Remarks:
# {admin_remark}

# ----------------------------------------

# Thank you for using AP RERA services.

# Regards,
# AP RERA Authority
# """

#     msg = MIMEMultipart()
#     msg["From"] = from_email
#     msg["To"] = email
#     msg["Subject"] = subject

#     msg.attach(MIMEText(body, "plain"))

#     server = smtplib.SMTP(smtp_host, smtp_port)
#     server.starttls()
#     server.login(smtp_user, smtp_password)
#     server.sendmail(from_email, email, msg.as_string())
#     server.quit()


# # ================= CLOSED MAIL - RESPONDENT =================
# def send_complaint_closed_mail_respondent(
#     email, respondent_name, complainant_name, subject_text, complaint_desc, admin_remark
# ):
#     smtp_host = os.getenv("SMTP_HOST")
#     smtp_port = int(os.getenv("SMTP_PORT"))
#     smtp_user = os.getenv("SMTP_USER")
#     smtp_password = os.getenv("SMTP_PASSWORD")
#     from_email = os.getenv("FROM_EMAIL")

#     subject = f"Complaint Closed - {subject_text}"

#     body = f"""
# Dear {respondent_name},

# The complaint filed against you has been CLOSED by AP RERA.

# ----------------------------------------
# Complaint Details
# ----------------------------------------

# Complainant Name:
# {complainant_name}

# Subject:
# {subject_text}

# Description:
# {complaint_desc}

# Final Remarks:
# {admin_remark}

# ----------------------------------------

# No further action is required.

# Regards,
# AP RERA Authority
# """

#     msg = MIMEMultipart()
#     msg["From"] = from_email
#     msg["To"] = email
#     msg["Subject"] = subject

#     msg.attach(MIMEText(body, "plain"))

#     server = smtplib.SMTP(smtp_host, smtp_port)
#     server.starttls()
#     server.login(smtp_user, smtp_password)
#     server.sendmail(from_email, email, msg.as_string())
#     server.quit()



import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_email_otp(to_email, otp):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("FROM_EMAIL")

    subject = "AP RERA OTP Verification"
    body = f"""
Dear Applicant,

Your OTP for verification is: {otp}

This OTP is valid for 5 minutes.

Regards,
AP RERA
"""

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()

def send_change_request_approval_email(to_email, application_no):
    send_email(
        to_email,
        "Change Request Approved",
        f"Your change request for application {application_no} has been approved."
    )    

    #code addded by ravi 

def send_approval_email(to_email, application_no, expiry_date, certificate_path):

    try:

        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = int(os.getenv("SMTP_PORT"))
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")
        from_email = os.getenv("FROM_EMAIL")

        print("===== MAIL DEBUG =====")
        print("SMTP HOST:", smtp_host)
        print("SMTP PORT:", smtp_port)
        print("SMTP USER:", smtp_user)
        print("TO EMAIL:", to_email)
        print("CERTIFICATE:", certificate_path)

        subject = "AP RERA Renewal Approved"

        body = f"""
Dear Applicant,

Your renewal application has been APPROVED.

Application Number : {application_no}
Expiry Date : {expiry_date}

Please find your certificate attached.

Regards,
AP RERA
"""

        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        with open(certificate_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(certificate_path))
            part["Content-Disposition"] = f'attachment; filename="{os.path.basename(certificate_path)}"'
            msg.attach(part)

        print("Connecting SMTP...")

        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()

        print("Logging in SMTP...")

        server.login(smtp_user, smtp_password)

        print("Sending email...")

        server.sendmail(from_email, to_email, msg.as_string())

        print("EMAIL SENT SUCCESSFULLY")

        server.quit()

    except Exception as e:

        print("EMAIL ERROR:", str(e))



    
def send_rejection_email(to_email, application_no, remarks):

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("FROM_EMAIL")

    subject = "AP RERA Renewal Rejected"

    body = f"""
Dear Applicant,

Your renewal application has been REJECTED.

Application Number : {application_no}

Remarks:
{remarks}

Regards,
AP RERA
"""

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()
    
    
    
def send_project_approval_email(to_email, application_no, project_name, certificate_path):

    try:

        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = int(os.getenv("SMTP_PORT"))
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")
        from_email = os.getenv("FROM_EMAIL")

        subject = "AP RERA Project Approved"

        body = f"""
Dear Applicant,

Your PROJECT REGISTRATION has been APPROVED.

Application Number : {application_no}
Project Name       : {project_name}

Please find your APPROVAL CERTIFICATE attached.

Congratulations! Your project is now registered under AP RERA.

Regards,
AP RERA
"""

        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        # ✅ Attach certificate
        with open(certificate_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(certificate_path))
            part["Content-Disposition"] = f'attachment; filename="{os.path.basename(certificate_path)}"'
            msg.attach(part)

        print("Sending Project Approval Email...")

        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

        print("PROJECT APPROVAL EMAIL SENT ✅")

    except Exception as e:
        print("PROJECT APPROVAL EMAIL ERROR:", str(e))
        
        


def send_project_rejection_email(to_email, application_no, project_name, remarks):

    try:

        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = int(os.getenv("SMTP_PORT"))
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")
        from_email = os.getenv("FROM_EMAIL")

        subject = "AP RERA Project Rejected"

        body = f"""
Dear Applicant,

Your PROJECT REGISTRATION has been REJECTED.

Application Number : {application_no}
Project Name       : {project_name}

Reason for Rejection:
{remarks}

Please review the remarks and re-apply after corrections.

Regards,
AP RERA
"""

        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        print("Sending Project Rejection Email...")

        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

        print("PROJECT REJECTION EMAIL SENT ❌")

    except Exception as e:
        print("PROJECT REJECTION EMAIL ERROR:", str(e))
        
def send_email(to_email, subject, body):

    try:
        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = int(os.getenv("SMTP_PORT"))
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")
        from_email = os.getenv("FROM_EMAIL")

        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        print("Sending reminder email...")

        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        return True

        print("✅ Reminder email sent")

    except Exception as e:
        return False
        print("❌ Reminder email error:", str(e))


def send_agent_change_request_approval_email(
    to_email, application_no, changed_fields=None
):
    changed_fields = changed_fields or []
    if changed_fields:
        lines = "\n".join(
            f"{index}. {field}" for index, field in enumerate(changed_fields, 1)
        )
        details_block = f"""
Updated Details:
{lines}
"""
    else:
        details_block = ""

    body = f"""
Dear Applicant,

Your agent change request has been APPROVED.

Application Number : {application_no}

{details_block}
Your requested details have been updated successfully.

Regards,
AP RERA
"""

    return send_email(
        to_email,
        f"AP RERA Agent Change Request Approved - {application_no}",
        body
    )


def send_agent_change_request_rejection_email(to_email, application_no):
    body = f"""
Dear Applicant,

Your agent change request has been REJECTED.

Application Number : {application_no}

Please login to the portal for more details.

Regards,
AP RERA
"""

    return send_email(
        to_email,
        f"AP RERA Agent Change Request Rejected - {application_no}",
        body
    )

def send_approval_email(to_email, application_no, expiry_date, certificate_path):

    try:

        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = int(os.getenv("SMTP_PORT"))
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")
        from_email = os.getenv("FROM_EMAIL")

        print("===== MAIL DEBUG =====")
        print("SMTP HOST:", smtp_host)
        print("SMTP PORT:", smtp_port)
        print("SMTP USER:", smtp_user)
        print("TO EMAIL:", to_email)
        print("CERTIFICATE:", certificate_path)

        subject = "AP RERA Renewal Approved"

        body = f"""
Dear Applicant,

Your renewal application has been APPROVED.

Application Number : {application_no}
Expiry Date : {expiry_date}

Please find your certificate attached.

Regards,
AP RERA
"""

        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        with open(certificate_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(certificate_path))
            part["Content-Disposition"] = (
                f'attachment; filename="{os.path.basename(certificate_path)}"'
            )
            msg.attach(part)

        print("Connecting SMTP...")

        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()

        print("Logging in SMTP...")

        server.login(smtp_user, smtp_password)

        print("Sending email...")

        server.sendmail(from_email, to_email, msg.as_string())

        print("EMAIL SENT SUCCESSFULLY")

        server.quit()

    except Exception as e:

        print("EMAIL ERROR:", str(e))


def send_rejection_email(to_email, application_no, remarks):

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("FROM_EMAIL")

    subject = "AP RERA Renewal Rejected"

    body = f"""
Dear Applicant,

Your renewal application has been REJECTED.

Application Number : {application_no}

Remarks:
{remarks}

Regards,
AP RERA
"""

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()


def send_change_request_approval_email(email, ref_no, changes):

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("FROM_EMAIL")

    subject = f"Change Request Approved - {ref_no}"

    change_text = ""
    for i, c in enumerate(changes, 1):
        change_text += f"""
{i}. {c['field']}
   Old: {c['old']}
   New: {c['new']}
"""

    body = f"""
Dear User,

Your change request ({ref_no}) has been APPROVED.

Changed Details:
{change_text}

Regards,
AP RERA
"""

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.sendmail(from_email, email, msg.as_string())
    server.quit()


def send_complaint_rejection_email(
    email, name, subject_text, complaint_desc, admin_remark
):

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("FROM_EMAIL")

    subject = f"Complaint Rejected - {subject_text}"

    body = f"""
Dear {name},

Your complaint has been REJECTED.

----------------------------------------
Complaint Details
----------------------------------------

Subject:
{subject_text}

Description:
{complaint_desc}

Admin Remarks:
{admin_remark}

----------------------------------------

If you have any queries, please contact support.

Regards,
AP RERA Team
"""

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.sendmail(from_email, email, msg.as_string())
    server.quit()


def send_complaint_approval_mail_complainant(
    email, name, subject_text, complaint_desc, admin_remark
):

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("FROM_EMAIL")

    subject = f"Complaint Accepted - {subject_text}"

    body = f"""
Dear {name},

We are pleased to inform you that your complaint has been ACCEPTED by AP RERA.

----------------------------------------
Complaint Details
----------------------------------------

Subject:
{subject_text}

Description:
{complaint_desc}

Authority Remarks:
{admin_remark}

----------------------------------------

Further proceedings will be initiated, and you will be notified accordingly.

Regards,
AP RERA Authority
"""

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.sendmail(from_email, email, msg.as_string())
    server.quit()


def send_complaint_approval_mail_respondent(
    email, respondent_name, complainant_name, subject_text, complaint_desc, admin_remark
):

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("FROM_EMAIL")

    subject = f"Notice: Complaint Filed Against You - {subject_text}"

    body = f"""
Dear {respondent_name},

This is to inform you that a complaint has been ACCEPTED by AP RERA against you.

----------------------------------------
Complaint Details
----------------------------------------

Complainant Name:
{complainant_name}

Subject:
{subject_text}

Description:
{complaint_desc}

Authority Remarks:
{admin_remark}

----------------------------------------

You are requested to respond as per AP RERA guidelines.

Regards,
AP RERA Authority
"""

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.sendmail(from_email, email, msg.as_string())
    server.quit()


def send_complaint_approval_mail_respondent_with_pdf(
    email,
    respondent_name,
    complainant_name,
    subject_text,
    complaint_desc,
    admin_remark,
    pdf_file,
):

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("FROM_EMAIL")

    subject = f"Notice: Complaint Filed Against You - {subject_text}"

    body = f"""
Dear {respondent_name},

This is to inform you that a complaint has been ACCEPTED by AP RERA against you.

----------------------------------------
Complaint Details
----------------------------------------

Complainant Name:
{complainant_name}

Subject:
{subject_text}

Description:
{complaint_desc}

Authority Remarks:
{admin_remark}

----------------------------------------

Please find the attached notice.

Regards,
AP RERA Authority
"""

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    # ✅ attach PDF from request directly
    if pdf_file:
        part = MIMEApplication(pdf_file.read(), Name=pdf_file.filename)
        part["Content-Disposition"] = f'attachment; filename="{pdf_file.filename}"'
        msg.attach(part)

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.sendmail(from_email, email, msg.as_string())
    server.quit()


def send_complaint_closed_mail_complainant(
    email, name, subject_text, complaint_desc, admin_remark
):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("FROM_EMAIL")

    subject = f"Complaint Closed - {subject_text}"

    body = f"""
Dear {name},

Your complaint has been CLOSED by AP RERA.

----------------------------------------
Complaint Details
----------------------------------------

Subject:
{subject_text}

Description:
{complaint_desc}

Final Remarks:
{admin_remark}

----------------------------------------

Thank you for using AP RERA services.

Regards,
AP RERA Authority
"""

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.sendmail(from_email, email, msg.as_string())
    server.quit()


# ================= CLOSED MAIL - RESPONDENT =================
def send_complaint_closed_mail_respondent(
    email, respondent_name, complainant_name, subject_text, complaint_desc, admin_remark
):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("FROM_EMAIL")

    subject = f"Complaint Closed - {subject_text}"

    body = f"""
Dear {respondent_name},

The complaint filed against you has been CLOSED by AP RERA.

----------------------------------------
Complaint Details
----------------------------------------

Complainant Name:
{complainant_name}

Subject:
{subject_text}

Description:
{complaint_desc}

Final Remarks:
{admin_remark}

----------------------------------------

No further action is required.

Regards,
AP RERA Authority
"""

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.sendmail(from_email, email, msg.as_string())
    server.quit()