from app import db

class PastProjectOtherTINDV(db.Model):
    __tablename__ = "past_projects_other_t_indv"

    id = db.Column(db.Integer, primary_key=True)
    application_no = db.Column(
        db.String(50),
        db.ForeignKey("promoter_profile_other_t_indv.application_no", ondelete="CASCADE")
    )

    project_name = db.Column(db.String(200))
    project_type = db.Column(db.String(100))
    current_status = db.Column(db.String(100))
    project_address = db.Column(db.Text)

    state = db.Column(db.String(100))
    district = db.Column(db.String(100))
    pin_code = db.Column(db.String(10))
    survey_no = db.Column(db.String(100))

    actual_completion_date = db.Column(db.Date)
    expected_completion_date = db.Column(db.Date)
