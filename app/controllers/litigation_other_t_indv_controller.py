from flask import Blueprint, request, jsonify
from app import db
from app.models.litigation_other_t_indv import LitigationOtherTINDV

litigation_other_t_indv_bp = Blueprint("litigation_other_t_indv_bp", __name__)

@litigation_other_t_indv_bp.route("/api/other-t-indv/litigation/add", methods=["POST"])
def add_litigation():
    data = request.json

    try:
        case = LitigationOtherTINDV(
            application_no=data["applicationNo"],
            case_no=data["caseNo"],
            tribunal_place=data["tribunalPlace"],
            petitioner_name=data["petitionerName"],
            respondent_name=data["respondentName"],
            case_facts=data["caseFacts"],
            case_status=data["caseStatus"],
            interim_order=data["interimOrder"],
            final_order_details=data["finalOrderDetails"]
        )

        db.session.add(case)
        db.session.commit()

        return jsonify({"message": "Litigation saved successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
