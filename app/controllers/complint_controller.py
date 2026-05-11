from flask import Blueprint, request, jsonify
from app.models.database import db
from app.models.complint_complainant import ComplintComplainant
from app.models.complint_respondent import ComplintRespondent
from app.models.complint_complaint import ComplintComplaint
from datetime import datetime
from sqlalchemy import text
from flask import send_from_directory
from app.utils.mail_service import (
    send_complaint_approval_mail_complainant,
    send_complaint_approval_mail_respondent_with_pdf,
    send_complaint_closed_mail_complainant,
    send_complaint_closed_mail_respondent,
)
from app.models.complaint_hearing import ComplaintHearing
from flask import request, jsonify
import os
import uuid
import logging
import traceback

complint_bp = Blueprint("complint_bp", __name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LOG_DIR = os.path.join(BASE_DIR, "logs")
UPLOAD_DIR = os.path.join(BASE_DIR, "app", "uploads", "complint_doc")

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

logger = logging.getLogger("complint_logger")
if not logger.handlers:
    handler = logging.FileHandler(os.path.join(LOG_DIR, "complint.log"))
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def generate_complaint_id():
    now = datetime.now()
    return int(now.strftime("%d%m%y%H%M%S"))


def generate_complaint_register_no(district):
    from datetime import datetime
    from sqlalchemy import text

    current_year = str(datetime.now().year)
    district_code = (district[:3] if district else "UNK").upper()

    counter = db.session.execute(
        text(
            """
            SELECT last_number FROM complaint_counter
            WHERE district = :district AND year = :year
        """
        ),
        {"district": district_code, "year": current_year},
    ).fetchone()

    if counter:
        next_number = counter[0] + 1

        db.session.execute(
            text(
                """
                UPDATE complaint_counter
                SET last_number = :num
                WHERE district = :district AND year = :year
            """
            ),
            {"num": next_number, "district": district_code, "year": current_year},
        )
    else:
        next_number = 1

        db.session.execute(
            text(
                """
                INSERT INTO complaint_counter (district, year, last_number)
                VALUES (:district, :year, :num)
            """
            ),
            {"district": district_code, "year": current_year, "num": next_number},
        )

    return f"{district_code}{str(next_number).zfill(6)}{current_year}"


@complint_bp.route("/complint/create", methods=["POST"])
def create_complint():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "JSON body required"}), 400

        c = data.get("complainant", {})
        r = data.get("respondent", {})
        comp = data.get("complaint", {})
        project = comp.get("project", {})

        # ---------- Complainant ----------
        complainant = ComplintComplainant(
            complainant_registered_id=c.get("registered_id"),
            complainant_type=c.get("type"),
            name=c.get("name"),
            mobile_no=c.get("mobile"),
            email=c.get("email"),
            address_line1=c.get("address_line1"),
            address_line2=c.get("address_line2"),
            state=c.get("state"),
            district=c.get("district"),
            pincode=c.get("pincode"),
        )
        db.session.add(complainant)
        db.session.flush()

        respondent = ComplintRespondent(
            registered_id=r.get("registered_id"),
            respondent_type=r.get("type"),
            is_rera_registered=r.get("is_rera_registered", False),
            registration_id=r.get("registration_id"),
            name=r.get("name"),
            phone=r.get("phone"),
            email=r.get("email"),
            project_name=r.get("project_name"),
            address_line1=r.get("address_line1"),
            address_line2=r.get("address_line2"),
            state=r.get("state"),
            district=r.get("district"),
            pincode=r.get("pincode"),
        )
        db.session.add(respondent)
        db.session.flush()

        complaint_register_no = generate_complaint_register_no(complainant.district)

        complaint = ComplintComplaint(
            complaint_id=generate_complaint_id(),
            complainant_id=complainant.complainant_id,
            respondent_id=respondent.respondent_id,
            subject=comp.get("subject"),
            relief_sought=comp.get("relief_sought"),
            complaint_regarding=comp.get("complaint_regarding"),
            application_type=comp.get("application_type"),
            description=comp.get("description"),
            complaint_facts=comp.get("complaint_facts"),
            project_details=project,
            complaint_documents={},
            supporting_documents=[],
            complaint_register_no=complaint_register_no,
        )

        db.session.add(complaint)
        db.session.commit()

        logger.info(
            f"Complaint created | ID={complaint.complaint_id} | REG={complaint_register_no}"
        )

        return jsonify(
            {
                "status": "success",
                "complaint_id": complaint.complaint_id,
                "complaint_register_no": complaint_register_no,
            }
        )

    except Exception:
        db.session.rollback()
        logger.error(traceback.format_exc())
        return jsonify({"status": "error"}), 500


