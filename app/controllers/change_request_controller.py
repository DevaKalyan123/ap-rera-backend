import os
import uuid
import json
import logging

from flask import Blueprint, request, jsonify, send_from_directory, current_app

from app.models.database import db
from app.models.project_change_request_model import ProjectChangeRequest
from app.models.change_request_changes_model import ChangeRequestChange
from app.utils.mail_service import send_rejection_email
from sqlalchemy import func
from app.utils.mail_service import send_change_request_approval_email

change_request_bp = Blueprint("change_request_bp", __name__)


def get_upload_folder():
    upload_folder = os.path.join(current_app.root_path, "uploads", "change_requests")
    os.makedirs(upload_folder, exist_ok=True)
    return upload_folder


LOG_FILE = os.path.join("app", "logs", "change_reqist.log")

logger = logging.getLogger("change_request")

if not logger.handlers:
    handler = logging.FileHandler(LOG_FILE)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def generate_reference_no():
    last_request = ProjectChangeRequest.query.order_by(
        ProjectChangeRequest.id.desc()
    ).first()

    if not last_request:
        return "REF-0001"

    last_id = last_request.id
    new_id = last_id + 1

    return f"REF-{str(new_id).zfill(4)}"


@change_request_bp.route("/change-request", methods=["POST"])
def create_change_request():

    try:
        data = request.form
        print("EMAIL ", data.get("email"))
        new_request = ProjectChangeRequest(
            reference_no=generate_reference_no(),
            application_number=data.get("application_number"),
            pan_number=data.get("pan_number"),
            project_name=data.get("project_name"),
            applicant_name=data.get("applicant_name"),
            email=data.get("email"),
            payment_gateway=data.get("payment_gateway"),
            payment_transaction_id=data.get("payment_transaction_id"),
            payment_status=data.get("payment_status"),
        )

        db.session.add(new_request)
        db.session.commit()

        request_id = new_request.id

        changes_json = request.form.get("changes")
        changes = json.loads(changes_json) if changes_json else []

        upload_folder = get_upload_folder()  # ✅ get once

        for i, row in enumerate(changes):

            old_file = request.files.get(f"old_file_{i}")
            new_file = request.files.get(f"new_file_{i}")
            proof_file = request.files.get(f"proof_file_{i}")

            old_path = None
            new_path = None
            proof_path = None

            # OLD FILE
            if old_file:
                filename = str(uuid.uuid4()) + "_" + old_file.filename
                filepath = os.path.join(upload_folder, filename)
                old_file.save(filepath)
                old_path = os.path.join("uploads", "change_requests", filename)

            if new_file:
                filename = str(uuid.uuid4()) + "_" + new_file.filename
                filepath = os.path.join(upload_folder, filename)
                new_file.save(filepath)
                new_path = os.path.join("uploads", "change_requests", filename)

            if proof_file:
                filename = str(uuid.uuid4()) + "_" + proof_file.filename
                filepath = os.path.join(upload_folder, filename)
                proof_file.save(filepath)
                proof_path = os.path.join("uploads", "change_requests", filename)

            change = ChangeRequestChange(
                request_id=request_id,
                section=row.get("section"),
                subsection=row.get("subsection"),
                field_name=row.get("field_name"),
                old_value=row.get("old_value"),
                new_value=row.get("new_value"),
                data_json=row.get("data_json"),
                description=row.get("description"),
                proof_document_name=proof_path,
                old_file_path=old_path,
                new_file_path=new_path,
                change_mode=row.get("change_mode"),
            )

            db.session.add(change)

        db.session.commit()

        logger.info(f"Change Request Created Successfully ID: {request_id}")

        return (
            jsonify(
                {
                    "message": "Change Request Created Successfully",
                    "request_id": request_id,
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        logger.error(str(e))
        return jsonify({"error": str(e)}), 500


@change_request_bp.route("/change-request/<int:id>", methods=["GET"])
def get_change_request(id):

    request_data = ProjectChangeRequest.query.get(id)

    if not request_data:
        return jsonify({"message": "Request not found"}), 404

    changes = ChangeRequestChange.query.filter_by(request_id=id).all()

    return jsonify(
        {
            "request": request_data.to_dict(),
            "changes": [c.to_dict() for c in changes],
        }
    )


@change_request_bp.route("/change-request/status/<string:status>", methods=["GET"])
def get_change_requests_by_status(status):

    try:
        if status.upper() == "ALL":
            requests = ProjectChangeRequest.query.all()
        else:
            requests = ProjectChangeRequest.query.filter_by(status=status).all()

        result = []
        for req in requests:
            result.append(
                {
                    "request": req.to_dict(),
                    "changes": [
                        change.to_dict() for change in req.changes
                    ],  # ✅ IMPORTANT
                }
            )

        return jsonify({"count": len(result), "data": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@change_request_bp.route("/change-request/document/<path:filename>", methods=["GET"])
def view_change_request_document(filename):

    upload_folder = get_upload_folder()

    return send_from_directory(upload_folder, filename)


from datetime import datetime


@change_request_bp.route("/change-request/reject/<int:id>", methods=["PUT"])
def reject_change_request(id):
    try:
        data = request.get_json()

        remarks = data.get("remarks")
        email = data.get("email")

        change_req = ProjectChangeRequest.query.get(id)

        if not change_req:
            return {"error": "Request not found"}, 404

        change_req.status = "REJECTED"
        change_req.regected_reson = remarks or ""
        change_req.email = email or change_req.email
        change_req.updated_at = datetime.utcnow()

        db.session.commit()

        # ✅ safe email sending
        if change_req.email:
            send_rejection_email(change_req.email, change_req.reference_no, remarks)

        return {"message": "Rejected + Stored + Mail Sent"}

    except Exception as e:
        db.session.rollback()
        print("ERROR:", str(e))
        return {"error": str(e)}, 500


@change_request_bp.route("/change-request/approve/<int:id>", methods=["PUT"])
def approve_change_request(id):
    try:
        data = request.get_json() or {}

        change_req = ProjectChangeRequest.query.get(id)

        if not change_req:
            return {"error": "Request not found"}, 404

        # ✅ UPDATE STATUS (IMPORTANT)
        change_req.status = "APPROVED"
        change_req.updated_at = datetime.utcnow()

        # ✅ get email
        email = data.get("email") or change_req.email

        # ✅ get changes
        changes = ChangeRequestChange.query.filter_by(request_id=id).all()

        change_list = []
        for c in changes:
            change_list.append(
                {"field": c.field_name, "old": c.old_value, "new": c.new_value}
            )

        # ✅ commit DB changes FIRST
        db.session.commit()

        # ✅ send email
        if email:
            send_change_request_approval_email(
                email, change_req.reference_no, change_list
            )

        return {"message": "Approved + Status Updated + Mail Sent"}

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500