from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
from sqlalchemy import text
from app import db
import os
import logging
import json 

from app.models.agent_registration_model import AgentModel

agent_bp = Blueprint("agent", __name__)
UPLOAD_FOLDER = "uploads/agents"
ALLOWED_EXT = {"pdf", "jpg", "jpeg", "png"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


def save_file(file):
    if not allowed_file(file.filename):
        raise ValueError("Invalid file type")

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    original_name = secure_filename(file.filename)
    stored_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{original_name}"
    path = os.path.join(UPLOAD_FOLDER, stored_name)

    file.save(path)

    return {
        "original_name": original_name,
        "stored_name": stored_name,
        "mime_type": file.mimetype,
        "path": path
    }


# ================= STEP 1 =================
@agent_bp.route("/register-step1", methods=["POST"])
def register_agent_step1():
    try:
        form = request.form
        files = request.files

        required_files = ["photograph", "panProof", "addressProof"]

        for f in required_files:
            if f not in files or files[f].filename == "":
                return jsonify({"success": False, "message": f"{f} missing"}), 400

        saved = {k: save_file(files[k]) for k in required_files}

        affidavit_file = None
        if "selfAffidavit" in files and files["selfAffidavit"].filename != "":
            affidavit_file = save_file(files["selfAffidavit"])

        # JSON lists from frontend
        projects = form.get("projects")
        litigations = form.get("litigations")
        other_rera = form.get("otherReraList")

        print("PROJECTS RAW:", projects)
        print("LITIGATIONS RAW:", litigations)
        print("OTHER RERA RAW:", other_rera)

        projects_list = json.loads(projects) if projects else []
        litigations_list = json.loads(litigations) if litigations else []
                # Attach litigation certificate files
        for i, l in enumerate(litigations_list):

            interim_file = files.get(f"interimCert_{i}")
            disposed_file = files.get(f"disposedCert_{i}")

            if interim_file and interim_file.filename != "":
                l["interim_order_certificate"] = save_file(interim_file)
            else:
                l["interim_order_certificate"] = None

            if disposed_file and disposed_file.filename != "":
                l["disposed_certificate"] = save_file(disposed_file)
            else:
                l["disposed_certificate"] = None
        other_rera_list = json.loads(other_rera) if other_rera else []

        data = {
            "agent_type": form.get("agentType"),
            "agent_name": form.get("agentName"),
            "father_name": form.get("fatherName"),
            "occupation_id": form.get("occupation"),
            "email": form.get("email"),
            "aadhaar": form.get("aadhaar"),
            "pan": form.get("pan"),
            "mobile": form.get("mobile"),

            "landline": form.get("landline") or None,
            "license_number": form.get("licenseNumber") or None,
            "license_date": form.get("licenseDate") if form.get("licenseDate") else None,

            "address1": form.get("address1"),
            "address2": form.get("address2") or None,
            "state_id": form.get("state"),
            "district": form.get("district"),
            "mandal": form.get("mandal"),
            "village": form.get("village"),
            "pincode": form.get("pincode"),

            "photograph": saved["photograph"],
            "pan_proof": saved["panProof"],
            "address_proof": saved["addressProof"],

            "self_declared_affidavit": affidavit_file,

            "last_five_years_project_details": form.get("last_five_years_project_details"),
            "any_civil_criminal_cases": form.get("any_civil_criminal_cases"),
            "registration_other_states": form.get("registration_other_states"),
        }

        result = AgentModel.create_agent_registration_step1(data)

        if not result["success"]:
            return jsonify(result), 500

        agent_id = result["agent_id"]

        # insert projects
        if projects_list:
            res_projects = AgentModel.insert_agent_projects(agent_id, projects_list)
            if not res_projects["success"]:
                return jsonify(res_projects), 500

        # insert litigations
        if litigations_list:
            res_litigations = AgentModel.insert_agent_litigations(agent_id, litigations_list)
            if not res_litigations["success"]:
                return jsonify(res_litigations), 500

        # insert other state rera
        if other_rera_list:
            res_other = AgentModel.insert_agent_other_state_rera(agent_id, other_rera_list)
            if not res_other["success"]:
                return jsonify(res_other), 500

        return jsonify({
            "success": True,
            "agent_id": agent_id,
            "application_no": result["application_no"]
        }), 201

    except Exception as e:
        logging.exception("Agent Step-1 failed")
        return jsonify({"success": False, "message": str(e)}), 500


# ================= STEP 2 =================
@agent_bp.route("/register-step2", methods=["POST"])
def register_agent_step2():
    try:
        form = request.form
        files = request.files

        agent_id = form.get("agent_id")
        if not agent_id:
            return jsonify({"success": False, "message": "agent_id missing"}), 400

        required_files = ["itrYear1", "itrYear2", "itrYear3"]
        for f in required_files:
            if f not in files or files[f].filename == "":
                return jsonify({"success": False, "message": f"{f} missing"}), 400

        saved = {k: save_file(files[k]) for k in required_files}

        result = AgentModel.update_itr_documents(
            agent_id=agent_id,
            itr_year1=saved["itrYear1"],
            itr_year2=saved["itrYear2"],
            itr_year3=saved["itrYear3"]
        )

        if result["success"]:
            return jsonify({"success": True}), 200

        return jsonify(result), 500

    except Exception as e:
        logging.exception("Agent Step-2 failed")
        return jsonify({"success": False, "message": str(e)}), 500


# ================= PREVIEW =================
@agent_bp.route("/preview/<int:agent_id>", methods=["GET"])
def agent_preview(agent_id):
    result = AgentModel.get_agent_preview(agent_id)

    if result["success"]:
        return jsonify(result), 200

    return jsonify(result), 404

@agent_bp.route("/check-pan", methods=["POST"])
def check_pan():
    try:
        data = request.get_json()
        pan = data.get("pan")

        if not pan:
            return jsonify({
                "success": False,
                "message": "PAN is required"
            }), 400

        result = AgentModel.get_agent_by_pan(pan.strip().upper())
        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
    
@agent_bp.route("/send-otp", methods=["POST"])
def send_otp():
    try:
        data = request.get_json()
        agent_id = data.get("agent_id")

        if not agent_id:
            return jsonify({
                "success": False,
                "message": "agent_id required"
            }), 400

        result = AgentModel.send_otp(agent_id)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
    
@agent_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    try:
        data = request.get_json()

        agent_id = data.get("agent_id")
        otp = data.get("otp")

        if not agent_id or not otp:
            return jsonify({
                "success": False,
                "message": "agent_id and otp required"
            }), 400

        result = AgentModel.verify_otp(agent_id, otp)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
    
@agent_bp.route("/payment-details/<int:agent_id>", methods=["GET"])
def get_payment_details(agent_id):
    query = text("""
        SELECT p.application_no,p.transaction_id,p.amount,p.payment_for,p.status,p.created_at,
        a.agent_name,a.mobile FROM agent_payment_t p
        JOIN agentregistration_details_t a ON a.id = p.agent_id
        WHERE p.agent_id = :agent_id ORDER BY p.id DESC LIMIT 1
    """)

    row = db.session.execute(query, {"agent_id": agent_id}).fetchone()

    if not row:
        return jsonify({"success": False}), 404

    return jsonify({
        "success": True,
        "data": dict(row._mapping)
    })
@agent_bp.route("/create-payment/<int:agent_id>", methods=["POST"])
def create_payment(agent_id):
    result = AgentModel.create_payment(agent_id)

    if result["success"]:
        return jsonify(result), 200

    return jsonify(result), 500
@agent_bp.route("/partial-applications/<string:pan>", methods=["GET"])
def partial_applications(pan):
    try:
        if not pan:
            return jsonify({
                "success": False,
                "message": "PAN is required"
            }), 400

        pan = pan.strip().upper()

        data = AgentModel.get_partial_applications(pan)

        return jsonify({
            "success": True,
            "data": data
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
    

@agent_bp.route("/resume-application/<application_no>", methods=["GET"])
def resume_application(application_no):
    try:
        result = AgentModel.agent_details_application_no(application_no)

        if result["success"]:
            return jsonify(result), 200

        return jsonify(result), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
@agent_bp.route("/send-otp-email", methods=["POST"])
def send_otp_email_preview():
    try:
        data = request.get_json()
        agent_id = data.get("agent_id")

        if not agent_id:
            return jsonify({"success": False, "message": "agent_id required"}), 400

        result = AgentModel.send_otp_email_by_agent_id(agent_id)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500