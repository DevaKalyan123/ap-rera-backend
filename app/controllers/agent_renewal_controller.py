from flask import Blueprint, request, jsonify
from datetime import datetime
from werkzeug.utils import secure_filename
from app.models.agent_renewal_model import AgentRenewal
from app.models.database import db
from app.utils.renewal_certificate_utils import generate_certificate,generate_certificate2
from app.utils.application_number_generator import generate_renewal_application_number
from app.models.agent_renewal_query_model import AgentRenewalQuery
from app.models.agent_registration_model import AgentModel
import os
from sqlalchemy import text
from app.utils.mail_service import send_approval_email, send_rejection_email
from app.models.admin_renewal_model import (
    get_renewal_dashboard_counts,
    get_renewals_by_status,
    get_renewal_detail,
    update_renewal_status
)


agent_renewal_bp = Blueprint("agent_renewal_bp", __name__)


# Create Renewal Application
@agent_renewal_bp.route("/create", methods=["POST"])
def create_renewal():

    data = request.get_json()

    if not data:
        return {"error": "Invalid JSON body"}, 400

    agent_id = data.get("agent_id")
    expiry_date = data.get("expiry_date")
    fee_type = data.get("fee_type")
    query = text("""
        SELECT email
        FROM agentregistration_details_t
        WHERE id = :agent_id
        """)

    row = db.session.execute(query, {"agent_id": agent_id}).fetchone()

    if row:
        email = row.email
    else:
        email = None

    if not agent_id or not fee_type:
        return {
            "error": "Missing required fields",
            "required": ["agent_id", "fee_type"]
        }, 400





    # 🚨 Prevent duplicate renewal
    existing = AgentRenewal.query.filter(
        AgentRenewal.agent_id == agent_id,
        AgentRenewal.renewal_status.in_(["DRAFT", "SUBMITTED"]),
        AgentRenewal.payment_status != "SUCCESS"
    ).first()

    if existing:
        return {
            "error": "Renewal already exists for this agent",
            "existing_application_no": existing.renewal_application_no
        }, 400


    # Fix expiry date
    if expiry_date and expiry_date != "None":
        expiry_date = datetime.fromisoformat(expiry_date).date()
    else:
        expiry_date = None


    # Generate renewal number
    application_no = generate_renewal_application_number()


    renewal = AgentRenewal(
        agent_id=agent_id,
        renewal_application_no=application_no,
        expiry_date=expiry_date,
        fee_type=fee_type,
        email=email
    )

    db.session.add(renewal)
    db.session.commit()

    return {
        "message": "Renewal created successfully",
        "application_no": application_no,
        "renewal_id": renewal.id
    }
# Submit Renewal
@agent_renewal_bp.route("/submit/<int:renewal_id>", methods=["POST"])
def submit_renewal(renewal_id):

    renewal = AgentRenewal.query.get(renewal_id)

    if not renewal:
        return jsonify({"error": "Renewal not found"}), 404

    renewal.renewal_status = "SUBMITTED"
    renewal.submitted_at = datetime.utcnow()

    db.session.commit()

    return jsonify({"message": "Renewal submitted"})


@agent_renewal_bp.route("/payment/<int:renewal_id>", methods=["POST"])
def update_payment(renewal_id):

    renewal = AgentRenewal.query.get(renewal_id)

    if not renewal:
        return {"error": "Renewal not found"}, 404
    
    email = renewal.email

    renewal.payment_status = "SUCCESS"

    db.session.commit()

    return {"message": "Payment updated successfully"}


# Officer Approval
from sqlalchemy import text

