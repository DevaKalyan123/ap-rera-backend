from app import db

class OrgMemberOtherTINDV(db.Model):
    __tablename__ = "org_members_other_t_indv"

    id = db.Column(db.Integer, primary_key=True)
    application_no = db.Column(
        db.String(50),
        db.ForeignKey("promoter_profile_other_t_indv.application_no", ondelete="CASCADE")
    )

    is_indian = db.Column(db.String(20))
    name = db.Column(db.String(200))
    designation = db.Column(db.String(100))
    mobile = db.Column(db.String(15))
    email = db.Column(db.String(100))

    address_line1 = db.Column(db.Text)
    address_line2 = db.Column(db.Text)
    state = db.Column(db.String(100))
    district = db.Column(db.String(100))
    pin_code = db.Column(db.String(10))

    aadhaar = db.Column(db.String(20))
    pan = db.Column(db.String(20))
    din = db.Column(db.String(20))
