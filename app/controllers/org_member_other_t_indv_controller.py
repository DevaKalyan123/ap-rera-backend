from flask import Blueprint, request, jsonify
from app import db
from app.models.org_member_other_t_indv import OrgMemberOtherTINDV

org_member_other_t_indv_bp = Blueprint("org_member_other_t_indv_bp", __name__)

# ===============================
# ADD MEMBER
# ===============================
@org_member_other_t_indv_bp.route("/api/other-t-indv/member/add", methods=["POST"])
def add_org_member():

    data = request.json

    try:
        member = OrgMemberOtherTINDV(
            application_no=data["applicationNo"],
            is_indian=data["isIndian"],
            name=data["name"],
            designation=data["designation"],
            mobile=data["mobile"],
            email=data["email"],
            address_line1=data["addressLine1"],
            address_line2=data["addressLine2"],
            state=data["state"],
            district=data["district"],
            pin_code=data["pinCode"],
            aadhaar=data["aadhaar"],
            pan=data["pan"],
            din=data["din"]
        )

        db.session.add(member)
        db.session.commit()

        return jsonify({"message": "Member added successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# ===============================
# GET MEMBERS
# ===============================
@org_member_other_t_indv_bp.route("/api/other-t-indv/member/<application_no>", methods=["GET"])
def get_members(application_no):

    members = OrgMemberOtherTINDV.query.filter_by(
        application_no=application_no
    ).all()

    result = []

    for m in members:
        result.append({
            "id": m.id,
            "name": m.name,
            "designation": m.designation,
            "mobile": m.mobile,
            "email": m.email
        })

    return jsonify(result), 200


# ===============================
# DELETE MEMBER
# ===============================
@org_member_other_t_indv_bp.route("/api/other-t-indv/member/delete/<int:id>", methods=["DELETE"])
def delete_member(id):

    member = OrgMemberOtherTINDV.query.get(id)

    if not member:
        return jsonify({"error": "Member not found"}), 404

    db.session.delete(member)
    db.session.commit()

    return jsonify({"message": "Member deleted successfully"}), 200