@agent_renewal_bp.route("/approve/<int:renewal_id>", methods=["POST"])
def approve_renewal(renewal_id):

    renewal = AgentRenewal.query.get(renewal_id)

    if not renewal:
        return {"error": "Renewal not found"}, 404

    renewal.renewal_status = "APPROVED"

    result = AgentModel.approve_agent_renewal(renewal.agent_id)

    if not result["success"]:
        return result, 400

    db.session.commit()

    certificate_path = generate_certificate(
        result["agent_name"],
        result["application_no"],
        result["expiry_date"]
    )

    return {
        "message": "Renewal approved successfully",
        "certificate": certificate_path,
        "new_expiry": str(result["expiry_date"])
    }


# Reject Renewal
@agent_renewal_bp.route("/reject/<int:renewal_id>", methods=["POST"])
def reject_renewal(renewal_id):

    renewal = AgentRenewal.query.get(renewal_id)

    renewal.renewal_status = "REJECTED"

    db.session.commit()

    return jsonify({"message": "Renewal rejected"})


# Get Renewal Status
@agent_renewal_bp.route("/status/<int:renewal_id>", methods=["GET"])
def renewal_status(renewal_id):

    renewal = AgentRenewal.query.get(renewal_id)

    if not renewal:
        return jsonify({"error": "Not found"}), 404

    return jsonify({
        "renewal_id": renewal.id,
        "status": renewal.renewal_status
    })
    
@agent_renewal_bp.route("/agent-details/<application_no>", methods=["GET"])
def get_agent_details(application_no):

    try:

        from sqlalchemy import text

        query = text("""
            SELECT
                id,
                agent_name,
                pan,
                mobile,
                email,
                license_date AS valid_from,
                (license_date + INTERVAL '5 years') AS valid_to
            FROM agentregistration_details_t
            WHERE application_no = :application_no
        """)

        row = db.session.execute(query, {
            "application_no": application_no
        }).fetchone()

        if not row:
            return jsonify({"error": "Agent not found"}), 404

        return jsonify({
            "agent_id": row.id,
            "agent_name": row.agent_name,
            "pan": row.pan,
            "mobile": row.mobile,
            "email": row.email,
            "valid_from": str(row.valid_from),
            "valid_to": str(row.valid_to)
        })

    except Exception as e:

        return jsonify({"error": str(e)}), 500
    
# ===============================
# Upload Documents (FIXED)
# ===============================
@agent_renewal_bp.route("/upload-doc", methods=["POST"])
def upload_doc():

    try:
        renewal_id = request.form.get("renewal_id")

        if not renewal_id:
            return {"error": "renewal_id missing"}, 400

        files = request.files

        if not files:
            return {"error": "No files received"}, 400

        # ✅ Correct upload folder
        upload_folder = os.path.join("app", "uploads", "agent_renewal_docs")

        # ✅ Create folder if not exists
        os.makedirs(upload_folder, exist_ok=True)

        saved_files = {}

        for key in files:

            file = files.get(key)

            if file and file.filename:

                # ✅ Secure filename
                filename = secure_filename(file.filename)

                file_path = os.path.join(upload_folder, filename)

                # ✅ Save file
                file.save(file_path)

                saved_files[key] = file_path

        return {
            "message": "Files uploaded successfully",
            "files": saved_files
        }

    except Exception as e:
        print("UPLOAD ERROR:", str(e))
        return {"error": str(e)}, 500
    
@agent_renewal_bp.route("/officer/list", methods=["GET"])
def officer_list():

    renewals = AgentRenewal.query.filter_by(renewal_status="SUBMITTED").all()

    data = []

    for r in renewals:
        data.append({
            "renewal_id": r.id,
            "agent_id": r.agent_id,
            "application_no": r.renewal_application_no,
            "status": r.renewal_status
        })

    return {"data": data}
@agent_renewal_bp.route("/query", methods=["POST"])
def raise_query():

    data = request.json

    query = AgentRenewalQuery(
        renewal_id=data["renewal_id"],
        query_text=data["query_text"],
        raised_by="OFFICER"
    )

    db.session.add(query)
    db.session.commit()

    return {"message": "Query raised"}
