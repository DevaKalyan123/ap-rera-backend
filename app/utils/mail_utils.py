import random
from flask import Blueprint, request, jsonify
from app.models.database import db
from sqlalchemy import text
from werkzeug.security import check_password_hash
from app.utils.mail_utils import send_otp_email

admin_bp = Blueprint("admin_bp", __name__)

# Temporary OTP store
otp_store = {}


@admin_bp.route("/admin/login", methods=["POST"])
def admin_login():
    try:
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password required"}), 400

        result = (
            db.session.execute(
                text(
                    """
                SELECT * FROM admin_master_t
                WHERE username = :u
                LIMIT 1
            """
                ),
                {"u": username},
            )
            .mappings()
            .fetchone()
        )

        if not result:
            return jsonify({"error": "Invalid username"}), 401

        # ✅ Plain password check
        if result["password"] != password:
            return jsonify({"error": "Invalid password"}), 401

        # OTP generation
        otp = str(random.randint(100000, 999999))
        otp_store[username] = otp

        send_otp_email(result["email"], otp)

        return (
            jsonify({"message": "OTP sent to registered email", "username": username}),
            200,
        )

    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500


# -------------------------------
# VERIFY OTP → RETURN FULL DATA
# -------------------------------
@admin_bp.route("/admin/verify-otp", methods=["POST"])
def verify_otp():
    try:
        data = request.get_json()

        username = data.get("username")
        otp = data.get("otp")

        if not username or not otp:
            return jsonify({"error": "Username and OTP required"}), 400

        if otp_store.get(username) != otp:
            return jsonify({"error": "Invalid OTP"}), 401

        result = (
            db.session.execute(
                text(
                    """
                SELECT * FROM admin_master_t
                WHERE username = :u
            """
                ),
                {"u": username},
            )
            .mappings()
            .fetchone()
        )

        if not result:
            return jsonify({"error": "Admin not found"}), 404

        # remove OTP after success
        otp_store.pop(username, None)

        return (
            jsonify(
                {
                    "message": "Login successful",
                    "admin": {
                        "id": result["id"],
                        "username": result["username"],
                        "full_name": result["full_name"],
                        "email": result["email"],
                        "phone": result["phone"],
                        "role": result["role"],
                        "department": result["department"],
                        "photo": result["photo"],
                        "employee_id": result["employee_id"],
                        "state": result["state"],
                        "district": result["district"],
                        "mandal": result["mandal"],
                        "village": result["village"],
                        "pincode": result["pincode"],
                    },
                }
            ),
            200,
        )

    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500