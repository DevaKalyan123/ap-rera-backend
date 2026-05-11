from app.models.database import db
from datetime import datetime


class AgentOtherThanIndividualLitigation(db.Model):
    __tablename__ = "agent_litigations_t"

    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(
        db.Integer, db.ForeignKey("agentregistration_details_t.id"), nullable=False
    )

    case_no = db.Column(db.String(150))
    tribunal_place = db.Column(db.String(255))
    petitioner_name = db.Column(db.String(255))
    respondent_name = db.Column(db.String(255))
    case_facts = db.Column(db.Text)

    present_status = db.Column(db.String(100))
    interim_order_certificate = db.Column(db.JSON)
    disposed_certificate = db.Column(db.JSON)
    self_declared_affidavit = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "case_no": self.case_no,
            "tribunal_name_place": self.tribunal_place,
            "petitioner_name": self.petitioner_name,
            "respondent_name": self.respondent_name,
            "case_facts": self.case_facts,
            "present_status": self.present_status,
            "interim_order": (
                self.interim_order_certificate.get("file")
                if isinstance(self.interim_order_certificate, dict)
                else self.interim_order_certificate
            ),
            "final_order_details": (
                self.disposed_certificate.get("file")
                if isinstance(self.disposed_certificate, dict)
                else self.disposed_certificate
            ),
            "self_declared_affidavit": self.self_declared_affidavit,
        }
