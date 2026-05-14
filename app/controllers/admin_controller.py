import random
from flask import Blueprint, request, jsonify
from sqlalchemy import text

from app.models.database import db
from app.utils.mail_utils import send_otp_email

admin_bp = Blueprint("admin_bp", __name__)

# Temporary OTP store
otp_store = {}


# =========================================
# ADMIN LOGIN
# =========================================
@admin_bp.route("/admin/login", methods=["POST"])
def admin_login():

    try:

        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        # VALIDATE INPUT
        if not username or not password:
            return jsonify({
                "error": "Username and password required"
            }), 400

        # GET ADMIN
        result = (
            db.session.execute(
                text("""
                    SELECT *
                    FROM admin_master_t
                    WHERE username = :u
                    LIMIT 1
                """),
                {"u": username},
            )
            .mappings()
            .fetchone()
        )

        # USERNAME CHECK
        if not result:
            return jsonify({
                "error": "Invalid username"
            }), 401

        # PASSWORD CHECK
        if result["password"] != password:
            return jsonify({
                "error": "Invalid password"
            }), 401

        # =========================================
        # OTP GENERATION
        # =========================================

        otp = str(random.randint(100000, 999999))

        # Store OTP
        otp_store[username] = otp

        print("===================================")
        print("LOGIN SUCCESS")
        print("USERNAME:", username)
        print("OTP:", otp)
        print("===================================")

        # SEND OTP EMAIL
        send_otp_email(result["email"], otp)

        return jsonify({
            "message": "OTP sent successfully",
            "username": username
        }), 200

    except Exception as e:

        print("LOGIN ERROR:", str(e))

        return jsonify({
            "error": "Internal server error"
        }), 500


# =========================================
# VERIFY OTP
# =========================================
@admin_bp.route("/admin/verify-otp", methods=["POST"])
def verify_otp():

    try:

        data = request.get_json()

        username = data.get("username")
        otp = data.get("otp")

        # VALIDATE INPUT
        if not username or not otp:
            return jsonify({
                "error": "Username and OTP required"
            }), 400

        # VERIFY OTP
        if otp_store.get(username) != otp:
            return jsonify({
                "error": "Invalid or expired OTP"
            }), 401

        # GET ADMIN DETAILS
        result = (
            db.session.execute(
                text("""
                    SELECT *
                    FROM admin_master_t
                    WHERE username = :u
                """),
                {"u": username},
            )
            .mappings()
            .fetchone()
        )

        if not result:
            return jsonify({
                "error": "Admin not found"
            }), 404

        # REMOVE OTP
        otp_store.pop(username, None)

        return jsonify({
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
            }
        }), 200

    except Exception as e:

        print("VERIFY OTP ERROR:", str(e))

        return jsonify({
            "error": "Internal server error"
        }), 500