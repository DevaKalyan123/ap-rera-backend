from app.models.database import db
from datetime import datetime
from sqlalchemy import text  # ✅ MOVE HERE


class PromoterRegistration(db.Model):
    __tablename__ = "promoter_registration"

    promoter_id = db.Column(db.Integer, primary_key=True)

    pan_number = db.Column(db.String(10), unique=True, nullable=False)
    user_type = db.Column(db.String(50), nullable=False)
    select_category = db.Column(db.String(50), nullable=False)

    name_applicant = db.Column(db.String(150), nullable=False)
    father_name = db.Column(db.String(150))

    mobile_number = db.Column(db.String(15), nullable=False)
    email_id = db.Column(db.String(150), nullable=False)

    state = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)

    upload_document = db.Column(db.String(255), nullable=False)

    name_organisation = db.Column(db.String(200))
    type_of_promoter = db.Column(db.String(100))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ METHOD
    @staticmethod
    def is_promoter_exists(promoter_register_id):
        try:
            query = text(
                """
                SELECT 1
                FROM promoter_registration
                WHERE promoter_register_id = :id
                LIMIT 1
            """
            )

            result = db.session.execute(
                query, {"id": str(promoter_register_id).strip()}
            ).fetchone()

            return True if result else False

        except Exception as e:
            print("ERROR:", e)
            return False