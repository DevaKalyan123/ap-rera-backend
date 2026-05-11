from app import db

class ReraOtherTINDV(db.Model):
    __tablename__ = "rera_details_other_t_indv"

    id = db.Column(db.Integer, primary_key=True)
    application_no = db.Column(
        db.String(50),
        db.ForeignKey("promoter_profile_other_t_indv.application_no", ondelete="CASCADE")
    )

    rera_reg_number = db.Column(db.String(150))
    rera_state = db.Column(db.String(100))
    registration_revoked = db.Column(db.String(10))
    revocation_reason = db.Column(db.Text)
