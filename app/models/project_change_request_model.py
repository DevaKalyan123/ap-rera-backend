from app.models.database import db
from datetime import datetime


class ProjectChangeRequest(db.Model):
    __tablename__ = "project_change_requests_t"

    id = db.Column(db.Integer, primary_key=True)

    reference_no = db.Column(db.String(30), unique=True)
    application_number = db.Column(db.String(50))
    pan_number = db.Column(db.String(20))

    project_name = db.Column(db.String(200))
    applicant_name = db.Column(db.String(200))

    status = db.Column(db.String(30), default="SUBMITTED")

    payment_gateway = db.Column(db.String(50))
    payment_transaction_id = db.Column(db.String(100))
    payment_status = db.Column(db.String(30), default="PENDING")

    amount = db.Column(db.Numeric(10, 2), default=5000)
    payment_date = db.Column(db.DateTime)

    remarks = db.Column(db.Text)
    regected_reson = db.Column(db.Text)
    email = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

    # Relationship
    changes = db.relationship(
        "ChangeRequestChange",
        backref="change_request",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "reference_no": self.reference_no,
            "application_number": self.application_number,
            "pan_number": self.pan_number,
            "project_name": self.project_name,
            "applicant_name": self.applicant_name,
            "status": self.status,
            "payment_gateway": self.payment_gateway,
            "payment_transaction_id": self.payment_transaction_id,
            "payment_status": self.payment_status,
            "amount": float(self.amount) if self.amount else None,
            "payment_date": self.payment_date,
            "remarks": self.remarks,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "email": self.email,
            "rejected_reason": self.regected_reson,
        }