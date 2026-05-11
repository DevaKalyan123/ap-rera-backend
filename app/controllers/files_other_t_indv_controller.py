import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app import db
from app.models.files_other_t_indv import FilesOtherTINDV

files_other_t_indv_bp = Blueprint("files_other_t_indv_bp", __name__)

UPLOAD_FOLDER = "uploads/Other_t_INDV"

@files_other_t_indv_bp.route("/api/other-t-indv/files/upload", methods=["POST"])
def upload_file_other():
    application_no = request.form.get("applicationNo")
    file_category = request.form.get("fileCategory")
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    folder = os.path.join(UPLOAD_FOLDER, application_no)
    os.makedirs(folder, exist_ok=True)

    filename = secure_filename(file.filename)
    file_path = os.path.join(folder, filename)
    file.save(file_path)

    record = FilesOtherTINDV(
        application_no=application_no,
        file_category=file_category,
        file_name=filename,
        file_path=file_path
    )

    db.session.add(record)
    db.session.commit()

    return jsonify({"message": "File uploaded successfully"}), 201
