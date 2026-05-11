from app.models.database import db
from datetime import datetime


class AgentRenewal(db.Model):
    __tablename__ = "agent_renewal_t"

    id = db.Column(db.Integer, primary_key=True)

    agent_id = db.Column(db.BigInteger, nullable=False)

    renewal_application_no = db.Column(db.String(50))

    expiry_date = db.Column(db.Date)

    fee_type = db.Column(db.String(50))

    renewal_status = db.Column(db.String(30), default="DRAFT")

    payment_status = db.Column(db.String(30), default="PENDING")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    email = db.Column(db.String(150))

    submitted_at = db.Column(db.DateTime)