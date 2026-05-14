import random
import logging
from flask import Blueprint, request, jsonify
from sqlalchemy import text

from app.models.database import db
from app.utils.mail_utils import send_otp_email

admin_bp = Blueprint("admin_bp", __name__)

# =========================================
# TEMP OTP STORE
# =========================================
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

        # =========================================
        # VALIDATE INPUT
        # =========================================
        if not username or not password:

            return jsonify({
                "error": "Username and password required"
            }), 400

        # =========================================
        # GET ADMIN FROM DB
        # =========================================
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

        # =========================================
        # USERNAME CHECK
        # =========================================
        if not result:

            return jsonify({
                "error": "Invalid username"
            }), 401

        # =========================================
        # PASSWORD CHECK
        # =========================================
        if result["password"] != password:

            return jsonify({
                "error": "Invalid password"
            }), 401

        # =========================================
        # GENERATE OTP
        # =========================================
        otp = str(random.randint(100000, 999999))

        # STORE OTP
        otp_store[username] = otp

        print("===================================")
        print("LOGIN SUCCESS FOR:", username)
        print("OTP GENERATED:", otp)
        print("===================================")

        # =========================================
        # SEND EMAIL
        # =========================================
        try:

            send_otp_email(result["email"], otp)

            print("MAIL SENT SUCCESSFULLY")

        except Exception as mail_error:

            print("MAIL ERROR:", str(mail_error))

        # =========================================
        # SUCCESS RESPONSE
        # =========================================
        return jsonify({
            "message": "OTP generated successfully",
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

        # =========================================
        # VALIDATE INPUT
        # =========================================
        if not username or not otp:

            return jsonify({
                "error": "Username and OTP required"
            }), 400

        # =========================================
        # VERIFY OTP
        # =========================================
        stored_otp = otp_store.get(username)

        if stored_otp != otp:

            print("INVALID OTP")

            return jsonify({
                "error": "Invalid or expired OTP"
            }), 401

        # =========================================
        # GET ADMIN DETAILS
        # =========================================
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

        # =========================================
        # REMOVE OTP
        # =========================================
        otp_store.pop(username, None)

        print("OTP VERIFIED SUCCESSFULLY")

        # =========================================
        # SUCCESS RESPONSE
        # =========================================
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