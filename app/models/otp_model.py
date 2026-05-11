from app.models.database import db

class AgentOTP(db.Model):
    __tablename__ = "agent_otp"

    id = db.Column(db.Integer, primary_key=True)
    pan_number = db.Column(db.String(10), nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())