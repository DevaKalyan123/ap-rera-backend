from sqlalchemy import text
from app.models.database import db

def get_planning_documents(application_number, pan_number):

    query = text("""
        SELECT 
            m.doc_id,
            m.doc_name,
            d.value
        FROM 
            project_registration_documents prd,
            jsonb_each(prd.documents::jsonb) d(key, value)
        JOIN 
            project_registration_document_master m
            ON m.doc_id = d.key::int
        WHERE 
            prd.application_number = :application_number
            AND prd.pan_number = :pan_number
            AND m.doc_id IN (2,3,7,8,9,10,14,26)
    """)

    result = db.session.execute(query, {
        "application_number": application_number,
        "pan_number": pan_number
    }).fetchall()

    return [
        {
            "doc_id": row.doc_id,
            "doc_name": row.doc_name,
            "data": row.value
        }
        for row in result
    ]

def get_all_planning_dashboard():

    from sqlalchemy import text
    from app.models.database import db

    query = text("""
        SELECT 
            pr.application_number,
            pr.pan_number,
            pr.architect_certificate_path,
            pr.engineer_certificate_path,
            pr.ca_certificate_path,
            m.doc_id,
            m.doc_name,
            d.value
        FROM 
            project_registration pr
        LEFT JOIN 
            project_registration_documents prd
            ON pr.application_number = prd.application_number
            AND pr.pan_number = prd.pan_number
        LEFT JOIN 
            jsonb_each(prd.documents::jsonb) d(key, value)
            ON TRUE
        LEFT JOIN 
            project_registration_document_master m
            ON m.doc_id = d.key::int
        WHERE 
            m.doc_id IN (2,3,7,8,9,10,14,26)
    """)

    result = db.session.execute(query).fetchall()

    final = {}

    for row in result:
        key = f"{row.application_number}_{row.pan_number}"

        if key not in final:
            final[key] = {
                "application_number": row.application_number,
                "pan_number": row.pan_number,
                "certificates": {
                    "architect_certificate_path": row.architect_certificate_path,
                    "engineer_certificate_path": row.engineer_certificate_path,
                    "ca_certificate_path": row.ca_certificate_path,
                },
                "documents": []
            }

        final[key]["documents"].append({
            "doc_id": row.doc_id,
            "doc_name": row.doc_name,
            "data": row.value
        })

    return list(final.values())

def get_all_planning_dashboard_by_type(user_type):

    from sqlalchemy import text
    from app.models.database import db

    # 🔥 Decide table
    if user_type == "individual":
        table_name = "project_registration"
    else:
        table_name = "othertheninduvidual_project_registration"

    query = text(f"""
        SELECT 
            pr.application_number,
            pr.pan_number,
            pr.architect_certificate_path,
            pr.engineer_certificate_path,
            pr.ca_certificate_path,
            m.doc_id,
            m.doc_name,
            d.value
        FROM 
            {table_name} pr
        LEFT JOIN 
            project_registration_documents prd
            ON pr.application_number = prd.application_number
            AND pr.pan_number = prd.pan_number
        LEFT JOIN 
            jsonb_each(prd.documents::jsonb) d(key, value)
            ON TRUE
        LEFT JOIN 
            project_registration_document_master m
            ON m.doc_id = d.key::int
        WHERE 
            m.doc_id IN (2,3,7,8,9,10,14,26)
    """)

    result = db.session.execute(query).fetchall()

    final = {}

    for row in result:
        key = f"{row.application_number}_{row.pan_number}"

        if key not in final:
            final[key] = {
                "application_number": row.application_number,
                "pan_number": row.pan_number,
                "certificates": {
                    "architect_certificate_path": row.architect_certificate_path,
                    "engineer_certificate_path": row.engineer_certificate_path,
                    "ca_certificate_path": row.ca_certificate_path,
                },
                "documents": []
            }

        if row.doc_id:
            final[key]["documents"].append({
                "doc_id": row.doc_id,
                "doc_name": row.doc_name,
                "data": row.value
            })

    return list(final.values())

