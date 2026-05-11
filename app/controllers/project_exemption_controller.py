import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app import db
from app.models.project_exemption_model import ProjectExemption

project_exemption_bp = Blueprint("project_exemption", __name__)

# 📂 Upload Folder
UPLOAD_FOLDER = "backend/uploads/exemption"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ---------------- CREATE ----------------
@project_exemption_bp.route("/create", methods=["POST"])
def create_project_exemption():
    try:
        data = request.form

        def save_file(file_key):
            file = request.files.get(file_key)
            if file:
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                return filepath
            return None

        new_record = ProjectExemption(
            name=data.get("name"),
            mobile_no=data.get("mobile_no"),
            email=data.get("email"),
            address=data.get("address"),
            ba_number=data.get("ba_number"),

            plan_proceedings_path=save_file("plan_proceedings"),
            request_letter_path=save_file("request_letter"),
            land_document_path=save_file("land_document"),
            advocate_document_path=save_file("advocate_document"),
        )

        db.session.add(new_record)
        db.session.commit()

        return jsonify({"message": "Created Successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- GET ALL ----------------
@project_exemption_bp.route("/all", methods=["GET"])
def get_all():
    records = ProjectExemption.query.all()

    result = []
    for r in records:
        result.append({
            "id": r.id,
            "name": r.name,
            "mobile_no": r.mobile_no,
            "email": r.email,
            "plan_proceedings_path": r.plan_proceedings_path,
            "request_letter_path": r.request_letter_path,
        })

    return jsonify(result)


# ---------------- GET BY ID ----------------
@project_exemption_bp.route("/<int:id>", methods=["GET"])
def get_by_id(id):
    record = ProjectExemption.query.get(id)

    if not record:
        return jsonify({"message": "Not found"}), 404

    return jsonify({
        "id": record.id,
        "name": record.name,
        "mobile_no": record.mobile_no,
        "email": record.email
    })


# ---------------- UPDATE ----------------
@project_exemption_bp.route("/update/<int:id>", methods=["PUT"])
def update(id):
    record = ProjectExemption.query.get(id)

    if not record:
        return jsonify({"message": "Not found"}), 404

    data = request.json

    record.name = data.get("name", record.name)
    record.mobile_no = data.get("mobile_no", record.mobile_no)
    record.email = data.get("email", record.email)

    db.session.commit()

    return jsonify({"message": "Updated Successfully"})


# ---------------- DELETE ----------------
@project_exemption_bp.route("/delete/<int:id>", methods=["DELETE"])
def delete(id):
    record = ProjectExemption.query.get(id)

    if not record:
        return jsonify({"message": "Not found"}), 404

    db.session.delete(record)
    db.session.commit()

    return jsonify({"message": "Deleted Successfully"})