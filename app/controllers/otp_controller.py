from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import random
import resend
import os

from sqlalchemy import text

from app.models.database import db
from app.models.agent_model import Agent
from app.models.agent_registration_model import AgentModel
from app.models.otp_model import AgentOTP

otp_bp = Blueprint("otp_bp", __name__)

# =========================================
# RESEND API KEY
# =========================================

resend.api_key = os.getenv("RESEND_API_KEY")


# =================================================
# SEND EMAIL OTP
# =================================================
@otp_bp.route("/send-email", methods=["POST"])
def send_email_otp():

    try:

        data = request.json

        pan = data.get("panNumber")

        if not pan:

            return jsonify({
                "error": "PAN number required"
            }), 400

        # =========================================
        # CHECK PAN + EMAIL
        # =========================================

        query = text("""
            SELECT id, email
            FROM agentregistration_details_t
            WHERE UPPER(pan) = :pan
            LIMIT 1
        """)

        row = db.session.execute(
            query,
            {"pan": pan.upper()}
        ).fetchone()

        if not row:

            return jsonify({
                "error": "PAN not registered"
            }), 404

        agent_id = row.id
        email = row.email

        if not email:

            return jsonify({
                "error": "Email not available"
            }), 400

        # =========================================
        # GENERATE OTP
        # =========================================

        otp = str(random.randint(100000, 999999))

        expiry = datetime.utcnow() + timedelta(minutes=5)

        # DELETE OLD OTP
        db.session.execute(
            text("""
                DELETE FROM agent_otp_t
                WHERE agent_id = :id
            """),
            {"id": agent_id}
        )

        # INSERT NEW OTP
        db.session.execute(
            text("""
                INSERT INTO agent_otp_t
                (
                    agent_id,
                    otp,
                    created_at
                )
                VALUES
                (
                    :agent_id,
                    :otp,
                    NOW()
                )
            """),
            {
                "agent_id": agent_id,
                "otp": otp
            }
        )

        db.session.commit()

        print("================================")
        print("OTP GENERATED:", otp)
        print("SENDING MAIL TO:", email)
        print("================================")

        # =========================================
        # SEND EMAIL USING RESEND
        # =========================================

        params = {

            "from": "onboarding@resend.dev",

            "to": [email],

            "subject": "AP RERA OTP Verification",

            "html": f"""
                <h2>AP RERA OTP Verification</h2>

                <p>
                    Dear Applicant,
                </p>

                <h1>
                    {otp}
                </h1>

                <p>
                    This OTP is valid for 5 minutes.
                </p>

                <br>

                <p>
                    Regards,<br>
                    AP RERA
                </p>
            """,
        }

        resend.Emails.send(params)

        print("OTP MAIL SENT SUCCESSFULLY")

        return jsonify({
            "message": "OTP sent to registered email"
        }), 200

    except Exception as e:

        db.session.rollback()

        print("MAIL ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 500


# =================================================
# VERIFY OTP
# =================================================
@otp_bp.route("/verify", methods=["POST"])
def verify_otp():

    try:

        data = request.json

        pan = data.get("panNumber")

        otp = data.get("otp")

        if not pan or not otp:

            return jsonify({
                "error": "PAN and OTP are required"
            }), 400

        # =========================================
        # GET AGENT ID
        # =========================================

        query = text("""
            SELECT id
            FROM agentregistration_details_t
            WHERE UPPER(pan) = :pan
            LIMIT 1
        """)

        row = db.session.execute(
            query,
            {"pan": pan.upper()}
        ).fetchone()

        if not row:

            return jsonify({
                "error": "PAN not registered"
            }), 404

        agent_id = row.id

        # =========================================
        # VERIFY OTP
        # =========================================

        otp_row = db.session.execute(
            text("""
                SELECT id
                FROM agent_otp_t
                WHERE agent_id = :agent_id
                  AND otp = :otp
                  AND created_at >= NOW() - INTERVAL '5 minutes'
                ORDER BY created_at DESC
                LIMIT 1
            """),
            {
                "agent_id": agent_id,
                "otp": otp
            }
        ).fetchone()

        if not otp_row:

            return jsonify({
                "error": "Invalid or expired OTP"
            }), 401

        # =========================================
        # MARK VERIFIED
        # =========================================

        db.session.execute(
            text("""
                UPDATE agent_otp_t
                SET is_verified = true
                WHERE id = :id
            """),
            {"id": otp_row.id}
        )

        db.session.commit()

        return jsonify({
            "message": "OTP verified successfully"
        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 500