@complint_bp.route("/complint/upload-complaint-documents", methods=["POST"])
def upload_complaint_documents():
    try:
        complaint_id = request.form.get("complaint_id")
        doc_type = request.form.get("type")
        file = request.files.get("document")

        if not complaint_id or not doc_type or not file:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "complaint_id, type, document required",
                    }
                ),
                400,
            )

        complaint = ComplintComplaint.query.get(complaint_id)
        if not complaint:
            return jsonify({"status": "error", "message": "Complaint not found"}), 404

        filename = f"{uuid.uuid4()}_{file.filename}"
        file.save(os.path.join(UPLOAD_DIR, filename))

        docs = dict(complaint.complaint_documents or {})

        docs[doc_type] = filename

        complaint.complaint_documents = docs
        db.session.commit()

        logger.info(f"Complaint document uploaded | {doc_type} | ID={complaint_id}")

        return jsonify({"status": "success", "complaint_documents": docs})

    except Exception:
        db.session.rollback()
        logger.error(traceback.format_exc())
        return jsonify({"status": "error"}), 500


@complint_bp.route("/complint/upload-supporting-documents", methods=["POST"])
def upload_supporting_documents():
    try:
        complaint_id = request.form.get("complaint_id")
        descriptions = request.form.getlist("document_description")
        files = request.files.getlist("documents")

        if not complaint_id:
            return jsonify({"status": "error", "message": "complaint_id required"}), 400

        if len(descriptions) != len(files):
            return (
                jsonify(
                    {"status": "error", "message": "Description & file count mismatch"}
                ),
                400,
            )

        complaint = ComplintComplaint.query.get(complaint_id)
        if not complaint:
            return jsonify({"status": "error", "message": "Complaint not found"}), 404

        docs = complaint.supporting_documents or []

        for desc, file in zip(descriptions, files):
            filename = f"{uuid.uuid4()}_{file.filename}"
            file.save(os.path.join(UPLOAD_DIR, filename))

            docs.append({"description": desc, "document": filename})

        complaint.supporting_documents = docs
        db.session.commit()

        logger.info(f"Supporting documents uploaded | ID={complaint_id}")

        return jsonify({"status": "success", "count": len(docs), "documents": docs})

    except Exception:
        db.session.rollback()
        logger.error(traceback.format_exc())
        return jsonify({"status": "error"}), 500


