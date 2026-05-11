from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.models.database import db


class QuarterlyDocument(db.Model):
    __tablename__ = "quarterly_documents"

    id = Column(Integer, primary_key=True, autoincrement=True)

    quarterly_id = Column(
        Integer,
        ForeignKey("quarterly_updates.id"),
        nullable=False
    )

    document_type = Column(String(200))
    file_path = Column(Text)