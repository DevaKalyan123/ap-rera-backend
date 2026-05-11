# app/models/login_model.py
from app.models.database import db
from sqlalchemy import text

def get_emails_by_pan(pan_number):
    pan = pan_number.strip().upper()

    query = text("""
        SELECT DISTINCT email FROM project_registrations
        WHERE UPPER(TRIM(pan_number)) = :pan

        UNION

        SELECT DISTINCT authorized_signatory_email
        FROM promoter_profile_other_t_indv
        WHERE UPPER(TRIM(pan_number)) = :pan
    """)

    result = db.session.execute(query, {"pan": pan}).fetchall()

    emails = [row[0] for row in result]

    return emails

def get_projects_by_pan(pan_number):
    query = text("""
        SELECT
            pr.application_number,
            preg.name AS promoter_name,
            preg.mobile AS promoter_mobile,
            pr.building_plan_no AS ba_no,
            pr.project_name AS project_name,
            pr.project_address1 AS project_address1,
            pr.project_district AS project_district,
            pr.project_mandal AS project_mandal,
            pr.project_village AS project_village,
            pr.project_pincode AS project_pincode,
            pr.building_permission_from AS validity_from,
            pr.building_permission_upto AS validity_to
        FROM project_registration pr
        JOIN project_registrations preg
          ON pr.application_number = preg.application_no
         AND pr.pan_number = preg.pan_number
        WHERE pr.pan_number = :pan
        ORDER BY pr.application_number
    """)
    result = db.session.execute(query, {"pan": pan_number}).mappings().all()
    return [dict(row) for row in result]