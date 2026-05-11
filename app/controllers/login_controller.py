import os
import logging
from flask import Blueprint, request, jsonify

from app.models.login_model import (
    get_emails_by_pan,
    get_projects_by_pan
)
from app.utils.otp_utils import generate_otp, verify_otp
from app.utils.mail_utils import send_otp_email

# =====================================================
# LOGGER SETUP (LOGIN CONTROLLER)
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "logs"))
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "login_controller.log")

logger = logging.getLogger("login_controller")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)

# =====================================================
# BLUEPRINT
# =====================================================
login_bp = Blueprint("login_bp", __name__)

# =====================================================
# TEST API
# =====================================================
@login_bp.route("/login/test", methods=["GET"])
def login_test():
    logger.info("TEST API HIT")
    return jsonify({
        "status": "success",
        "message": "Login API is working"
    }), 200


# =====================================================
# SEND OTP API
# =====================================================
@login_bp.route("/login/send-otp", methods=["POST"])
def send_otp():
    logger.info("========== /login/send-otp API HIT ==========")

    try:
        data = request.get_json(force=True)
        logger.info(f"Request JSON: {data}")

        pan = data.get("pan_number")

        if not pan:
            logger.warning("PAN missing in request")
            return jsonify({
                "message": "pan_number is required"
            }), 400

        emails = get_emails_by_pan(pan)
        logger.info(f"Emails fetched for PAN {pan}: {emails}")

        if not emails:
            logger.warning(f"PAN NOT FOUND: {pan}")
            return jsonify({
                "message": "PAN is not existing"
            }), 404

        otp = generate_otp(pan)
        logger.info(f"OTP generated for PAN {pan}")

        for email in emails:
            logger.info(f"Sending OTP to {email}")
            send_otp_email(email, otp)

        logger.info(f"OTP sent successfully for PAN {pan}")

        return jsonify({
            "message": "OTP sent successfully to registered email"
        }), 200

    except Exception as e:
        logger.exception("🔥 ERROR in send-otp")
        return jsonify({
            "message": "Internal Server Error",
            "error": str(e)
        }), 500


# =====================================================
# VERIFY OTP API (IMPORTANT – FIXES YOUR BUG)
# =====================================================
@login_bp.route("/login/verify-otp", methods=["POST"])
def verify_login_otp():
    logger.info("========== /login/verify-otp API HIT ==========")

    try:
        data = request.get_json(force=True)
        logger.info(f"Verify OTP Request: {data}")

        pan = data.get("pan_number")
        otp = data.get("otp")

        if not pan or not otp:
            return jsonify({
                "message": "pan_number and otp are required"
            }), 400

        # 🔐 ACTUAL OTP VALIDATION
        is_valid = verify_otp(pan, otp)

        if not is_valid:
            logger.warning(f"INVALID / EXPIRED OTP for PAN {pan}")
            return jsonify({
                "message": "Invalid or expired OTP"
            }), 401

        logger.info(f"OTP VERIFIED SUCCESSFULLY for PAN {pan}")

        # Optional: Fetch projects after login
        projects = get_projects_by_pan(pan)

        return jsonify({
            "message": "OTP verified successfully",
            "pan_number": pan,
            "projects": projects
        }), 200

    except Exception as e:
        logger.exception("🔥 ERROR in verify-otp")
        return jsonify({
            "message": "Internal Server Error",
            "error": str(e)
        }), 500