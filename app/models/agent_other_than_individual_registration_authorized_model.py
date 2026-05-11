from app.models.database import db
from datetime import datetime

class AgentOtherThanIndividualAuthorized(db.Model):
    __tablename__ = "agent_authorized_details_t"

    id = db.Column(db.Integer, primary_key=True)
    organisation_id = db.Column(
        db.Integer, db.ForeignKey("agentregistration_details_t.id"), nullable=False
    )

    name = db.Column(db.String(150), nullable=False)
    mobile_number = db.Column(db.String(15))
    email_id = db.Column(db.String(150))
    photo = db.Column(db.String(255))
    board_resolution = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "mobile_number": self.mobile_number,
            "email_id": self.email_id,
            "photo": self.photo,
            "board_resolution": self.board_resolution,
            "created_at": (
                self.created_at.strftime("%Y-%m-%d %H:%M:%S")
                if self.created_at
                else None
            ),
        }
