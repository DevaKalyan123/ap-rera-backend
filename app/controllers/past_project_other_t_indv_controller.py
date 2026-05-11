from flask import Blueprint, request, jsonify
from app import db
from app.models.past_project_other_t_indv import PastProjectOtherTINDV

past_project_other_t_indv_bp = Blueprint("past_project_other_t_indv_bp", __name__)

@past_project_other_t_indv_bp.route("/api/other-t-indv/project/add", methods=["POST"])
def add_past_project():
    data = request.json

    try:
        project = PastProjectOtherTINDV(
            application_no=data["applicationNo"],
            project_name=data["projectName"],
            project_type=data["projectType"],
            current_status=data["currentStatus"],
            project_address=data["projectAddress"],
            state=data["projectStateUT"],
            district=data["projectDistrict"],
            pin_code=data["pinCode"],
            survey_no=data["surveyNo"],
            actual_completion_date=data.get("actualCompletionDate"),
            expected_completion_date=data.get("expectedCompletionDate")
        )

        db.session.add(project)
        db.session.commit()

        return jsonify({"message": "Project saved successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
