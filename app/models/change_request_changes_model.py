from app.models.database import db
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime


class ChangeRequestChange(db.Model):
    __tablename__ = "change_request_changes_t"

    id = db.Column(db.Integer, primary_key=True)

    request_id = db.Column(
        db.Integer,
        db.ForeignKey("project_change_requests_t.id", ondelete="CASCADE"),
        nullable=False
    )

    section = db.Column(db.String(100))
    subsection = db.Column(db.String(100))

    field_name = db.Column(db.String(200))

    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)

    data_json = db.Column(JSONB)

    description = db.Column(db.Text)

    proof_document_name = db.Column(db.String(255))

    old_file_path = db.Column(db.Text)
    new_file_path = db.Column(db.Text)

    change_mode = db.Column(db.String(10))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "request_id": self.request_id,
            "section": self.section,
            "subsection": self.subsection,
            "field_name": self.field_name,
            "old_value": self.old_value,
            "new_value": self.new_value,
            "data_json": self.data_json,
            "description": self.description,
            "proof_document_name": self.proof_document_name,
            "old_file_path": self.old_file_path,
            "new_file_path": self.new_file_path,
            "change_mode": self.change_mode,
            "created_at": self.created_at
        }