from app.models.database import db
from datetime import datetime


class AgentRenewalQuery(db.Model):

    __tablename__ = "agent_renewal_query_t"

    id = db.Column(db.Integer, primary_key=True)

    renewal_id = db.Column(db.Integer)

    query_text = db.Column(db.Text)

    raised_by = db.Column(db.String(20))

    response = db.Column(db.Text)

    status = db.Column(db.String(20), default="OPEN")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)