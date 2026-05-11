import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.models.database import db
from app.models.project_wizard import ProjectRegistration
from app.models.quarterly_update import QuarterlyUpdate
from app.models.quarterly_document import QuarterlyDocument
from datetime import datetime
from dateutil.relativedelta import relativedelta

quarterly_bp = Blueprint("quarterly_bp", __name__)

UPLOAD_FOLDER = "uploads/quarterly"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def generate_quarter_id(registration_date):
    today = datetime.now()

    diff = relativedelta(today, registration_date)
    total_months = diff.years * 12 + diff.months

    quarter_number = (total_months // 3) + 1

    if quarter_number < 1:
        quarter_number = 1

    if quarter_number > 4:
        quarter_number = 4  # Max 4 quarters only

    year = registration_date.year

    return f"Q{quarter_number}-{year}"


@quarterly_bp.route("/quarterly-update", methods=["POST"])
def create_quarterly():

    pan_number = request.form.get("panNumber")
    occupancy = request.form.get("occupancy")

    # 1️⃣ Find project using PAN
    project = ProjectRegistration.query.filter_by(
        pan_number=pan_number
    ).first()

    if not project:
        return jsonify({"error": "Invalid PAN"}), 400

    # 2️⃣ Generate Quarter ID
    # 2️⃣ Generate Quarter ID based on registration date
    registration_date = project.created_at
    quarter_id = generate_quarter_id(registration_date)

    # 3️⃣ Prevent duplicate quarter
    existing = QuarterlyUpdate.query.filter_by(
        project_id=project.id,
        quarter_id=quarter_id
    ).first()

    if existing:
        return jsonify({
            "error": f"{quarter_id} already submitted"
        }), 400

    # 4️⃣ Create Quarterly record
    quarterly = QuarterlyUpdate(
        project_id=project.id,
        quarter_id=quarter_id,
        occupancy=(occupancy == "YES"),
        status="DRAFT"
    )

    db.session.add(quarterly)
    db.session.commit()

    # 5️⃣ Save documents
    for key in request.files:
        file = request.files[key]
        if file:
            filename = secure_filename(file.filename)
            path = os.path.join(
                UPLOAD_FOLDER,
                f"{quarterly.id}_{filename}"
            )
            file.save(path)

            doc = QuarterlyDocument(
                quarterly_id=quarterly.id,
                document_type=key,
                file_path=path
            )
            db.session.add(doc)

    db.session.commit()

    return jsonify({
        "message": "Quarterly Update Created",
        "quarter_id": quarter_id
    }), 201


# =========================
# GET CURRENT QUARTER
# =========================
@quarterly_bp.route("/current-quarter", methods=["GET"])
def get_current_quarter():

    pan_number = request.args.get("panNumber")

    project = ProjectRegistration.query.filter_by(
        pan_number=pan_number
    ).first()

    if not project:
        return jsonify({"error": "Invalid PAN"}), 400

    registration_date = project.created_at
    quarter_id = generate_quarter_id(registration_date)

    return jsonify({"quarter_id": quarter_id})