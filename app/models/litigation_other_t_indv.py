from app import db

class LitigationOtherTINDV(db.Model):
    __tablename__ = "litigations_other_t_indv"

    id = db.Column(db.Integer, primary_key=True)
    application_no = db.Column(
        db.String(50),
        db.ForeignKey("promoter_profile_other_t_indv.application_no", ondelete="CASCADE")
    )

    case_no = db.Column(db.String(150))
    tribunal_place = db.Column(db.Text)
    petitioner_name = db.Column(db.Text)
    respondent_name = db.Column(db.Text)
    case_facts = db.Column(db.Text)
    case_status = db.Column(db.String(100))

    interim_order = db.Column(db.String(10))
    final_order_details = db.Column(db.String(10))
    interim_order_certificate_path = db.Column(db.Text)
    disposed_certificate_path = db.Column(db.Text)