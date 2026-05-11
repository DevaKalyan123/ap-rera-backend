from flask import Blueprint, request, jsonify
from app.models.projectapplicationdetailsextension import (
    get_project_basic_details_by_application_no1
)

projectapplicationdetailsextension_bp = Blueprint(
    "projectapplicationdetailsextension_bp",
    __name__
)

@projectapplicationdetailsextension_bp.route(
    "/project/basic-details-by-application",
    methods=["GET"]
)
def get_project_basic_details_by_application():
    application_number = request.args.get("applicationNumber")

    if not application_number:
        return jsonify({
            "success": False,
            "message": "applicationNumber is required"
        }), 400

    data = get_project_basic_details_by_application_no(application_number)

    return jsonify({
        "success": True,
        "data": data
    }), 200


