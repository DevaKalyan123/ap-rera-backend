from app.models.database import db
from sqlalchemy.sql import text


def insert_extension_project_application(data):
    query = text("""
        INSERT INTO extension_project_application_details (
            application_number,
            project_name,
            project_id,
            validity_from,
            validity_to,
            new_validity_from,
            new_validity_to,
            representation_letter,
            form_b,
            consent_letter,
            form_e,
            form_p4,
            extension_proceeding,
            status
        )
        VALUES (
            :application_number,
            :project_name,
            :project_id,
            :validity_from,
            :validity_to,
            :new_validity_from,
            :new_validity_to,
            :representation_letter,
            :form_b,
            :consent_letter,
            :form_e,
            :form_p4,
            :extension_proceeding,
            'SUBMITTED'
        )
    """)

    db.session.execute(query, {
        "application_number": data["application_number"],
        "project_name": data["project_name"],
        "project_id": data["project_id"],
        "validity_from": data["validity_from"],
        "validity_to": data["validity_to"],
        "new_validity_from": data["new_validity_from"],
        "new_validity_to": data["new_validity_to"],
        "representation_letter": data["representation_letter"],
        "form_b": data["form_b"],
        "consent_letter": data["consent_letter"],
        "form_e": data["form_e"],
        "form_p4": data["form_p4"],
        "extension_proceeding": data["extension_proceeding"],
    })

    db.session.commit()



    
def get_project_basic_details_by_pan(pan_number):
    query = text("""
        WITH all_promoters AS (
            SELECT 
                application_no as app_no, 
                pan_number, 
                name as promoter_name, 
                promoter_type,
                email  
            FROM project_registrations
            WHERE pan_number = :pan_number

            UNION

            SELECT 
                application_no as app_no, 
                pan_number, 
                organization_name as promoter_name, 
                promoter_type,
                authorized_signatory_email AS email  
            FROM promoter_profile_other_t_indv
            WHERE pan_number = :pan_number
        )
        SELECT 
            ap.app_no AS application_number,
            ap.promoter_name AS name,
            ap.promoter_type AS promoter_type,
            ap.email AS email,
            COALESCE(NULLIF(pr.project_name, ''), pn.project_name) AS project_name,
            pr.building_plan_no,
            pr.building_permission_from,
            pr.building_permission_upto
        FROM all_promoters ap
        LEFT JOIN project_registration pr 
            ON ap.app_no = pr.application_number
        LEFT JOIN project_registrations pn
            ON ap.app_no = pn.application_no
    """)

    result = db.session.execute(
        query,
        {"pan_number": pan_number}
    ).mappings().all()

    return [dict(r) for r in result]