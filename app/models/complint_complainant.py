from app.models.database import db

class ComplintComplainant(db.Model):
    __tablename__ = "complainants"

    complainant_id = db.Column(db.Integer, primary_key=True)

    # ⭐ NEW RERA FIELDS
    is_rera_registered = db.Column(db.Boolean, default=False)
    registration_id = db.Column(db.String(50))


    complainant_registered_id = db.Column(db.String(50))
    complainant_type = db.Column(db.String(50), nullable=False)

    name = db.Column(db.String(150), nullable=False)
    mobile_no = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(150))

    address_line1 = db.Column(db.Text)
    address_line2 = db.Column(db.Text)
    state = db.Column(db.String(50))
    district = db.Column(db.String(50))
    pincode = db.Column(db.String(10))

    created_at = db.Column(db.DateTime, server_default=db.func.now())