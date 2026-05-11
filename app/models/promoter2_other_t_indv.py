from app import db

class Promoter2OtherTINDV(db.Model):
    __tablename__ = "promoter2_other_t_indv"

    id = db.Column(db.Integer, primary_key=True)
    application_no = db.Column(
        db.String(50),
        db.ForeignKey("promoter_profile_other_t_indv.application_no", ondelete="CASCADE")
    )

    is_organization = db.Column(db.String(10))
    is_indian = db.Column(db.String(20))

    name = db.Column(db.String(200))
    state = db.Column(db.String(100))
    district = db.Column(db.String(100))

    address_line1 = db.Column(db.Text)
    address_line2 = db.Column(db.Text)
    pin_code = db.Column(db.String(10))

    mobile = db.Column(db.String(15))
    email = db.Column(db.String(100))

    pan_card = db.Column(db.String(20))
    aadhaar = db.Column(db.String(20))
    passport_no = db.Column(db.String(50))
    supporting_document_path = db.Column(db.Text)