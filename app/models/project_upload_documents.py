from app.models.database import db
from datetime import datetime
from sqlalchemy.ext.mutable import MutableDict  # 🔥 ADD THIS

class ProjectRegistrationDocument(db.Model):
    __tablename__ = "project_registration_documents"

    application_number = db.Column(db.String(50), primary_key=True)
    pan_number = db.Column(db.String(20), primary_key=True)

    # 🔥 CHANGE THIS LINE
    documents = db.Column(MutableDict.as_mutable(db.JSON), nullable=True)

    uploaded_on = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "application_number": self.application_number,
            "pan_number": self.pan_number,
            "documents": self.documents or {},
            "uploaded_on": self.uploaded_on
        }