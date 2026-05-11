from flask import Blueprint, request, jsonify, send_from_directory
from app.models.database import db
from app.models.agent_other_than_individual_registration_organisation_model import (
    AgentOtherThanIndividualOrganisation,
)
from app.models.agent_other_than_individual_registration_entity_model import (
    AgentOtherThanIndividualEntity,
)
from app.models.agent_other_than_individual_registration_authorized_model import (
    AgentOtherThanIndividualAuthorized,
)
from app.models.agent_other_than_individual_registration_litigation_model import (
    AgentOtherThanIndividualLitigation,
)

import os
import json
import logging
from werkzeug.utils import secure_filename
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "agent_doc")
LOG_FILE = os.path.join(BASE_DIR, "logs", "agent_registration.log")

os.makedirs(UPLOAD_DIR, exist_ok=True)

logger = logging.getLogger("agent_registration")
logger.setLevel(logging.INFO)

if not logger.handlers:
    fh = logging.FileHandler(LOG_FILE)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(fh)

agent_other_than_individual_registration_bp = Blueprint(
    "agent_other_than_individual_registration_bp", __name__
)


def save_file(file_obj, prefix):
    if not file_obj:
        return None
    filename = secure_filename(file_obj.filename)
    final_name = f"{prefix}_{filename}"
    file_obj.save(os.path.join(UPLOAD_DIR, final_name))
    return f"agent_doc/{final_name}"


def generate_application_no():
    return datetime.now().strftime("%Y%m%d%H%M%S")


# ==========================================================
# REGISTER AGENT
# ==========================================================


