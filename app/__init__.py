from flask_cors import CORS
from flask import Flask, send_from_directory, request
from app.config import Config
from app.models.database import db 
from app.utils.request_logger import log_request
from app.jobs.payment_reminder import start_scheduler

import logging
from logging.handlers import RotatingFileHandler
import os


# ---------------------------------------------------------
# Logging Setup
# ---------------------------------------------------------

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(LOG_DIR, "app.log")

handler = RotatingFileHandler(
    log_file,
    maxBytes=5_000_000,
    backupCount=5
)

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

handler.setFormatter(formatter)

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(handler)
root_logger.addHandler(logging.StreamHandler())

# reduce flask request noise
logging.getLogger("werkzeug").setLevel(logging.WARNING)


# ---------------------------------------------------------
# Create Flask App
# ---------------------------------------------------------

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)
    start_scheduler(app)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # uploads folder
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


    # ---------------------------------------------------------
    # CORS Configuration
    # ---------------------------------------------------------

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    CORS(app)

    @app.before_request
    def handle_options():
        if request.method == "OPTIONS":
            return "", 200

    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,PATCH,DELETE,OPTIONS"
        return response


    # ---------------------------------------------------------
    # Database Initialization
    # ---------------------------------------------------------

    db.init_app(app)


    # ---------------------------------------------------------
    # GLOBAL API AUDIT LOGGER (MIDDLEWARE)
    # ---------------------------------------------------------

    # app.after_request(log_request)


    # ---------------------------------------------------------
    # Serve Uploaded Files
    # ---------------------------------------------------------

    @app.route("/uploads/<path:filename>")
    def serve_uploaded_file(filename):
        # Check app/uploads first
        app_uploads = app.config["UPLOAD_FOLDER"]
        if os.path.exists(os.path.join(app_uploads, filename)):
            return send_from_directory(app_uploads, filename)
            
        # Check root uploads folder
        root_uploads = os.path.join(BASE_DIR, "..", "uploads")
        if os.path.exists(os.path.join(root_uploads, filename)):
            return send_from_directory(root_uploads, filename)
            
        return "File not found", 404


    # ---------------------------------------------------------
    # Register Blueprints
    # ---------------------------------------------------------

    from app.controllers.test_connection_controller import test_connection_bp
    from app.controllers.location_controller import location_bp
    from app.controllers.development_details_controller import development_details_bp
    from app.controllers.project_registration_controller import project_registration_bp
    from app.controllers.project_wizard_controller import project_wizard_bp
    from app.controllers.complint_controller import complint_bp
    from app.controllers.promoter_registration_controller import promoter_registration_bp
    from app.controllers.project_uploddocuments_controller import project_upload_documents_bp
    from app.controllers.occupation_controller import occupation_controller
    from app.controllers.agent_registration_controller import agent_bp
    from app.controllers.otp_controller import otp_bp
    from app.controllers.associate_controller import associate_bp
    from app.controllers.application_associate_controller import application_associate_bp
    from app.controllers.project_preview_controller import preview_bp
    from app.controllers.projectapplicationdetailsextension import projectapplicationdetailsextension_bp
    from app.controllers.login_controller import login_bp
    from app.controllers.agent_other_than_individual_registration_controller import agent_other_than_individual_registration_bp
    from app.controllers.othertheninduvidual_project_registration_controller import othertheninduvidual_project_registration_bp
    from app.controllers.othertheninduvidual_project_preview_controller import othertheninduvidual_project_preview_bp

    # other modules
    from app.controllers.rera_other_t_indv_controller import rera_other_t_indv_bp
    from app.controllers.past_project_other_t_indv_controller import past_project_other_t_indv_bp
    from app.controllers.litigation_other_t_indv_controller import litigation_other_t_indv_bp
    from app.controllers.promoter2_other_t_indv_controller import promoter2_other_t_indv_bp
    from app.controllers.files_other_t_indv_controller import files_other_t_indv_bp
    from app.controllers.promoter_other_t_indv_controller import promoter_other_t_indv_bp
    from app.controllers.org_member_other_t_indv_controller import org_member_other_t_indv_bp

    from app.controllers.quarterly_controller import quarterly_bp
    from app.controllers.project_quarterly_plot_controller import project_quarterly_plot_bp
    from app.controllers.change_request_controller import change_request_bp

    from app.controllers.project_closure_controller import project_closure_bp

    from app.controllers.agent_renewal_controller import agent_renewal_bp
    from app.controllers.admin_requests_controller import admin_requests_bp
    from app.controllers.admin_requests_controller2 import admin_renewal_bp
    from app.controllers.admin_controller import admin_bp
    from app.controllers.agent_change_request_controller import agent_change_request_bp
    from app.controllers.scrutiny_projectregistation_controller import scrutiny_bp
    from app.controllers.chat_controller import chat_bp
    from app.controllers.faq_controller import faq_bp
    from app.controllers.verification_controller import verification_bp
    from app.controllers.agent_scrutiny_controller import agent_scrutiny_bp
    from app.controllers.project_unregistered_controller import project_unregistered_bp 
    from app.controllers.project_exemption_controller import project_exemption_bp
    


    # ---------------------------------------------------------
    # Register API Routes
    # ---------------------------------------------------------

    app.register_blueprint(change_request_bp, url_prefix="/api")
    app.register_blueprint(quarterly_bp, url_prefix="/api")

    app.register_blueprint(promoter_other_t_indv_bp)
    app.register_blueprint(org_member_other_t_indv_bp)
    app.register_blueprint(rera_other_t_indv_bp)
    app.register_blueprint(past_project_other_t_indv_bp)
    app.register_blueprint(litigation_other_t_indv_bp)
    app.register_blueprint(promoter2_other_t_indv_bp)
    app.register_blueprint(files_other_t_indv_bp)

    app.register_blueprint(agent_other_than_individual_registration_bp, url_prefix="/api")
    app.register_blueprint(preview_bp, url_prefix="/api")
    app.register_blueprint(application_associate_bp, url_prefix="/api")
    app.register_blueprint(associate_bp, url_prefix="/api")
    app.register_blueprint(project_upload_documents_bp, url_prefix="/api")
    app.register_blueprint(project_wizard_bp, url_prefix="/api")
    app.register_blueprint(promoter_registration_bp, url_prefix="/api")
    app.register_blueprint(complint_bp, url_prefix="/api")
    app.register_blueprint(development_details_bp, url_prefix="/api")
    app.register_blueprint(test_connection_bp, url_prefix="/api")
    app.register_blueprint(location_bp, url_prefix="/api")
    app.register_blueprint(project_registration_bp, url_prefix="/api")
    app.register_blueprint(occupation_controller, url_prefix="/api")

    app.register_blueprint(agent_bp, url_prefix="/api/agent")
    app.register_blueprint(otp_bp, url_prefix="/api/otp")

    app.register_blueprint(projectapplicationdetailsextension_bp, url_prefix="/api")
    app.register_blueprint(login_bp, url_prefix="/api")
    app.register_blueprint(othertheninduvidual_project_registration_bp, url_prefix="/api")

    app.register_blueprint(othertheninduvidual_project_preview_bp, url_prefix="/api")

    app.register_blueprint(project_quarterly_plot_bp)

    app.register_blueprint(project_closure_bp, url_prefix="/api/project_closure")

    app.register_blueprint(agent_renewal_bp, url_prefix="/api/agent-renewal")
    app.register_blueprint(admin_renewal_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/api")
    app.register_blueprint(agent_change_request_bp, url_prefix="/api")
    app.register_blueprint(scrutiny_bp, url_prefix="/api")
    app.register_blueprint(chat_bp, url_prefix="/api")
    app.register_blueprint(faq_bp, url_prefix="/api")
    app.register_blueprint(verification_bp, url_prefix="/api")
    app.register_blueprint(project_unregistered_bp, url_prefix="/api")
    app.register_blueprint(project_exemption_bp, url_prefix="/project-exemption")
    app.register_blueprint(agent_scrutiny_bp)


    return app