from app import db
from datetime import datetime


class AuditLog(db.Model):

    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)

    application_number = db.Column(db.String(100))
    action = db.Column(db.String(100))

    ip_address = db.Column(db.String(50))

    user_agent = db.Column(db.Text)

    endpoint = db.Column(db.String(255))
    method = db.Column(db.String(10))

    status_code = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)