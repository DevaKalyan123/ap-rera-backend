from flask import Blueprint, request, jsonify
from app.models.application_associate import ApplicationAssociate
from app.models.database import db

# 🔽 IMPORT ASSOCIATE MODELS (FOR PREVIEW)
from app.models.architect import Architect
from app.models.engineer import Engineer
from app.models.accountant import Accountant
from app.models.project_agent import AgentModel
from app.models.contractor import Contractor
from app.models.project_engineer import ProjectEngineer

import logging
#hello

application_associate_bp = Blueprint(
    "application_associate",
    __name__
)

# ======================================================
# POST: LINK ASSOCIATE TO APPLICATION (ALREADY WORKING)
# ======================================================
@application_associate_bp.route("/application/associate", methods=["POST"])
def link_associate_to_application():
    try:
        data = request.get_json()
        logging.info(f"checkthe input: '{data}'")
        if not data:
            return jsonify({
                "success": False,
                "message": "Invalid JSON payload"
            }), 400

        required_fields = [
            "application_number",
            "pan_number",
            "associate_type",
            "associate_id",
        ]

        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    "success": False,
                    "message": f"{field} is required"
                }), 400

        link = ApplicationAssociate(
            application_number=data["application_number"],
            pan_number=data["pan_number"],
            associate_type=data["associate_type"],
            associate_id=data["associate_id"],
        )

        db.session.add(link)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Associate linked to application successfully"
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ======================================================
# GET: FETCH ASSOCIATES FOR PREVIEW (🔥 NEW & REQUIRED)
# ======================================================
@application_associate_bp.route("/application/associates", methods=["GET"])
def get_application_associates():
    try:
        application_number = request.args.get("application_number")
        pan_number = request.args.get("pan_number")

        if not application_number or not pan_number:
            return jsonify({
                "success": False,
                "message": "application_number and pan_number are required"
            }), 400

        links = ApplicationAssociate.query.filter_by(
            application_number=application_number,
            pan_number=pan_number
        ).all()

        result = {
            "architects": [],
            "engineers": [],
            "accountants": [],
            "agents": [],
            "contractors": [],
            "project_engineers": [] 
        }

        for link in links:
            if link.associate_type == "architect":
                obj = Architect.query.get(link.associate_id)
                if obj:
                    result["architects"].append(obj.to_dict())

            elif link.associate_type == "engineer":
                obj = Engineer.query.get(link.associate_id)
                if obj:
                    result["engineers"].append(obj.to_dict())

            elif link.associate_type == "accountant":
                obj = Accountant.query.get(link.associate_id)
                if obj:
                    result["accountants"].append(obj.to_dict())

            elif link.associate_type == "agent":
                obj = AgentModel.query.get(link.associate_id)
                if obj:
                    result["agents"].append(obj.to_dict())

            elif link.associate_type == "contractor":
                obj = Contractor.query.get(link.associate_id)
                if obj:
                    result["contractors"].append(obj.to_dict())

            elif link.associate_type == "project_engineer":
                obj = ProjectEngineer.query.get(link.associate_id)
                if obj:
                    result["project_engineers"].append(obj.to_dict())

        return jsonify({
            "success": True,
            "data": result
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500