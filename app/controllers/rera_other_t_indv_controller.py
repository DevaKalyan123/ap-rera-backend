from flask import Blueprint, request, jsonify
from app import db
from app.models.rera_other_t_indv import ReraOtherTINDV

rera_other_t_indv_bp = Blueprint("rera_other_t_indv_bp", __name__)

@rera_other_t_indv_bp.route("/api/other-t-indv/rera/add", methods=["POST"])
def add_rera_other():
    data = request.json

    try:
        rera = ReraOtherTINDV(
            application_no=data["applicationNo"],
            rera_reg_number=data["reraRegNumber"],
            rera_state=data["reraState"],
            registration_revoked=data["registrationRevoked"],
            revocation_reason=data.get("revocationReason")
        )

        db.session.add(rera)
        db.session.commit()

        return jsonify({"message": "RERA saved successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
