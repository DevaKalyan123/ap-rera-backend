import os
import logging
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.models.database import db
from app.models.promoter_registration_model import PromoterRegistration

promoter_registration_bp = Blueprint(
    "promoter_registration_bp", __name__
)

# ============================
# LOGGER SETUP (SAFE VERSION)
# ============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "..", "logs")

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "promoter_registration.log")

logger = logging.getLogger("promoter_registration_logger")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler(LOG_FILE)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


# ============================
# HELPER (SAFE FORM VALUE)
# ============================
def safe_get(field):
    value = request.form.get(field)
    return value.strip() if value else None


# ============================
# POST: PROMOTER REGISTRATION
# ============================
@promoter_registration_bp.route(
    "/promoter/registration", methods=["POST"]
)
def promoter_registration():
    logger.info("========== PROMOTER REGISTRATION START ==========")

    try:
        # ----------------------------
        # Incoming Logs
        # ----------------------------
        logger.info(f"Incoming POST form data: {dict(request.form)}")
        logger.info(f"Incoming FILES: {request.files}")

        # ----------------------------
        # OPTIONAL FILE UPLOAD
        # ----------------------------
        file = request.files.get("upload_document")
        file_path = None

        if file and file.filename:
            original_filename = secure_filename(file.filename)

            # Auto-generate safe filename
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            pan = safe_get("pan_number") or "UNKNOWN"
            ext = os.path.splitext(original_filename)[1]

            new_filename = f"promoter_registration_{pan}_{timestamp}{ext}"

            upload_dir = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                "promoter_doc"
            )
            os.makedirs(upload_dir, exist_ok=True)

            file_path = os.path.join(upload_dir, new_filename)
            file.save(file_path)

            logger.info(f"File saved successfully at: {file_path}")
        else:
            logger.info("No document uploaded (allowed)")

        # ----------------------------
        # DB Save
        # ----------------------------
        promoter = PromoterRegistration(
            pan_number=safe_get("pan_number"),
            user_type=safe_get("user_type"),
            select_category=safe_get("select_category"),
            name_applicant=safe_get("name_applicant"),
            father_name=safe_get("father_name"),
            mobile_number=safe_get("mobile_number"),
            email_id=safe_get("email_id"),
            state=safe_get("state"),
            district=safe_get("district"),
            upload_document=file_path,
            name_organisation=safe_get("name_organisation"),
            type_of_promoter=safe_get("type_of_promoter")
        )

        db.session.add(promoter)
        db.session.commit()

        logger.info(
            f"DB INSERT SUCCESS | promoter_id={promoter.promoter_id}"
        )

        response = {
            "message": "Promoter registration successful",
            "promoter_id": promoter.promoter_id
        }

        logger.info(f"Outgoing Response: {response}")
        logger.info("========== PROMOTER REGISTRATION END ==========")

        return jsonify(response), 201

    except Exception as e:
        db.session.rollback()
        logger.exception("PROMOTER REGISTRATION FAILED")
        return jsonify({"error": str(e)}), 500


# ============================
# GET: FETCH PROMOTER (DEBUG)
# ============================
@promoter_registration_bp.route(
    "/promoter/registration/<int:promoter_id>",
    methods=["GET"]
)
def get_promoter(promoter_id):
    logger.info(f"Incoming GET request | promoter_id={promoter_id}")

    promoter = PromoterRegistration.query.get(promoter_id)

    if not promoter:
        logger.warning("Promoter not found")
        return jsonify({"error": "Not found"}), 404

    data = {
        "promoter_id": promoter.promoter_id,
        "pan_number": promoter.pan_number,
        "name_applicant": promoter.name_applicant,
        "email_id": promoter.email_id,
        "upload_document": promoter.upload_document
    }

    logger.info(f"Outgoing GET data: {data}")
    return jsonify(data), 200


@promoter_registration_bp.route(
    "/check-promoter/<promoter_register_id>", methods=["GET"]
)
def check_promoter(promoter_register_id):
    try:
        exists = PromoterRegistration.is_promoter_exists(promoter_register_id)

        return jsonify({"exists": exists}), 200

    except Exception as e:
        return jsonify({"exists": False, "error": str(e)}), 500