@complint_bp.route("/complint/<complaint_id>", methods=["GET"])
def get_complaint(complaint_id):
    try:

        complaint = ComplintComplaint.query.get_or_404(complaint_id)

        complainant = ComplintComplainant.query.get(complaint.complainant_id)
        respondent = ComplintRespondent.query.get(complaint.respondent_id)

        hearings = (
            ComplaintHearing.query.filter_by(complaint_id=complaint_id)
            .order_by(ComplaintHearing.hearing_no.asc())
            .all()
        )

        hearing_list = []

        for h in hearings:
            hearing_list.append(
                {
                    "hearing_id": h.hearing_id,
                    "hearing_no": h.hearing_no,
                    "hearing_date": (
                        h.hearing_date.strftime("%d-%m-%Y %H:%M:%S")
                        if h.hearing_date
                        else None
                    ),
                    "next_hearing_date": (
                        h.next_hearing_date.strftime("%d-%m-%Y %H:%M:%S")
                        if h.next_hearing_date
                        else None
                    ),
                    "hearing_place": h.hearing_place,
                    "remarks": h.remarks,
                    "status": h.status,
                    "documents": h.documents,
                }
            )

        return jsonify(
            {
                "complaint": {
                    "complaint_id": complaint.complaint_id,
                    "subject": complaint.subject,
                    "relief_sought": complaint.relief_sought,
                    "application_type": complaint.application_type,
                    "complaint_regarding": complaint.complaint_regarding,
                    "description": complaint.description,
                    "complaint_facts": complaint.complaint_facts,
                    "complaint_documents": complaint.complaint_documents,
                    "supporting_documents": complaint.supporting_documents,
                    "project_details": complaint.project_details,
                    "reject_reson": complaint.reject_reson,
                    "status": complaint.status,
                    "created_at": (
                        complaint.created_at.strftime("%d-%m-%Y %H:%M:%S")
                        if complaint.created_at
                        else None
                    ),
                },
                "complainant": {
                    "name": complainant.name,
                    "type": complainant.complainant_type,
                    "mobile": complainant.mobile_no,
                    "email": complainant.email,
                    "address": {
                        "line1": complainant.address_line1,
                        "line2": complainant.address_line2,
                        "state": complainant.state,
                        "district": complainant.district,
                        "pincode": complainant.pincode,
                    },
                },
                "respondent": {
                    "name": respondent.name,
                    "type": respondent.respondent_type,
                    "project_name": respondent.project_name,
                    "mobile": respondent.phone,
                    "email": respondent.email,
                    "is_rera_registered": respondent.is_rera_registered,
                    "registration_id": respondent.registration_id,
                    "address": {
                        "line1": respondent.address_line1,
                        "line2": respondent.address_line2,
                        "state": respondent.state,
                        "district": respondent.district,
                        "pincode": respondent.pincode,
                    },
                },
                "hearings": hearing_list,
            }
        )

    except Exception as e:
        logger.error(traceback.format_exc())
        return (
            jsonify(
                {"status": "error", "message": "Unable to fetch complaint details"}
            ),
            500,
        )


@complint_bp.route("/complint/list", methods=["GET"])
def list_complaints():
    try:
        complaints = ComplintComplaint.query.order_by(
            ComplintComplaint.created_at.desc()
        ).all()

        data = [
            {
                "complaint_id": c.complaint_id,
                "subject": c.subject,
                "status": c.status,
                "reject_reson": c.reject_reson,
                "complaint_register_no": c.complaint_register_no,
                "application_type": c.application_type,
                "created_at": (
                    c.created_at.strftime("%d-%m-%Y %H:%M:%S") if c.created_at else None
                ),
            }
            for c in complaints
        ]

        return jsonify({"status": "success", "total": len(data), "data": data})

    except Exception:
        logger.error(traceback.format_exc())
        return jsonify({"status": "error"}), 500


@complint_bp.route("/complint/document/<filename>", methods=["GET"])
def view_complaint_document(filename):
    try:
        return send_from_directory(UPLOAD_DIR, filename, as_attachment=False)
    except Exception:
        logger.error(traceback.format_exc())
        return jsonify({"error": "File not found"}), 404