def get_all_planning_dashboard_mixed():

    from sqlalchemy import text
    from app.models.database import db

    query = text("""
        SELECT 
            pr.application_number,
            pr.pan_number,
            pr.architect_certificate_path,
            pr.engineer_certificate_path,
            pr.ca_certificate_path,
            'individual' AS type,
            m.doc_id,
            m.doc_name,
            d.value
        FROM project_registration pr
        LEFT JOIN project_registration_documents prd
            ON pr.application_number = prd.application_number
            AND pr.pan_number = prd.pan_number
        LEFT JOIN jsonb_each(prd.documents::jsonb) d(key, value)
            ON TRUE
        LEFT JOIN project_registration_document_master m
            ON m.doc_id = d.key::int
        WHERE m.doc_id IN (2,3,7,8,9,10,14,26)

        UNION ALL

        SELECT 
            pr.application_number,
            pr.pan_number,
            pr.architect_certificate_path,
            pr.engineer_certificate_path,
            pr.ca_certificate_path,
            'other' AS type,
            m.doc_id,
            m.doc_name,
            d.value
        FROM othertheninduvidual_project_registration pr
        LEFT JOIN project_registration_documents prd
            ON pr.application_number = prd.application_number
            AND pr.pan_number = prd.pan_number
        LEFT JOIN jsonb_each(prd.documents::jsonb) d(key, value)
            ON TRUE
        LEFT JOIN project_registration_document_master m
            ON m.doc_id = d.key::int
        WHERE m.doc_id IN (2,3,7,8,9,10,14,26)
    """)

    result = db.session.execute(query).fetchall()

    final = {}

    for row in result:
        key = f"{row.application_number}_{row.pan_number}_{row.type}"

        if key not in final:
            final[key] = {
                "application_number": row.application_number,
                "pan_number": row.pan_number,
                "type": row.type,   # 🔥 THIS IS IMPORTANT
                "certificates": {
                    "architect_certificate_path": row.architect_certificate_path,
                    "engineer_certificate_path": row.engineer_certificate_path,
                    "ca_certificate_path": row.ca_certificate_path,
                },
                "documents": []
            }

        if row.doc_id:
            final[key]["documents"].append({
                "doc_id": row.doc_id,
                "doc_name": row.doc_name,
                "data": row.value
            })

    return list(final.values())

def get_planning_single(application_number, pan_number):

    from sqlalchemy import text
    from app.models.database import db

    # 🔹 Step 1: Check individual table
    check = db.session.execute(text("""
        SELECT 1 FROM project_registration
        WHERE application_number = :application_number
        AND pan_number = :pan_number
    """), {
        "application_number": application_number,
        "pan_number": pan_number
    }).fetchone()

    # 🔹 Step 2: Decide table
    if check:
        table = "project_registration"
        user_type = "individual"
    else:
        table = "othertheninduvidual_project_registration"
        user_type = "other"

    # 🔹 Step 3: Fetch data
    rows = db.session.execute(text(f"""
        SELECT 
            pr.application_number,
            pr.pan_number,
            pr.architect_certificate_path,
            pr.engineer_certificate_path,
            pr.ca_certificate_path,
            m.doc_id,
            m.doc_name,
            d.value
        FROM {table} pr
        LEFT JOIN project_registration_documents prd
            ON pr.application_number = prd.application_number
            AND pr.pan_number = prd.pan_number
        LEFT JOIN jsonb_each(prd.documents::jsonb) d(key, value)
            ON TRUE
        LEFT JOIN project_registration_document_master m
            ON m.doc_id = d.key::int
        WHERE 
            pr.application_number = :application_number
            AND pr.pan_number = :pan_number
            AND m.doc_id IN (2,3,7,8,9,10,14,26)
    """), {
        "application_number": application_number,
        "pan_number": pan_number
    }).fetchall()

    if not rows:
        return {}

    first = rows[0]

    return {
        "application_number": first.application_number,
        "pan_number": first.pan_number,
        "type": user_type,
        "certificates": {
            "architect_certificate_path": first.architect_certificate_path,
            "engineer_certificate_path": first.engineer_certificate_path,
            "ca_certificate_path": first.ca_certificate_path,
        },
        "documents": [
            {
                "doc_id": r.doc_id,
                "doc_name": r.doc_name,
                "data": r.value
            }
            for r in rows if r.doc_id
        ]
    }