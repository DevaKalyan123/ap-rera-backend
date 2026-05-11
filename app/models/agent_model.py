from app.models.database import db

class Agent(db.Model):
    __tablename__ = "agent_details"

    id = db.Column(db.Integer, primary_key=True)
    pan_number = db.Column(db.String(10), unique=True, nullable=False)
    mobile_number = db.Column(db.String(15))
    is_pan_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    @staticmethod
    def agent_details_application_no(application_no):
        try:
            query = text("""
                SELECT * FROM agentregistration_details_t WHERE application_no = :application_no
                LIMIT 1
            """)

            row = db.session.execute(
                query,
                {"application_no": application_no}
            ).mappings().first()

            if not row:
                return {
                    "success": False,
                    "message": "Application not found"
                }

            return {
                "success": True,
                "data": dict(row)
            }

        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }