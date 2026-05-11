from app.models.database import db


class ComplintComplaint(db.Model):
    __tablename__ = "complaints"

    complaint_id = db.Column(db.BigInteger, primary_key=True)

    complainant_id = db.Column(
        db.Integer, db.ForeignKey("complainants.complainant_id"), nullable=False
    )
    respondent_id = db.Column(
        db.Integer, db.ForeignKey("respondents.respondent_id"), nullable=False
    )

    subject = db.Column(db.String(255), nullable=False)
    relief_sought = db.Column(db.Text, nullable=False)
    complaint_regarding = db.Column(db.String(100))
    application_type = db.Column(db.String(10))
    status = db.Column(db.String(15), default="open")
    reject_reson = db.Column(db.Text)
    description = db.Column(db.Text, nullable=False)
    complaint_facts = db.Column(db.JSON)
    complaint_documents = db.Column(db.JSON)
    complaint_register_no = db.Column(db.String(100))
    supporting_documents = db.Column(db.JSON)
    project_details = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, server_default=db.func.now())