from flask import Blueprint, jsonify
from app.models.admin_renewal_model import get_all_projects

from email.message import EmailMessage
from reportlab.pdfgen import canvas
from sqlalchemy import text
from app.models.database import db
from flask import request
from app.models.admin_renewal_model import (
    get_renewal_dashboard_counts,
    get_renewals_by_status
)
from app.utils.renewal_certificate_utils import generate_project_certificate
from app.utils.mail_service import (
    send_project_approval_email,
    send_project_rejection_email
)

# Blueprint
admin_renewal_bp = Blueprint("admin_renewal_bp", __name__)


# ===============================
# Renewal Dashboard Counts
# ===============================
@admin_renewal_bp.route("/admin/renewal-dashboard", methods=["GET","OPTIONS"])
def renewal_dashboard():

    data = get_renewal_dashboard_counts()

    return jsonify(data)


# ===============================
# Renewals By Status
# ===============================
@admin_renewal_bp.route("/admin/renewals/<status>", methods=["GET","OPTIONS"])
def renewals_by_status(status):

    rows = get_renewals_by_status(status.upper())

    result = []

    for r in rows:
        result.append({
            "id": r["id"],
            "agent_id": r["agent_id"],
            "application_no": r["application_no"],
            "expiry_date": r["expiry_date"],
            "status": r["renewal_status"],
            "payment_status": r["payment_status"]
        })

    return jsonify(result)
@admin_renewal_bp.route("/admin/projects", methods=["GET","OPTIONS"])
def admin_projects():

    rows = get_all_projects()

    result = []

    for r in rows:
        result.append({
    "id": r["id"],
    "application_no": r["application_no"],
    "promoter_type": r["promoter_type"],
    "pan_number": r["pan_number"],
    "bank_name": r["bank_name"],
    "status": r["status"]

})

    return jsonify(result)
# ===============================
# Get Full Project Details
# ===============================
@admin_renewal_bp.route("/admin/projects/<int:id>", methods=["GET"])
def get_project_details(id):

    query = text("""
        SELECT *
        FROM project_registrations
        WHERE id = :id
    """)

    project = db.session.execute(query, {"id": id}).mappings().first()
    if not project:
        return jsonify({"error": "Project not found"}), 404

    return jsonify(dict(project))
# ===============================
# Update Project Status
# ===============================
@admin_renewal_bp.route("/admin/projects/<int:id>/status", methods=["PUT"])
def update_project_status(id):
    data = request.json
    status = data.get("status")

    query = text("""
        UPDATE project_registrations
        SET status = :status
        WHERE id = :id
    """)

    db.session.execute(query, {"status": status, "id": id})
    db.session.commit()

    return jsonify({"message": "Status updated"})
from flask import request


# ===============================
# Approve Project
# ===============================
@admin_renewal_bp.route("/admin/projects/<int:id>/approve", methods=["PUT"])
def approve_project(id):

    try:

        # 1. Get project
        query = text("SELECT * FROM project_registrations WHERE id = :id")
        project = db.session.execute(query, {"id": id}).mappings().first()

        if not project:
            return jsonify({"error": "Project not found"}), 404

        print("Project Email:", project.get("email"))

        # 2. Update status
        db.session.execute(
            text("UPDATE project_registrations SET status='APPROVED' WHERE id=:id"),
            {"id": id}
        )
        db.session.commit()

        # 3. Generate Certificate
        print("Generating project certificate...")

        certificate_path = generate_project_certificate(project)

        print("Certificate Path:", certificate_path)

        # 4. Send Email
        print("Sending approval email...")

        send_project_approval_email(
            project["email"],
            project["application_no"],
            project.get("project_name"),
            certificate_path
        )

        print("Project approval email sent")

        return jsonify({"message": "Project Approved Successfully"})

    except Exception as e:

        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500
    
    
@admin_renewal_bp.route("/admin/projects/<int:id>/reject", methods=["PUT"])
def reject_project(id):

    try:

        data = request.json
        comment = data.get("comment")

        if not comment:
            return jsonify({"error": "Comment required"}), 400

        # 1. Get project
        query = text("SELECT * FROM project_registrations WHERE id = :id")
        project = db.session.execute(query, {"id": id}).mappings().first()

        if not project:
            return jsonify({"error": "Project not found"}), 404

        print("Project Email:", project.get("email"))

        # 2. Update status
        db.session.execute(
            text("""
                UPDATE project_registrations
                SET status='REJECTED',
                    rejection_comment=:comment
                WHERE id=:id
            """),
            {"comment": comment, "id": id}
        )
        db.session.commit()

        # 3. Send rejection email
        print("Sending rejection email...")

        send_project_rejection_email(
            project["email"],
            project["application_no"],
            project.get("project_name"),
            comment
        )

        print("Project rejection email sent")

        return jsonify({"message": "Project Rejected Successfully"})

    except Exception as e:

        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500