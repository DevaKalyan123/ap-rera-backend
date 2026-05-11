import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from sqlalchemy import text

from app.models.database import db
from app.models.project_closure_model import ProjectClosureNEW
from app.utils.request_logger import get_client_ip


project_closure_bp = Blueprint("project_closure", __name__)


# ---------------------------------------------------------
# FETCH PROJECT DETAILS
# ---------------------------------------------------------
@project_closure_bp.route("/details", methods=["GET"])
def get_project_details():

    try:

        application_no = request.args.get("applicationNumber")

        if not application_no:
            return jsonify({
                "status": "error",
                "message": "Application number missing"
            }), 400

        query = text("""
            SELECT
                pr.application_no,
                pr.project_name,
                pr.name AS promoter_name
            FROM project_registrations pr
            WHERE pr.application_no::TEXT = :application_no
        """)

        result = db.session.execute(
            query,
            {"application_no": str(application_no)}
        ).mappings().first()

        if result is None:
            return jsonify({
                "status": "error",
                "message": "Project not found"
            }), 404

        return jsonify({
            "status": "success",
            "data": {
                "applicationNumber": result["application_no"],
                "projectName": result["project_name"],
                "promoterName": result["promoter_name"]
            }
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "status": "error",
            "message": "Server error"
        }), 500


# ---------------------------------------------------------
# FILE SAVE FUNCTION
# ---------------------------------------------------------
def save_file(file, prefix, application_no):

    if not file or file.filename == "":
        return None

    filename = secure_filename(f"{prefix}_{application_no}_{file.filename}")

    upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], "closures")

    os.makedirs(upload_dir, exist_ok=True)

    filepath = os.path.join(upload_dir, filename)

    file.save(filepath)

    return f"uploads/closures/{filename}"


# ---------------------------------------------------------
# SUBMIT PROJECT CLOSURE
# ---------------------------------------------------------
@project_closure_bp.route("/submit", methods=["POST"])
def submit_closure():

    try:

        data = request.form

        application_no = data.get("applicationNumber")

        if not application_no:
            return jsonify({
                "status": "error",
                "message": "Application number required"
            }), 400

        # capture client ip
        ip_address = get_client_ip()

        closure = ProjectClosureNEW(
            application_number=application_no,
            project_name=data.get("projectName"),
            promoter_name=data.get("promoterName"),
            occupancy_certificate_status=data.get("occupancyCertificateStatus"),
            reason_for_closure=data.get("reasonForClosure"),
            declaration_accepted=data.get("declarationAccepted") == "true",
            ip_address=ip_address
        )

        # ---------------- FILE UPLOADS ----------------

        if data.get("occupancyCertificateStatus") == "Yes":
            closure.occupancy_certificate_doc = save_file(
                request.files.get("occupancyCertificateDoc"),
                "occupancy",
                application_no
            )

        closure.sale_deed_copies_doc = save_file(
            request.files.get("saleDeedCopiesDoc"),
            "sale_deed",
            application_no
        )

        closure.association_of_allottees_doc = save_file(
            request.files.get("associationOfAllotteesDoc"),
            "association",
            application_no
        )

        closure.common_areas_handover_doc = save_file(
            request.files.get("commonAreasHandoverDoc"),
            "common_area",
            application_no
        )

        closure.structural_liability_affidavit_doc = save_file(
            request.files.get("structuralLiabilityDoc"),
            "structural",
            application_no
        )

        closure.unsold_units_affidavit_doc = save_file(
            request.files.get("unsoldUnitsDoc"),
            "unsold_units",
            application_no
        )

        closure.rera_bank_statement_doc = save_file(
            request.files.get("reraBankStatementDoc"),
            "bank_statement",
            application_no
        )

        photos = request.files.getlist("projectPhotosDoc")

        photo_paths = []

        for photo in photos:
            path = save_file(photo, "photo", application_no)
            if path:
                photo_paths.append(path)

        closure.project_photos_doc = ",".join(photo_paths)

        db.session.add(closure)

        (application_no, "PROJECT_CLOSURE_SUBMIT")

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Project closure submitted successfully"
        }), 201

    except Exception as e:

        print("Closure submit error:", e)

        db.session.rollback()

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ---------------------------------------------------------
# CHECK IF ALREADY SUBMITTED
# ---------------------------------------------------------
@project_closure_bp.route("/check", methods=["GET"])
def check_closure():

    try:
        application_no = request.args.get("applicationNumber")

        if not application_no:
            return jsonify({
                "status": "error",
                "message": "Application number required"
            }), 400

        # ✅ CHECK IN DB
        exists = db.session.query(ProjectClosureNEW).filter_by(
            application_number=application_no
        ).first()

        return jsonify({
            "exists": True if exists else False
        })

    except Exception as e:
        print("Check error:", e)

        return jsonify({
            "status": "error",
            "message": "Server error"
        }), 500