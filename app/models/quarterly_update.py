from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from app.models.database import db


class QuarterlyUpdate(db.Model):
    __tablename__ = "quarterly_updates"

    id = Column(Integer, primary_key=True, autoincrement=True)

    project_id = Column(
        Integer,
        ForeignKey("project_registrations.id"),
        nullable=False
    )

    quarter_id = Column(String(20), nullable=False)
    occupancy = Column(Boolean, default=False)
    status = Column(String(20), default="DRAFT")

    created_at = Column(DateTime, default=db.func.current_timestamp())