@agent_other_than_individual_registration_bp.route(
    "/agent/other-than-individual", methods=["POST"]
)
def register_agent():
    try:
        form = request.form
        files = request.files

        application_no = generate_application_no()

        affidavit_value = form.get("self_declared_affidavit")

        if affidavit_value in (None, "", "null"):
            affidavit_value = None
        else:
            try:
                affidavit_value = json.loads(affidavit_value)
            except Exception:
                affidavit_value = None

        # ================= MASTER TABLE =================

        agent = AgentOtherThanIndividualOrganisation(
            agent_type="Other Than Individual",
            application_no=application_no,
            agent_name=form.get("organisation_name"),
            father_name="NA",
            occupation_id=None,
            email=form.get("email_id"),
            aadhaar=None,
            pan=form.get("pan_card_number"),
            mobile=form.get("mobile_number"),
            landline=form.get("landline_number"),
            license_number=None,
            license_date=None,
            address1=form.get("address_line1"),
            address2=form.get("address_line2"),
            state_id=form.get("state"),
            district=form.get("district"),
            mandal=form.get("mandal"),
            village=form.get("village"),
            pincode=form.get("pincode"),
            photograph={},
            pan_proof={"file": save_file(files.get("pan_card_doc"), "org_pan")},
            address_proof={
                "file": save_file(files.get("address_proof_doc"), "address_proof")
            },
            self_declared_affidavit=affidavit_value,
           
            any_civil_criminal_cases=None,
            registration_other_states=json.dumps(
                json.loads(form.get("other_state_rera_details", "[]"))
            ),
            declaration=True,
            organisation_type=form.get("organisation_type"),
            registration_identifier=form.get("registration_number"),
            registration_date=form.get("registration_date"),
            registration_cert_doc=save_file(
                files.get("registration_cert_doc"), "registration_cert"
            ),
            gst_number=form.get("gst_number"),
            gst_doc=save_file(files.get("gst_doc"), "gst"),
            legal_document=save_file(
                files.get("memorandum_doc") or files.get("partnership_deed"),
                "legal_document",
            ),
            last_five_years_projects_details=json.loads(
                form.get("last_five_year_projects", "[]")
            ),
        )

        db.session.add(agent)
        db.session.flush()
        agent_id = agent.id

        # ================= ENTITIES =================

        entities_data = json.loads(form.get("entities", "[]"))

        for index, e in enumerate(entities_data):
            entity = AgentOtherThanIndividualEntity(
                designation=e.get("designation"),
                name=e.get("name"),
                email_id=e.get("email"),
                mobile_number=e.get("mobile"),
                state_ut=e.get("state"),
                district=e.get("district"),
                address_line1=e.get("address1"),
                address_line2=e.get("address2"),
                pincode=e.get("pincode"),
                pan_card_number=e.get("pan"),
                aadhaar_number=e.get("aadhaar"),
                entity_type=e.get("nationality"),
                din_number=e.get("din"),
                photograph=save_file(
                    files.get(f"entity_photo_{index}"), f"entity_photo_{index}"
                ),
                aadhaar_doc=save_file(
                    files.get(f"entity_aadhaar_doc_{index}"), f"entity_aadhaar_{index}"
                ),
                pan_card_doc=save_file(
                    files.get(f"entity_pan_doc_{index}"), f"entity_pan_{index}"
                ),
                address_proof=save_file(
                    files.get(f"entity_address_proof_{index}"),
                    f"entity_address_{index}",
                ),
                organisation_id=agent_id,
            )
            db.session.add(entity)

        # ================= AUTHORIZED =================

        authorized_data = json.loads(form.get("authorized_persons", "[]"))

        for index, a in enumerate(authorized_data):
            authorized = AgentOtherThanIndividualAuthorized(
                name=a.get("name"),
                email_id=a.get("email"),
                mobile_number=a.get("mobile"),
                photo=save_file(
                    files.get(f"authorized_photo_{index}"), f"authorized_photo_{index}"
                ),
                board_resolution=save_file(
                    files.get(f"board_resolution_{index}"), f"board_resolution_{index}"
                ),
                organisation_id=agent_id,
            )
            db.session.add(authorized)

        # ================= LITIGATIONS =================

        litigations_data = json.loads(form.get("litigations", "[]"))

        if litigations_data:
            for index, l in enumerate(litigations_data):
                litigation = AgentOtherThanIndividualLitigation(
                    case_no=l.get("case_no"),
                    tribunal_place=l.get("tribunal_name_place"),
                    petitioner_name=l.get("petitioner_name"),
                    respondent_name=l.get("respondent_name"),
                    case_facts=l.get("case_facts"),
                    present_status=l.get("present_status"),
                    interim_order_certificate={
                        "file": save_file(
                            files.get(f"interim_certificate_{index}"),
                            f"interim_{index}",
                        )
                    },
                    disposed_certificate={
                        "file": save_file(
                            files.get(f"final_certificate_{index}"), f"final_{index}"
                        )
                    },
                    self_declared_affidavit=None,
                    agent_id=agent_id,
                )
                db.session.add(litigation)
        else:
            affidavit_file = save_file(files.get("self_affidavit"), "self_affidavit")
            litigation = AgentOtherThanIndividualLitigation(
                self_declared_affidavit=affidavit_file,
                agent_id=agent_id,
            )
            db.session.add(litigation)

        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "agent_id": agent_id,
                    "application_no": application_no,
                    "pan": agent.pan,
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        logger.error("REGISTER ERROR", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


# ==========================================================
# GET DETAILS
# ==========================================================


@agent_other_than_individual_registration_bp.route(
    "/agent/other-than-individual/details", methods=["GET"]
)
def get_agent_other_than_individual_details():

    organisation_id = request.args.get("organisation_id")

    if not organisation_id:
        return jsonify({"status": "error", "message": "organisation_id required"}), 400

    organisation = AgentOtherThanIndividualOrganisation.query.filter_by(
        id=organisation_id
    ).first()

    if not organisation:
        return jsonify({"status": "error", "message": "Not found"}), 404

    entities = AgentOtherThanIndividualEntity.query.filter_by(
        organisation_id=organisation_id
    ).all()

    authorized = AgentOtherThanIndividualAuthorized.query.filter_by(
        organisation_id=organisation_id
    ).all()

    litigations = AgentOtherThanIndividualLitigation.query.filter_by(
        agent_id=organisation_id
    ).all()

    return (
        jsonify(
            {
                "status": "success",
                "organisation": organisation.to_dict(),
                "entities": [e.to_dict() for e in entities],
                "authorized": [a.to_dict() for a in authorized],
                "litigations": [l.to_dict() for l in litigations],
            }
        ),
        200,
    )


# ==========================================================
# SERVE FILES
# ==========================================================


@agent_other_than_individual_registration_bp.route(
    "/agent_doc/<path:filename>", methods=["GET"]
)
def serve_agent_files(filename):
    return send_from_directory(UPLOAD_DIR, filename)


@agent_other_than_individual_registration_bp.route(
    "/agent/other-than-individual/itr", methods=["PATCH"]
)
def update_agent_itr_documents():
    try:
        form = request.form
        files = request.files

        id = form.get("id")
        pan_card_number = form.get("pan_card_number")

        if not id or not pan_card_number:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "id and pan_card_number are required",
                    }
                ),
                400,
            )

        organisation = AgentOtherThanIndividualOrganisation.query.filter_by(
            id=id, pan=pan_card_number
        ).first()

        if not organisation:
            return (
                jsonify({"status": "error", "message": "Organisation not found"}),
                404,
            )

        if files.get("itr_year1"):
            organisation.itr_year1 = save_file(files.get("itr_year1"), "itr1")

        if files.get("itr_year2"):
            organisation.itr_year2 = save_file(files.get("itr_year2"), "itr2")

        if files.get("itr_year3"):
            organisation.itr_year3 = save_file(files.get("itr_year3"), "itr3")

        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "ITR documents updated successfully",
                    "itr_documents": {
                        "itr_year1": organisation.itr_year1,
                        "itr_year2": organisation.itr_year2,
                        "itr_year3": organisation.itr_year3,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        logger.error("ITR PATCH ERROR", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500
@agent_other_than_individual_registration_bp.route(
    "/check-application/<application_no>", methods=["GET"]
)
def check_application(application_no):
    try:
        exists = AgentOtherThanIndividualOrganisation.is_application_exists(
            application_no
        )

        return jsonify({"exists": exists}), 200

    except Exception as e:
        return jsonify({"exists": False, "error": str(e)}), 500
