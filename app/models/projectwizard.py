
from sqlalchemy import Column, Integer, String, Text, DateTime, Date
from app.models.database import db


class ProjectRegistration(db.Model):
    __tablename__ = 'project_registrations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Application
    application_no = Column(String(50), unique=True, nullable=False)
    promoter_type = Column(String(50), default='individual')
    pan_number = Column(String(10), nullable=False)

    # Bank Details
    bank_state = Column(String(100))
    bank_name = Column(String(200))
    branch_name = Column(String(200))
    account_no = Column(String(50))
    account_holder = Column(String(200))
    ifsc = Column(String(11))

    # Promoter Details
    name = Column(String(200), nullable=False)
    father_name = Column(String(200))
    aadhaar = Column(String(12))
    mobile = Column(String(10), nullable=False)
    landline = Column(String(15))
    email = Column(String(200), nullable=False)
    promoter_website = Column(String(500))
    state_ut = Column(String(100))
    district = Column(String(100))
    license_no = Column(String(100))
    license_date = Column(Date)
    gst_num = Column(String(15))

    # Other State Registration
    other_state_reg = Column(Text)
    rera_reg_number = Column(String(100))
    rera_state = Column(String(100))
    registration_revoked = Column(Text)

    # Projects Last 5 Years
    last_five_years = Column(Text)
    project_name = Column(String(500))
    project_type = Column(String(100))
    current_status = Column(String(100))
    project_address = Column(Text)
    project_state_ut = Column(String(100))
    project_district = Column(String(100))
    pin_code = Column(String(6))
    survey_no = Column(String(100))

    # Litigations
    litigation = Column(Text)
    case_no = Column(String(100))
    tribunal_place = Column(String(200))
    petitioner_name = Column(String(200))
    respondent_name = Column(String(200))
    case_facts = Column(Text)
    case_status = Column(String(100))
    interim_order = Column(Text)
    final_order_details = Column(Text)

    # Promoter 2
    promoter2 = Column(Text)
    promoter2_is_organization = Column(Text)
    promoter2_is_indian = Column(Text)
    promoter2_name = Column(String(200))
    promoter2_address_line1 = Column(String(500))
    promoter2_address_line2 = Column(String(500))
    promoter2_mobile = Column(String(10))
    promoter2_email = Column(String(200))
    promoter2_pan_card = Column(String(10))

    # =========================
    # FILE UPLOAD COLUMNS
    # =========================
    bank_statement_file = Column(Text)
    pan_file = Column(Text)
    aadhaar_file = Column(Text)
    photograph_file = Column(Text)
    license_certificate_file = Column(Text)
    gst_document_file = Column(Text)
    self_affidavit_file = Column(Text)
    promoter2_documents_file = Column(Text)
    itr_documents_file = Column(Text)
    balance_sheet_file = Column(Text)

    # Metadata
    created_at = Column(DateTime, default=db.func.current_timestamp())


class ProjectWizardModel:

    @staticmethod
    def create_table():
        db.create_all()

    @staticmethod
    def insert_project(data):
        registration = ProjectRegistration(**data)
        db.session.add(registration)
        db.session.commit()
        return registration

    @staticmethod
    def fetch_all():
        return ProjectRegistration.query.order_by(ProjectRegistration.id.desc()).all()

    @staticmethod
    def fetch_by_application_no(application_no):
        return ProjectRegistration.query.filter_by(application_no=application_no).first()