from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy import text

from app.models.database import db
from app.models.agent_model import Agent
from app.models.agent_registration_model import AgentModel
from app.models.otp_model import AgentOTP

otp_bp = Blueprint("otp_bp", __name__)


# =================================================
# SEND EMAIL OTP (FINAL — NO app.utils)
# =================================================
@otp_bp.route("/send-email", methods=["POST"])
def send_email_otp():
    try:
        data = request.json
        pan = data.get("panNumber")

        if not pan:
            return jsonify({"error": "PAN number required"}), 400

        # ✅ STEP 1: Check PAN + email
        query = text("""
            SELECT id, email
            FROM agentregistration_details_t
            WHERE UPPER(pan) = :pan
            LIMIT 1
        """)

        row = db.session.execute(
            query, {"pan": pan.upper()}
        ).fetchone()

        if not row:
            return jsonify({"error": "PAN not registered"}), 404

        agent_id = row.id
        email = row.email

        if not email:
            return jsonify({"error": "Email not available"}), 400

        # ✅ STEP 2: Generate OTP
        otp = str(random.randint(100000, 999999))
        expiry = datetime.utcnow() + timedelta(minutes=5)

        # delete old otp
        db.session.execute(
            text("DELETE FROM agent_otp_t WHERE agent_id = :id"),
            {"id": agent_id}
        )

        # insert new otp
        db.session.execute(
            text("""
                INSERT INTO agent_otp_t
                    (agent_id, otp, created_at)
                VALUES
                    (:agent_id, :otp, NOW())
            """),
            {
                "agent_id": agent_id,
                "otp": otp
            }
        )

        db.session.commit()

        # =================================================
        # ✅ STEP 3: SEND EMAIL (INLINE)
        # =================================================
        config = current_app.config

        msg = MIMEMultipart()
        msg["From"] = config["FROM_EMAIL"]
        msg["To"] = email
        msg["Subject"] = "AP RERA OTP Verification"

        msg.attach(MIMEText(f"""
Dear Applicant,

Your OTP for Agent Registration verification is:

{otp}

This OTP is valid for 5 minutes.

Regards,
AP RERA
""", "plain"))

        server = smtplib.SMTP(
            config["SMTP_HOST"],
            config["SMTP_PORT"]
        )

        if config["SMTP_USE_TLS"]:
            server.starttls()

        server.login(
            config["SMTP_USER"],
            config["SMTP_PASSWORD"]
        )

        server.sendmail(
            config["FROM_EMAIL"],
            email,
            msg.as_string()
        )

        server.quit()

        return jsonify({
            "message": "OTP sent to registered email"
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": str(e)
        }), 500
@otp_bp.route("/verify", methods=["POST"])
def verify_otp():
    try:
        data = request.json
        pan = data.get("panNumber")
        otp = data.get("otp")

        if not pan or not otp:
            return jsonify({"error": "PAN and OTP are required"}), 400

        # 🔍 Get agent id
        query = text("""
            SELECT id
            FROM agentregistration_details_t
            WHERE UPPER(pan) = :pan
            LIMIT 1
        """)

        row = db.session.execute(
            query, {"pan": pan.upper()}
        ).fetchone()

        if not row:
            return jsonify({"error": "PAN not registered"}), 404

        agent_id = row.id

        # 🔐 Validate OTP
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
            return jsonify({"error": "Invalid or expired OTP"}), 401

        # ✅ Mark OTP verified
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