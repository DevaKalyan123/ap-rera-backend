from sqlalchemy import Column, Integer, String, Text, DateTime
from app.models.database import db


class ChangeRequest(db.Model):
    __tablename__ = "change_requests"

    id = Column(Integer, primary_key=True)
    application_no = Column(String(50), nullable=False)
    change_type = Column(String(200), nullable=False)
    description = Column(Text)
    document = Column(Text)
    status = Column(String(50), default="Pending")
    reject_reason = Column(Text)
    created_at = Column(DateTime, default=db.func.current_timestamp())