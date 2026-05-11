from app import db

class FilesOtherTINDV(db.Model):
    __tablename__ = "files_Other_t_INDV"

    id = db.Column(db.Integer, primary_key=True)

    application_no = db.Column(
        db.String(50),
        db.ForeignKey("promoter_profile_Other_t_INDV.application_no", ondelete="CASCADE")
    )

    file_category = db.Column(db.String(100))
    file_name = db.Column(db.String(255))
    file_path = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, server_default=db.func.now())
