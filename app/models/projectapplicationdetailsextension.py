# from app.models.database import db
# from sqlalchemy import text

# def get_project_basic_details_by_application_no(application_number):
#     query = text("""
#         SELECT
#             preg.application_no        AS application_number,
#             preg.project_name                  AS project_name,

#             dd.project_id              AS project_id,

#             pr.building_permission_from,
#             pr.building_permission_upto

#         FROM project_registrations preg

#         LEFT JOIN project_registration pr
#                ON preg.application_no = pr.application_number

#         LEFT JOIN development_details dd
#                ON preg.application_no = dd.application_number

#         WHERE preg.application_no = :application_number
#         LIMIT 1
#     """)

#     result = db.session.execute(
#         query,
#         {"application_number": application_number}
#     ).mappings().first()

#     return dict(result) if result else None
from app.models.database import db
from sqlalchemy import text

def get_project_basic_details_by_application_no1(application_number):
    query = text("""
        SELECT
            preg.application_no AS application_number,
            preg.project_name   AS project_name,
            dd.project_id       AS project_id,
            pr.building_permission_from,
            pr.building_permission_upto
        FROM project_registrations preg
        LEFT JOIN project_registration pr
               ON preg.application_no = pr.application_number
        LEFT JOIN development_details dd
               ON preg.application_no = dd.application_number
        WHERE preg.application_no = :application_number
        LIMIT 1
    """)

    result = db.session.execute(
        query, {"application_number": application_number}
    ).mappings().first()

    return dict(result) if result else None
