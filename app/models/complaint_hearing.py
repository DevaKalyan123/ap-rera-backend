from app.models.database import db


class ComplaintHearing(db.Model):
    __tablename__ = "complaint_hearings"
    hearing_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    complaint_id = db.Column(
        db.BigInteger,
        db.ForeignKey("complaints.complaint_id", ondelete="CASCADE"),
        nullable=False,
    )
    hearing_no = db.Column(db.Integer)
    hearing_date = db.Column(db.DateTime, nullable=False)
    next_hearing_date = db.Column(db.DateTime)
    hearing_place = db.Column(db.String(300))
    remarks = db.Column(db.Text)
    status = db.Column(db.String(20))
    documents = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, server_default=db.func.now())