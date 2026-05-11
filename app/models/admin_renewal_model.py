from app.models.database import db
from sqlalchemy import text


# ===============================
# Dashboard Counts
# ===============================
def get_renewal_dashboard_counts():

    query = text("""
        SELECT
            COUNT(*) AS total,
            COUNT(*) FILTER (WHERE renewal_status='DRAFT') AS draft,
            COUNT(*) FILTER (WHERE renewal_status='APPROVED') AS approved,
            COUNT(*) FILTER (WHERE renewal_status='REJECTED') AS rejected,
            COUNT(*) FILTER (WHERE renewal_status='EXPIRED') AS expired
        FROM agent_renewal_t
    """)

    result = db.session.execute(query).fetchone()

    return {
        "total": result.total,
        "draft": result.draft,
        "approved": result.approved,
        "rejected": result.rejected,
        "expired": result.expired
    }


# ===============================
# Get Renewals By Status
# ===============================
def get_renewals_by_status(status):

    query = text("""
        SELECT
            id,
            agent_id,
            renewal_application_no,
            expiry_date,
            renewal_status,
            payment_status
        FROM agent_renewal_t
        WHERE renewal_status = :status
        ORDER BY id DESC
    """)

    rows = db.session.execute(query, {"status": status}).fetchall()

    renewals = []

    for r in rows:
        renewals.append({
            "id": r.id,
            "agent_id": r.agent_id,
            "application_no": r.renewal_application_no,
            "expiry_date": str(r.expiry_date),
            "renewal_status": r.renewal_status,
            "payment_status": r.payment_status
        })

    return renewals


# ===============================
# Renewal Detail (JOIN documents)
# ===============================
def get_renewal_detail(renewal_id):

    query = text("""
        SELECT
            r.id,
            r.agent_id,
            r.renewal_application_no,
            r.expiry_date,
            r.fee_type,
            r.renewal_status,
            r.payment_status,
            r.remarks,

            d.passport_photo,
            d.aadhaar_card,
            d.pan_card,
            d.address_proof,
            d.previous_rera_certificate

        FROM agent_renewal_t r
        LEFT JOIN agent_renewal_documents_t d
        ON r.agent_id= d.renewal_id

        WHERE r.id = :renewal_id
    """)

    row = db.session.execute(query, {"renewal_id": renewal_id}).fetchone()

    if not row:
        return None

    return {
        "id": row.id,
        "agent_id": row.agent_id,
        "application_no": row.renewal_application_no,
        "expiry_date": str(row.expiry_date),
        "fee_type": row.fee_type,
        "renewal_status": row.renewal_status,
        "payment_status": row.payment_status,
        "remarks": row.remarks,
        "documents": {
            "passport_photo": row.passport_photo,
            "aadhaar_card": row.aadhaar_card,
            "pan_card": row.pan_card,
            "address_proof": row.address_proof,
            "previous_rera_certificate": row.previous_rera_certificate
        }
    }


# ===============================
# Update Renewal Status
# ===============================
def update_renewal_status(renewal_id, status, remarks):

    query = text("""
        UPDATE agent_renewal_t
        SET renewal_status = :status,
            remarks = :remarks
        WHERE id = :renewal_id
    """)

    db.session.execute(query, {
        "status": status,
        "remarks": remarks,
        "renewal_id": renewal_id
    })

    db.session.commit()
def get_all_projects():
    query = text("""
        SELECT 
            id,
            application_no,
            promoter_type,
            pan_number,
            bank_name,
            status
        FROM project_registrations
        ORDER BY id DESC
    """)
    
    return db.session.execute(query).mappings().all()