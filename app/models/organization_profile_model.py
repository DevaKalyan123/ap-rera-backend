from sqlalchemy import text
from app import db

def get_org_profile(application_no):
    print("🔥 DB FETCH application_no:", application_no)

    row = db.session.execute(text("""
        SELECT *
        FROM promoter_profile_Other_t_INDV
        WHERE application_no = :app
    """), {"app": application_no}).mappings().fetchone()

    print("🔥 ORG PROFILE ROW:", row)

    return dict(row) if row else {}


def get_org_rera_details(application_no):
    rows = db.session.execute(text("""
        SELECT *
        FROM rera_details_Other_t_INDV
        WHERE application_no = :app
    """), {"app": application_no}).mappings().fetchall()

    return [dict(r) for r in rows] if rows else []

def get_litigations(application_no):
    rows = db.session.execute(text("""
        SELECT *
        FROM litigations_other_t_indv
        WHERE application_no = :app
    """), {"app": application_no}).mappings().fetchall()
    return [dict(r) for r in rows] if rows else []

def get_promoter2(application_no):
    rows = db.session.execute(text("""
        SELECT *
        FROM promoter2_other_t_indv
        WHERE application_no = :app
    """), {"app": application_no}).mappings().fetchall()
    return [dict(r) for r in rows] if rows else []


def get_org_members(application_no):
    rows = db.session.execute(text("""
        SELECT *
        FROM org_members_Other_t_INDV
        WHERE application_no = :app
    """), {"app": application_no}).mappings().fetchall()

    return [dict(r) for r in rows] if rows else []

def get_past_projects(application_no):
    rows = db.session.execute(text("""
        SELECT *
        FROM past_projects_Other_t_INDV
        WHERE application_no = :app
    """), {"app": application_no}).mappings().fetchall()

    return [dict(r) for r in rows] if rows else []