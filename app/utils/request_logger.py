from flask import request
from app.models.database import db
from app.models.audit_log_model import AuditLog


def get_client_ip():

    ip = request.headers.get(
        "X-Forwarded-For",
        request.headers.get("X-Real-IP", request.remote_addr)
    )

    if ip and "," in ip:
        ip = ip.split(",")[0]

    return ip


def extract_application_number():

    # try from form-data
    app_no = request.form.get("applicationNumber")

    if app_no:
        return app_no

    # try from query params
    app_no = request.args.get("applicationNumber")

    if app_no:
        return app_no

    # try from JSON
    if request.is_json:
        data = request.get_json(silent=True)
        if data:
            return data.get("applicationNumber")

    return None


def determine_action():

    path = request.path

    if "project_closure" in path:
        return "PROJECT_CLOSURE_SUBMIT"

    if "login" in path:
        return "USER_LOGIN"

    if "project_registration" in path:
        return "PROJECT_REGISTER"

    if "upload" in path:
        return "FILE_UPLOAD"

    return "API_CALL"


def log_request(response):

    try:

        # log only API routes
        if not request.path.startswith("/api"):
            return response

        ip_address = get_client_ip()

        application_number = extract_application_number()

        action = determine_action()

        log = AuditLog(
            application_number=application_number,
            action=action,
            ip_address=ip_address,
            endpoint=request.path,
            method=request.method,
            user_agent=request.headers.get("User-Agent"),
            status_code=response.status_code
        )

        db.session.add(log)
        db.session.commit()

    except Exception as e:

        print("Audit log error:", e)

    return response