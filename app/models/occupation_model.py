from app.models.database import db

class Occupation(db.Model):
    __tablename__ = "occupation_master_t"

    occupation_id = db.Column(db.Integer, primary_key=True)
    occupation_name = db.Column(db.String(100), nullable=False)

    @staticmethod
    def get_all():
        return Occupation.query.all()