from datetime import datetime
from app.models.agent_renewal_model import AgentRenewal
from app.models.database import db


def generate_renewal_application_number():

    year = datetime.now().year

    count = db.session.query(AgentRenewal).count() + 1

    return f"APRERA-REN-{year}-{str(count).zfill(5)}"