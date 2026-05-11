from flask import Blueprint, jsonify, request
from app.controllers.project_preview_data_controller import build_project_preview_data
from app.models.project_registration_model import get_project_registration
from app.models.application_associate import ApplicationAssociate
from app.models.architect import Architect
from app.models.engineer import Engineer
from app.models.accountant import Accountant
from app.models.project_agent import AgentModel

# --------------------------------------------------
# Blueprint
# --------------------------------------------------
preview_bp = Blueprint("preview", __name__)

# --------------------------------------------------
# Preview API (USED BY FRONTEND)
# --------------------------------------------------
@preview_bp.route("/project/preview", methods=["POST"])
def project_preview_controller():
    print("🔥 PREVIEW CONTROLLER HIT 🔥")

    raw_data = request.get_json()
    print("🔥 RAW JSON:", raw_data)

    preview_data = build_project_preview_data(raw_data)

    return jsonify({
        "success": True,
        "data": preview_data
    })


# --------------------------------------------------
# Project Registration Fetch API (OPTIONAL / DEBUG)
# --------------------------------------------------
@preview_bp.route("/project-registration/<application_number>/<pan_number>", methods=["GET"])
def get_project_registration_controller(application_number, pan_number):
    try:
        data = get_project_registration(application_number, pan_number)

        if not data:
            return jsonify({"message": "No project found"}), 404

        return jsonify({
            "success": True,
            "data": data
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500