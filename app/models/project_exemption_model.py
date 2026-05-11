from app import db
from datetime import datetime

class ProjectExemption(db.Model):
    __tablename__ = "project_exemption"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150))
    mobile_no = db.Column(db.String(15))
    email = db.Column(db.String(150))
    address = db.Column(db.Text)
    ba_number = db.Column(db.String(50))

    plan_proceedings_path = db.Column(db.Text)
    request_letter_path = db.Column(db.Text)
    land_document_path = db.Column(db.Text)
    advocate_document_path = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    approver_status = db.Column(db.String(20), default="pending")

    remark_s1 = db.Column(db.Text)
    remark_s2 = db.Column(db.Text)

    s1_authority_id = db.Column(db.Integer)
    s2_authority_id = db.Column(db.Integer)

    certificate_path = db.Column(db.Text)

    s1_authority_checked_date = db.Column(db.DateTime)
    s2_authority_checked_date = db.Column(db.DateTime)