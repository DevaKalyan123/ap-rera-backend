from app.models.database import db
from sqlalchemy import text
from datetime import datetime, timedelta
from app.utils.mail_service import send_email_otp
import json
import random


class AgentModel:

    # ================= STEP 1 =================
    @staticmethod
    def create_agent_registration_step1(data):
        try:
            application_no = datetime.now().strftime("%Y%m%d") + str(random.randint(10000, 99999))

            query = text("""
                INSERT INTO agentregistration_details_t (
                    agent_type,
                    application_no,
                    agent_name,
                    father_name,
                    occupation_id,
                    email,
                    aadhaar,
                    pan,
                    mobile,
                    landline,
                    license_number,
                    license_date,
                    address1,
                    address2,
                    state_id,
                    district,
                    mandal,
                    village,
                    pincode,
                    photograph,
                    pan_proof,
                    address_proof,
                    self_declared_affidavit,
                    last_five_years_project_details,
                    any_civil_criminal_cases,
                    registration_other_states,
                    declaration
                )
                VALUES (
                    :agent_type,
                    :application_no,
                    :agent_name,
                    :father_name,
                    :occupation_id,
                    :email,
                    :aadhaar,
                    :pan,
                    :mobile,
                    :landline,
                    :license_number,
                    :license_date,
                    :address1,
                    :address2,
                    :state_id,
                    :district,
                    :mandal,
                    :village,
                    :pincode,
                    CAST(:photograph AS jsonb),
                    CAST(:pan_proof AS jsonb),
                    CAST(:address_proof AS jsonb),
                    CAST(:self_declared_affidavit AS jsonb),
                    :last_five_years_project_details,
                    :any_civil_criminal_cases,
                    :registration_other_states,
                    TRUE
                )
                RETURNING id, application_no
            """)

            params = {
                **data,
                "application_no": application_no,
                "photograph": json.dumps(data["photograph"]),
                "pan_proof": json.dumps(data["pan_proof"]),
                "address_proof": json.dumps(data["address_proof"]),

                # ✅ IMPORTANT
                "self_declared_affidavit": json.dumps(data["self_declared_affidavit"]) if data.get("self_declared_affidavit") else None,
                "last_five_years_project_details": data.get("last_five_years_project_details"),
                "any_civil_criminal_cases": data.get("any_civil_criminal_cases"),
                "registration_other_states": data.get("registration_other_states"),
            }

            result = db.session.execute(query, params)
            row = result.fetchone()
            db.session.commit()

            return {
                "success": True,
                "agent_id": row.id,
                "application_no": row.application_no
            }

        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": str(e)}


    # ================= INSERT PROJECTS =================
    @staticmethod
    def insert_agent_projects(agent_id, projects):
        try:
            query = text("""
                INSERT INTO agent_projects_t (agent_id, project_name)
                VALUES (:agent_id, :project_name)
            """)

            for p in projects:
                db.session.execute(query, {
                    "agent_id": agent_id,
                    "project_name": p.get("name")
                })

            db.session.commit()
            return {"success": True}

        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": str(e)}

    @staticmethod
    def insert_agent_litigations(agent_id, litigations):
        try:
            query = text("""
                INSERT INTO agent_litigations_t
                (
                    agent_id,
                    case_no,
                    tribunal_place,
                    petitioner_name,
                    respondent_name,
                    case_facts,
                    present_status,
                    interim_order,
                    final_order,
                    interim_order_certificate,
                    disposed_certificate
                )
                VALUES
                (
                    :agent_id,
                    :case_no,
                    :tribunal_place,
                    :petitioner_name,
                    :respondent_name,
                    :case_facts,
                    :present_status,
                    :interim_order,
                    :final_order,
                    CAST(:interim_order_certificate AS jsonb),
                    CAST(:disposed_certificate AS jsonb)
                )
            """)

            for l in litigations:
                db.session.execute(query, {
                    "agent_id": agent_id,
                    "case_no": l.get("caseNo"),
                    "tribunal_place": l.get("namePlace"),
                    "petitioner_name": l.get("petitioner"),
                    "respondent_name": l.get("respondent"),
                    "case_facts": l.get("facts"),
                    "present_status": l.get("presentStatus"),
                    "interim_order": l.get("interimOrder"),
                    "final_order": l.get("finalOrder"),

                    # must be JSON string or None
                    "interim_order_certificate": json.dumps(l.get("interim_order_certificate")) if l.get("interim_order_certificate") else None,
                    "disposed_certificate": json.dumps(l.get("disposed_certificate")) if l.get("disposed_certificate") else None,
                })

            db.session.commit()
            return {"success": True}

        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": str(e)}


  
    @staticmethod
    def insert_agent_other_state_rera(agent_id, other_rera_list):
        try:
            query = text("""
                INSERT INTO agent_other_state_rera_t
                (
                    agent_id,
                    registration_number,
                    state_id,
                    state_name,
                    district
                )
                VALUES
                (
                    :agent_id,
                    :registration_number,
                    :state_id,
                    :state_name,
                    :district
                )
            """)

            for r in other_rera_list:
                db.session.execute(query, {
                    "agent_id": agent_id,
                    "registration_number": r.get("regNo"),
                    "state_id": r.get("stateId"),
                    "state_name": r.get("stateName"),
                    "district": r.get("districtName")   # or r.get("district")
                })

            db.session.commit()
            return {"success": True}

        except Exception as e:
            return {"success": False, "message": str(e)}



    # ================= STEP 2 =================
    @staticmethod
    def update_itr_documents(agent_id, itr_year1, itr_year2, itr_year3):
        try:
            query = text("""
                UPDATE agentregistration_details_t
                SET
                    itr_year1 = CAST(:itr_year1 AS jsonb),
                    itr_year2 = CAST(:itr_year2 AS jsonb),
                    itr_year3 = CAST(:itr_year3 AS jsonb)
                WHERE id = :agent_id
            """)

            db.session.execute(query, {
                "agent_id": agent_id,
                "itr_year1": json.dumps(itr_year1),
                "itr_year2": json.dumps(itr_year2),
                "itr_year3": json.dumps(itr_year3),
            })

            db.session.commit()
            return {"success": True}

        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": str(e)}

    # ================= PREVIEW =================
    @staticmethod
    def get_agent_preview(agent_id):
        try:
            query = text("""
                SELECT
                    a.agent_type,
                    a.id AS agent_id,
                    a.agent_name,
                    a.father_name,
                    a.occupation_id,
                    o.occupation_name,
                    a.email,
                    a.aadhaar,
                    a.pan,
                    a.mobile,
                    a.landline,
                    a.license_number,
                    a.license_date,


                    a.address1,
                    a.address2,
                    a.pincode,

                    a.state_id,
                    sm.state_name AS state_name,

                    a.district,
                    dm.district_name AS district_name,

                    a.mandal,
                    mm.mandal_name AS mandal_name,

                    a.village,
                    vm.village_name AS village_name,

                    a.photograph,
                    a.pan_proof,
                    a.address_proof,
                    a.self_declared_affidavit,

                    a.itr_year1,
                    a.itr_year2,
                    a.itr_year3,

                    a.last_five_years_project_details,
                    a.any_civil_criminal_cases,
                    a.registration_other_states

                FROM agentregistration_details_t a

                LEFT JOIN occupation_master_t o
                    ON a.occupation_id = o.occupation_id
                LEFT JOIN state_master_t sm 
                    ON a.state_id::integer = sm.id
                LEFT JOIN districts_t dm 
                    ON a.district::integer = dm.id
                LEFT JOIN mandals_t mm 
                    ON a.mandal::integer = mm.id
                LEFT JOIN villages_t vm 
                    ON a.village::integer = vm.id

                WHERE a.id = :agent_id
            """)

            agent_row = db.session.execute(query, {"agent_id": agent_id}).mappings().first()

            if not agent_row:
                return {"success": False, "message": "Agent not found"}

            # ---------------- PROJECTS ----------------
            project_query = text("""
                SELECT id, project_name
                FROM agent_projects_t
                WHERE agent_id = :agent_id
                ORDER BY id
            """)

            projects = db.session.execute(project_query, {"agent_id": agent_id}).mappings().all()

            # ---------------- LITIGATIONS ----------------
            litigation_query = text("""
                SELECT
                    id,
                    case_no,
                    tribunal_place,
                    petitioner_name,
                    respondent_name,
                    case_facts,
                    present_status,
                    interim_order,
                    final_order,
                    interim_order_certificate,
                    disposed_certificate
                FROM agent_litigations_t
                WHERE agent_id = :agent_id
                ORDER BY id
            """)

            litigations = db.session.execute(litigation_query, {"agent_id": agent_id}).mappings().all()

            # ---------------- OTHER STATE RERA ----------------
            other_state_query = text("""
                SELECT
                    id,
                    registration_number,
                    state_id,
                    state_name,
                    district
                FROM agent_other_state_rera_t
                WHERE agent_id = :agent_id
                ORDER BY id
            """)

            other_states = db.session.execute(other_state_query, {"agent_id": agent_id}).mappings().all()

            # ---------------- FINAL RESPONSE ----------------
            return {
                "success": True,
                "data": {
                    "agent_details": dict(agent_row),
                    "projects": [dict(p) for p in projects],
                    "litigations": [dict(l) for l in litigations],
                    "other_state_rera": [dict(o) for o in other_states]
                }
            }

        except Exception as e:
            return {"success": False, "message": str(e)}


    
    @staticmethod
    def get_agent_by_pan(pan):
        try:
            query = text("""
                SELECT id
                FROM agentregistration_details_t
                WHERE UPPER(pan) = :pan
                LIMIT 1
            """)

            row = db.session.execute(
                query, {"pan": pan}
            ).fetchone()

            if row:
                return {
                    "success": True,
                    "exists": True
                }

            return {
                "success": True,
                "exists": False
            }

        except Exception as e:
            return {
                "success": False,
            "message": str(e)
        }

    @staticmethod
    def send_otp(agent_id):
        try:
            query = text("""
                SELECT email
                FROM agentregistration_details_t
                WHERE id = :agent_id
            """)

            row = db.session.execute(query, {"agent_id": agent_id}).fetchone()

            if not row:
                return {"success": False, "message": "Agent not found"}

            email = row.email

            otp = str(random.randint(100000, 999999))

            # delete old otp
            db.session.execute(text("""
                DELETE FROM agent_otp_t WHERE agent_id = :agent_id
            """), {"agent_id": agent_id})

            # insert otp
            db.session.execute(text("""
                INSERT INTO agent_otp_t (agent_id, otp, created_at)
                VALUES (:agent_id, :otp, NOW())
            """), {"agent_id": agent_id, "otp": otp})

            db.session.commit()

            # ✅ HERE YOU MUST KEEP THIS LINE
            send_email_otp(email, otp)

            return {"success": True, "message": "OTP sent to registered email"}

        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": str(e)}

    
    @staticmethod
    def verify_otp(agent_id, otp):
        try:
            query = text("""
                SELECT a.application_no, a.agent_name
                FROM agent_otp_t o
                JOIN agentregistration_details_t a
                ON a.id = o.agent_id
                WHERE o.agent_id = :agent_id
                AND o.otp = :otp
                AND o.created_at >= NOW() - INTERVAL '5 minutes'
                LIMIT 1
            """)

            row = db.session.execute(query, {
                "agent_id": agent_id,
                "otp": otp
            }).fetchone()

            if not row:
                return {
                    "success": False,
                    "message": "Invalid or expired OTP"
                }

            return {
                "success": True,
                "application_no": row.application_no,
                "agent_name": row.agent_name
            }

        except Exception as e:
            return {"success": False, "message": str(e)}

    @staticmethod
    def create_payment(agent_id):
        try:
            transaction_id = "TXN" + str(random.randint(100000000, 999999999))

            query = text("""
                INSERT INTO agent_payment_t
                (
                    agent_id,
                    application_no,
                    transaction_id,
                    amount,
                    payment_for,
                    mobile,
                    status,
                    created_at
                )
                SELECT
                    id,
                    application_no,
                    :transaction_id,
                    10000,
                    'Agent Registration Fee',
                    mobile,
                    'PENDING',
                    NOW()
                FROM agentregistration_details_t
                WHERE id = :agent_id
                RETURNING id, application_no
            """)

            row = db.session.execute(query, {
                "agent_id": agent_id,
                "transaction_id": transaction_id
            }).fetchone()

            db.session.commit()

            return {
                "success": True,
                "payment_id": row.id,
                "application_no": row.application_no,
                "transaction_id": transaction_id
            }

        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": str(e)}

    
        # ================= EMAIL OTP =================
    @staticmethod
    def send_otp_email(pan):
        try:
            # 1️⃣ Check PAN & get email
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
                return {
                    "success": False,
                    "message": "PAN number not registered"
                }

            agent_id = row.id
            email = row.email

            if not email:
                return {
                    "success": False,
                    "message": "Email not available for this PAN"
                }

            # 2️⃣ Generate OTP
            otp = str(random.randint(100000, 999999))
            expiry = datetime.utcnow() + timedelta(minutes=5)

            # 3️⃣ Delete previous OTP
            db.session.execute(
                text("DELETE FROM agent_otp_t WHERE agent_id = :id"),
                {"id": agent_id}
            )

            # 4️⃣ Insert new OTP
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

            # 5️⃣ Send email
            from app.utils.mail_service import send_email

            email_body = f"""
Dear Applicant,

Your OTP for Agent Registration verification is:

{otp}

This OTP is valid for 5 minutes.

Regards,
AP RERA
"""

            send_email(
                to_email=email,
                subject="AP RERA OTP Verification",
                body=email_body
            )

            return {
                "success": True,
                "message": "OTP sent to registered email"
            }

        except Exception as e:
            db.session.rollback()
            return {
                "success": False,
                "message": str(e)
            }
    # ===============================
    # PARTIAL APPLICATIONS
    # ===============================
    @staticmethod
    def get_partial_applications(pan):
        query = text("""
            SELECT
                id AS agent_id,
                application_no,
                agent_name,
                'Individual' AS name_type,
                'Yet To Pay Reg Fee' AS status
            FROM agentregistration_details_t
            WHERE UPPER(pan) = :pan
        """)

        rows = db.session.execute(query, {"pan": pan}).fetchall()

        return [dict(r._mapping) for r in rows]
    
    @staticmethod
    def send_otp_email_by_agent_id(agent_id):
        try:
            query = text("""
                SELECT email
                FROM agentregistration_details_t
                WHERE id = :agent_id
            """)

            row = db.session.execute(query, {"agent_id": agent_id}).fetchone()

            if not row:
                return {"success": False, "message": "Agent not found"}

            email = row.email
            if not email:
                return {"success": False, "message": "Email not available"}

            otp = str(random.randint(100000, 999999))

            # delete old otp
            db.session.execute(
                text("DELETE FROM agent_otp_t WHERE agent_id = :agent_id"),
                {"agent_id": agent_id}
            )

            # insert new otp
            db.session.execute(text("""
                INSERT INTO agent_otp_t (agent_id, otp, email, created_at)
                VALUES (:agent_id, :otp, :email, NOW())
            """), {
                "agent_id": agent_id,
                "otp": otp,
                "email": email
            })

            db.session.commit()

            # send email using your existing email function
            from app.controllers.otp_controller import send_email_otp   # use correct import

            send_email_otp(email, otp)

            return {"success": True, "message": "OTP sent to registered email"}

        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": str(e)}
        
@staticmethod
def approve_agent_renewal(agent_id):
    try:

        query = text("""
            UPDATE agentregistration_details_t
            SET license_date = NOW() + INTERVAL '5 years'
            WHERE id = :agent_id
            RETURNING agent_name, application_no, license_date
        """)

        row = db.session.execute(query, {
            "agent_id": agent_id
        }).fetchone()

        db.session.commit()

        if not row:
            return {
                "success": False,
                "message": "Agent not found"
            }

        return {
            "success": True,
            "agent_name": row.agent_name,
            "application_no": row.application_no,
            "expiry_date": row.license_date
        }

    except Exception as e:
        db.session.rollback()
        return {
            "success": False,
            "message": str(e)
        }