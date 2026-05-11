from app import db
from datetime import datetime


class ProjectClosureNEW(db.Model):

    __tablename__ = "project_closures"

    id = db.Column(db.Integer, primary_key=True)

    application_number = db.Column(db.String(100), nullable=False)
    project_name = db.Column(db.String(255))
    promoter_name = db.Column(db.String(255))
    ip_address = db.Column(db.String(50))

    occupancy_certificate_doc = db.Column(db.Text)
    sale_deed_copies_doc = db.Column(db.Text)
    association_of_allottees_doc = db.Column(db.Text)
    common_areas_handover_doc = db.Column(db.Text)
    structural_liability_affidavit_doc = db.Column(db.Text)
    unsold_units_affidavit_doc = db.Column(db.Text)
    rera_bank_statement_doc = db.Column(db.Text)
    project_photos_doc = db.Column(db.Text)
    

    occupancy_certificate_status = db.Column(db.String(10))

    reason_for_closure = db.Column(db.Text)

    declaration_accepted = db.Column(db.Boolean)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)