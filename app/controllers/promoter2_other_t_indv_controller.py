from flask import Blueprint, request, jsonify
from app import db
from app.models.promoter2_other_t_indv import Promoter2OtherTINDV

promoter2_other_t_indv_bp = Blueprint("promoter2_other_t_indv_bp", __name__)

@promoter2_other_t_indv_bp.route("/api/other-t-indv/promoter2/add", methods=["POST"])
def add_promoter2():
    data = request.json

    try:
        promoter2 = Promoter2OtherTINDV(
            application_no=data["applicationNo"],
            is_organization=data["isOrganization"],
            is_indian=data["isIndian"],
            name=data["name"],
            state=data["state"],
            district=data["district"],
            address_line1=data["addressLine1"],
            address_line2=data["addressLine2"],
            pin_code=data["pinCode"],
            mobile=data["mobile"],
            email=data["email"],
            pan_card=data["panCard"],
            aadhaar=data.get("aadhaar"),
            passport_no=data.get("passportNo")
        )

        db.session.add(promoter2)
        db.session.commit()

        return jsonify({"message": "Promoter2 saved successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
