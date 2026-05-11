from app.models.database import db

class ComplintRespondent(db.Model):
    __tablename__ = "respondents"

    respondent_id = db.Column(db.Integer, primary_key=True)

    registered_id = db.Column(db.String(50))
    respondent_type = db.Column(db.String(50), nullable=False)

     # ⭐ NEW RERA FIELDS
    is_rera_registered = db.Column(db.Boolean, default=False)
    registration_id = db.Column(db.String(50))

    name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(150))

    project_name = db.Column(db.String(200))

    address_line1 = db.Column(db.Text)
    address_line2 = db.Column(db.Text)
    state = db.Column(db.String(50))
    district = db.Column(db.String(50))
    pincode = db.Column(db.String(10))

    created_at = db.Column(db.DateTime, server_default=db.func.now())