@complint_bp.route("/complint/send-rejection-mail", methods=["POST"])
def send_complaint_rejection_mail():
    try:
        data = request.get_json()

        complaint_id = data.get("complaint_id")
        email = data.get("email")
        name = data.get("name")
        subject = data.get("subject")
        complaint_desc = data.get("description")
        admin_remark = data.get("admin_remark")

        if not complaint_id:
            return jsonify({"status": "error", "message": "Complaint ID required"}), 400

        if not email:
            return jsonify({"status": "error", "message": "Email required"}), 400

        if not name:
            return jsonify({"status": "error", "message": "Name required"}), 400

        if not subject:
            return jsonify({"status": "error", "message": "Subject required"}), 400

        complaint = ComplintComplaint.query.get(complaint_id)

        if not complaint:
            return jsonify({"status": "error", "message": "Complaint not found"}), 404

        complaint.reject_reson = admin_remark
        complaint.status = "rejected"
        db.session.commit()

        send_complaint_rejection_email(
            email=email,
            name=name,
            subject_text=subject,
            complaint_desc=complaint_desc,
            admin_remark=admin_remark,
        )

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Complaint Rejected & Mail Sent Successfully",
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@complint_bp.route("/complint/approve-mail", methods=["POST"])
def send_complaint_approval_mail():
    try:

        # ================= GET FORM DATA =================
        complainant_email = request.form.get("complainant_email")
        complainant_name = request.form.get("complainant_name")

        respondent_email = request.form.get("respondent_email")
        respondent_name = request.form.get("respondent_name")

        subject_text = request.form.get("subject")
        complaint_desc = request.form.get("description")
        admin_remark = request.form.get("admin_remark")

        complaint_id = request.form.get("complaint_id")
        hearing_date = request.form.get("hearing_date")
        next_hearing_date = request.form.get("next_hearing_date")
        hearing_place = request.form.get("hearing_place")
        remarks = request.form.get("remarks")
        status = request.form.get("status")

        notice_pdf = request.files.get("notice_pdf")

        # ================= GET COMPLAINT =================
        complaint = ComplintComplaint.query.get(complaint_id)

        if not complaint:
            return jsonify({"status": "error", "message": "Complaint not found"}), 404

        # =====================================================
        # 🔥 CASE 1: CLOSE COMPLAINT
        # =====================================================
        if status == "closed":

            # ✅ Update status
            complaint.status = "close"

            # ✅ Send mail to complainant
            if complainant_email:
                send_complaint_closed_mail_complainant(
                    complainant_email,
                    complainant_name,
                    subject_text,
                    complaint_desc,
                    admin_remark,
                )

            # ✅ Send mail to respondent
            if respondent_email:
                send_complaint_closed_mail_respondent(
                    respondent_email,
                    respondent_name,
                    complainant_name,
                    subject_text,
                    complaint_desc,
                    admin_remark,
                )

            db.session.commit()

            return jsonify(
                {
                    "status": "success",
                    "message": "Complaint closed & mails sent successfully",
                }
            )

        # =====================================================
        # 🔥 CASE 2: APPROVE (EXISTING LOGIC)
        # =====================================================

        # ✅ Send approval mail to complainant
        if complainant_email:
            send_complaint_approval_mail_complainant(
                complainant_email,
                complainant_name,
                subject_text,
                complaint_desc,
                admin_remark,
            )

        # ✅ Send approval mail to respondent with PDF
        if respondent_email:
            send_complaint_approval_mail_respondent_with_pdf(
                respondent_email,
                respondent_name,
                complainant_name,
                subject_text,
                complaint_desc,
                admin_remark,
                notice_pdf,
            )

        from app.models.complaint_hearing import ComplaintHearing

        # ================= DOCUMENTS =================
        documents_files = request.files.getlist("documents")
        documents_data = []

        for file in documents_files:
            if file:
                filename = f"{uuid.uuid4()}_{file.filename}"
                file.save(os.path.join(UPLOAD_DIR, filename))
                documents_data.append({"name": filename})

        # ================= CREATE HEARING =================
        if complaint_id and hearing_date:
            hearing = ComplaintHearing(
                complaint_id=complaint_id,
                hearing_no=1,
                hearing_date=datetime.fromisoformat(hearing_date),
                next_hearing_date=(
                    datetime.strptime(next_hearing_date, "%Y-%m-%dT%H:%M")
                    if next_hearing_date
                    else None
                ),
                hearing_place=hearing_place,
                remarks=remarks,
                status=status,
                documents=documents_data,
            )

            db.session.add(hearing)

            # ✅ Update complaint status to pending
            complaint.status = "pending"

            db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "Mails sent & First hearing created successfully",
            }
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@complint_bp.route("/complint/add-hearing", methods=["POST"])
def add_hearing():
    try:
        logger.info("🔄 add_hearing API called")

        # ================= GET DATA =================
        complaint_id = request.form.get("complaint_id")
        next_hearing_date_str = request.form.get("next_hearing_date")
        hearing_place = request.form.get("hearing_place")
        remarks = request.form.get("remarks")
        status = request.form.get("status")

        documents_files = request.files.getlist("documents")
        descriptions = request.form.getlist("descriptions")
        logger.info(
            f"📥 Incoming Data → complaint_id={complaint_id}, next_hearing_date={next_hearing_date_str}, status={status}"
        )

        # ================= VALIDATION =================
        if not complaint_id or not next_hearing_date_str:
            logger.warning("⚠ Missing required fields")
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "complaint_id & next_hearing_date required",
                    }
                ),
                400,
            )

        # ================= DATE PARSE =================
        try:
            next_hearing_date = datetime.strptime(
                next_hearing_date_str, "%Y-%m-%dT%H:%M"
            )
        except Exception as e:
            logger.error(f"❌ Date parsing failed: {str(e)}")
            return jsonify({"status": "error", "message": "Invalid date format"}), 400

        # ================= GET LAST HEARING =================
        last_hearing = (
            ComplaintHearing.query.filter_by(complaint_id=complaint_id)
            .order_by(ComplaintHearing.hearing_no.desc())
            .first()
        )

        # ================= AUTO LOGIC =================
        if last_hearing:
            hearing_no = (last_hearing.hearing_no or 0) + 1
            hearing_date = last_hearing.next_hearing_date
            if not hearing_date:
                hearing_date = datetime.now()

            logger.info(
                f"📌 Last hearing found → no={last_hearing.hearing_no}, next_date={last_hearing.next_hearing_date}"
            )

        else:
            hearing_no = 1
            hearing_date = next_hearing_date or datetime.now()

            logger.info("📌 First hearing (no previous record)")

        # ================= DOCUMENTS =================
        documents_data = []
        for i, file in enumerate(documents_files):
            if file:
                filename = f"{uuid.uuid4()}_{file.filename}"
                file.save(os.path.join(UPLOAD_DIR, filename))

                documents_data.append(
                    {
                        "description": descriptions[i] if i < len(descriptions) else "",
                        "name": filename,
                    }
                )

                logger.info(f"📎 File saved → {filename}")

        # ================= INSERT =================
        hearing = ComplaintHearing(
            complaint_id=complaint_id,
            hearing_no=hearing_no,
            hearing_date=hearing_date,
            next_hearing_date=next_hearing_date,
            hearing_place=hearing_place,
            remarks=remarks,
            status=status,
            documents=documents_data,
        )

        db.session.add(hearing)
        db.session.commit()

        logger.info(f"✅ Hearing inserted successfully → hearing_no={hearing_no}")

        return jsonify(
            {
                "status": "success",
                "message": "Hearing added successfully",
                "hearing_no": hearing_no,
            }
        )

    except Exception as e:
        logger.error(f"❌ ERROR in add_hearing → {str(e)}")
        logger.error(traceback.format_exc())

        db.session.rollback()

        return jsonify({"status": "error", "message": str(e)}), 500


@complint_bp.route("/complint/hearings/<complaint_id>", methods=["GET"])
def get_hearings(complaint_id):
    try:
        hearings = (
            ComplaintHearing.query.filter_by(complaint_id=complaint_id)
            .order_by(ComplaintHearing.hearing_no.asc())
            .all()
        )

        data = []

        for h in hearings:
            data.append(
                {
                    "hearing_id": h.hearing_id,
                    "hearing_no": h.hearing_no,
                    "hearing_date": (
                        h.hearing_date.strftime("%d-%m-%Y %H:%M:%S")
                        if h.hearing_date
                        else None
                    ),
                    "next_hearing_date": (
                        h.next_hearing_date.strftime("%d-%m-%Y %H:%M:%S")
                        if h.next_hearing_date
                        else None
                    ),
                    "hearing_place": h.hearing_place,
                    "remarks": h.remarks,
                    "status": h.status,
                    "documents": h.documents,
                }
            )

        return jsonify({"status": "success", "data": data})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500