@agent_renewal_bp.route("/query/respond", methods=["POST"])
def respond_query():

    data = request.json

    query = AgentRenewalQuery.query.get(data["query_id"])

    if not query:
        return {"error": "Query not found"}, 404

    query.response = data["response"]

    query.status = "RESOLVED"

    db.session.commit()

    return {"message": "Query responded"}

@agent_renewal_bp.route("/query/<int:renewal_id>")
def get_queries(renewal_id):

    queries = AgentRenewalQuery.query.filter_by(renewal_id=renewal_id).all()

    result = []

    for q in queries:
        result.append({
            "query_id": q.id,
            "query": q.query_text,
            "response": q.response,
            "status": q.status
        })

    return {"queries": result}
from sqlalchemy import text

@agent_renewal_bp.route("/<int:renewal_id>/preview", methods=["GET"])
def get_preview(renewal_id):

    renewal = db.session.execute(
        text("SELECT * FROM agent_renewal_t WHERE id = :id"),
        {"id": renewal_id}
    ).fetchone()

    if not renewal:
        return {"error": "Renewal not found"}, 404

    agent = db.session.execute(
        text("""
        SELECT agent_name, pan, mobile, email
        FROM agentregistration_details_t
        WHERE id = :agent_id
        """),
        {"agent_id": renewal.agent_id}
    ).fetchone()

    if not agent:
        return {"error": "Agent not found"}, 404

    return {
        "renewal_id": renewal.id,
        "application_no": renewal.renewal_application_no,
        "created_at": str(renewal.created_at),
        "renewal_status": renewal.renewal_status,
        "expiry_date": str(renewal.expiry_date),
        "payment_status": renewal.payment_status,

        "agent_name": agent.agent_name,
        "pan": agent.pan,
        "mobile": agent.mobile,
        "email": agent.email
    }
    
# ===============================
# Admin Renewal Dashboard Counts
# ===============================
@agent_renewal_bp.route("/admin/renewal-dashboard", methods=["GET","OPTIONS"])
def renewal_dashboard():

    data = get_renewal_dashboard_counts()

    return jsonify(data)


# ===============================
# Admin Renewals By Status
# ===============================
@agent_renewal_bp.route("/admin/renewals/<status>", methods=["GET","OPTIONS"])
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


# ===============================
# Renewal Detail
# ===============================
@agent_renewal_bp.route("/admin/renewal/<int:renewal_id>", methods=["GET"])
def renewal_detail(renewal_id):

    data = get_renewal_detail(renewal_id)

    if not data:
        return {"error": "Record not found"}, 404

    return jsonify(data)


# ===============================


@agent_renewal_bp.route("/admin/renewal/update/<int:renewal_id>", methods=["PUT"])
def update_status(renewal_id):

    try:

        data = request.get_json()

        status = data.get("status")
        remarks = data.get("remarks")

        print("Status:", status)
        print("Remarks:", remarks)

        renewal = AgentRenewal.query.get(renewal_id)

        if not renewal:
            return {"error": "Renewal not found"}, 404

        print("Renewal Email:", renewal.email)

        renewal.renewal_status = status
        renewal.remarks = remarks

        db.session.commit()

        # APPROVED CASE
        if status == "APPROVED":

            print("Generating certificate...")

            certificate_path = generate_certificate2(
                renewal.agent_id,
                renewal.renewal_application_no,
                renewal.expiry_date
            )

            print("Certificate Path:", certificate_path)

            print("Sending approval email...")

            send_approval_email(
                renewal.email,
                renewal.renewal_application_no,
                renewal.expiry_date,
                certificate_path
            )

            print("Approval mail sent")

        # REJECTED CASE
        elif status == "REJECTED":

            print("Sending rejection email...")

            send_rejection_email(
                renewal.email,
                renewal.renewal_application_no,
                remarks
            )

            print("Rejection mail sent")

        return {"message": "Renewal updated successfully"}

    except Exception as e:

        print("ERROR OCCURRED:", str(e))

        return {"error": str(e)}, 500