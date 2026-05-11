from sqlalchemy import text
from app.models.database import db

def _normalize_agent_type(value):
    val = (value or "").lower().strip()
    # DB stores "Other Than Individual" or "other" for org agents
    if "other" in val:
        return "Other Than Individual"
    return "Individual"

def _build_scrutiny_label(agent_type):
    val = (agent_type or "").lower().strip()
    return "S1" if "other" in val else "S2"

def _serialize_agent_row(row):
    agent_type = row["agent_type"]
    return {
        "application_no": row["application_no"],
        "promoter_type": agent_type,
        "promoter_display": _normalize_agent_type(agent_type),
        "applicant_name": row["agent_name"],
        "mobile": row["mobile"],
        "email": row["email"],
        "project_name": row["agent_name"], # We use Agent Name as there is no project name
        "project_type": _normalize_agent_type(agent_type),
        "project_status": "Under Scrutiny",
        "project_cost": "N/A",
        "district": row["district"] or "N/A",
        "status": "PENDING",
        "created_at": str(row["created_at"]) if "created_at" in row and row["created_at"] else None,
        "scrutiny_label": _build_scrutiny_label(agent_type),
        "review_desk": "Technical Committee",
        "wizard": {},
        "preview": {},
    }

def get_agent_scrutiny_registrations(dept=None):
    condition = ""
    
    ad_districts = [
        "Alluri Sitharama Raju", "Anakapalli", "Anantapuramu", "Annamayya",
        "Bapatla", "Chittoor", "Dr. B.R. Ambedkar Konaseema", "East Godavari",
        "Eluru", "Guntur", "Kakinada", "Krishna", "NTR"
    ]
    ad_districts_str = ", ".join([f"UPPER('{d}')" for d in ad_districts])

    if dept and dept.lower() != "verification":
        required_verification = "'verification'"
        is_ad = dept.lower() in ["ad", "assistant director"]
        is_dd = dept.lower() in ["dd", "deputy director"]

        if is_ad or is_dd:
            required_verification = "'planning'"

        condition += f"""
        AND EXISTS (
            SELECT 1 
            FROM agent_verification_final_status_t v
            WHERE TRIM(v.application_no) = TRIM(a.application_no)
            AND v.status = 'verified'
            AND LOWER(v.verified_by) = {required_verification}
        )
        """

        if is_ad:
            condition += f"\n        AND UPPER(COALESCE(dm.district_name, CAST(a.district AS TEXT))) IN ({ad_districts_str})"
        elif is_dd:
            condition += f"\n        AND (UPPER(COALESCE(dm.district_name, CAST(a.district AS TEXT))) NOT IN ({ad_districts_str}) OR COALESCE(dm.district_name, CAST(a.district AS TEXT)) IS NULL)"

    query = text(f"""
        SELECT
            a.application_no AS application_no,
            a.agent_type AS agent_type,
            a.agent_name AS agent_name,
            a.mobile AS mobile,
            a.email AS email,
            COALESCE(dm.district_name, CAST(a.district AS TEXT)) AS district,
            NOW() AS created_at -- Fallback if no created_at exists in agentregistration_details_t
        FROM agentregistration_details_t a
        LEFT JOIN districts_t dm
          ON CAST(a.district AS TEXT) = CAST(dm.id AS TEXT)
        WHERE 1=1
        {condition}
        ORDER BY a.id DESC
    """)

    rows = db.session.execute(query).mappings().all()
    return [_serialize_agent_row(row) for row in rows]

def get_agent_scrutiny_registration_by_application(application_no):
    query = text(
        """
        SELECT
            a.id AS agent_id,
            a.application_no AS application_no,
            a.agent_type AS agent_type,
            a.agent_name AS agent_name,
            a.mobile AS mobile,
            a.email AS email,
            COALESCE(dm.district_name, CAST(a.district AS TEXT)) AS district,
            NOW() AS created_at
        FROM agentregistration_details_t a
        LEFT JOIN districts_t dm
          ON CAST(a.district AS TEXT) = CAST(dm.id AS TEXT)
        WHERE TRIM(a.application_no) = TRIM(:application_no)
        LIMIT 1
        """
    )
    row = db.session.execute(query, {"application_no": application_no}).mappings().first()
    if not row:
        return None

    return _serialize_agent_row(row)

def get_agent_scrutiny_full_details(application_no):
    try:
        # First get the agent row to check type
        query_agent = text("""
            SELECT id, agent_type, organisation_type, registration_identifier,
                   registration_date, registration_cert_doc,
                   gst_number, gst_doc, legal_document,
                   agent_name, pan, email, mobile, landline,
                   address1, address2, state_id, district, mandal, village, pincode,
                   pan_proof, address_proof, photograph,
                   self_declared_affidavit,
                   itr_year1, itr_year2, itr_year3,
                   last_five_years_projects_details,
                   any_civil_criminal_cases, registration_other_states
            FROM agentregistration_details_t
            WHERE application_no = :app_no LIMIT 1
        """)
        agent_row = db.session.execute(query_agent, {"app_no": application_no}).mappings().first()
        if not agent_row:
            return {"success": False, "message": "Agent not found"}

        agent_id = agent_row["id"]
        agent_type_val = (agent_row["agent_type"] or "").lower()
        is_other = "other" in agent_type_val

        if is_other:
            # --- Other Than Individual: build dict directly from the row ---
            def safe_json(val):
                """Return val as-is if already dict, parse if string, else None."""
                if val is None:
                    return None
                if isinstance(val, dict):
                    return val
                try:
                    import json as _json
                    return _json.loads(val)
                except Exception:
                    return {"file": val}  # treat plain string as file path

            agent_details = {
                "agent_id": agent_id,
                "agent_type": agent_row["agent_type"],
                "agent_name": agent_row["agent_name"],
                "organisation_type": agent_row["organisation_type"],
                "registration_identifier": agent_row["registration_identifier"],
                "registration_date": str(agent_row["registration_date"]) if agent_row["registration_date"] else None,
                "registration_cert_doc": agent_row["registration_cert_doc"],
                "gst_number": agent_row["gst_number"],
                "gst_doc": agent_row["gst_doc"],
                "legal_document": agent_row["legal_document"],
                "pan": agent_row["pan"],
                "email": agent_row["email"],
                "mobile": agent_row["mobile"],
                "landline": agent_row["landline"],
                "address1": agent_row["address1"],
                "address2": agent_row["address2"],
                "state_id": agent_row["state_id"],
                "district": agent_row["district"],
                "mandal": agent_row["mandal"],
                "village": agent_row["village"],
                "pincode": agent_row["pincode"],
                "pan_proof": safe_json(agent_row["pan_proof"]),
                "address_proof": safe_json(agent_row["address_proof"]),
                "photograph": safe_json(agent_row["photograph"]),
                "self_declared_affidavit": safe_json(agent_row["self_declared_affidavit"]),
                "itr_year1": agent_row["itr_year1"],
                "itr_year2": agent_row["itr_year2"],
                "itr_year3": agent_row["itr_year3"],
                "last_five_years_projects_details": safe_json(agent_row["last_five_years_projects_details"]) or [],
                "any_civil_criminal_cases": agent_row["any_civil_criminal_cases"],
                "registration_other_states": agent_row["registration_other_states"],
            }

            # Fetch entities (directors/partners/trustees)
            from app.models.agent_other_than_individual_registration_entity_model import AgentOtherThanIndividualEntity
            entities = AgentOtherThanIndividualEntity.query.filter_by(organisation_id=agent_id).all()

            # Fetch authorized persons
            from app.models.agent_other_than_individual_registration_authorized_model import AgentOtherThanIndividualAuthorized
            authorized = AgentOtherThanIndividualAuthorized.query.filter_by(organisation_id=agent_id).all()

            return {
                "success": True,
                "data": {
                    "agent_details": agent_details,
                    "entities": [e.to_dict() for e in entities],
                    "authorized_persons": [a.to_dict() for a in authorized],
                    "projects": [],
                    "litigations": [],
                    "other_state_rera": [],
                }
            }
        else:
            # --- Individual: use the existing preview function (safe with integer JOINs) ---
            from app.models.agent_registration_model import AgentModel
            return AgentModel.get_agent_preview(agent_id)

    except Exception as e:
        return {"success": False, "message": str(e)}


def _clean_optional(value):
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return value

def create_agent_scrutiny_file(data):
    query = text(
        """
        INSERT INTO agent_scrutiny_files_t (
            file_number, inward_no, memo_number, file_date, "type",
            from_where, to_whom, assign_to, description, remarks,
            document_desc, file_path
        )
        VALUES (
            :file_number, :inward_no, :memo_number, :file_date, :type,
            :from_where, :to_whom, :assign_to, :description, :remarks,
            :document_desc, :file_path
        )
        RETURNING *
        """
    )
    params = {
        "file_number": data.get("file_number"),
        "inward_no": data.get("inward_no"),
        "memo_number": _clean_optional(data.get("memo_number")),
        "file_date": data.get("file_date"),
        "type": data.get("type"),
        "from_where": data.get("from_where"),
        "to_whom": data.get("to_whom"),
        "assign_to": data.get("assign_to"),
        "description": data.get("description"),
        "remarks": _clean_optional(data.get("remarks")),
        "document_desc": _clean_optional(data.get("document_desc")),
        "file_path": _clean_optional(data.get("file_path")),
    }
    row = db.session.execute(query, params).mappings().first()
    db.session.commit()
    return dict(row) if row else None

def get_agent_scrutiny_fpms_dashboard_data():
    summary_query = text("SELECT COUNT(*) AS total_files FROM agent_scrutiny_files_t")
    files_query = text("SELECT * FROM agent_scrutiny_files_t ORDER BY created_at DESC, id DESC")

    summary_row = db.session.execute(summary_query).mappings().first()
    file_rows = db.session.execute(files_query).mappings().all()

    total_files = int(summary_row["total_files"] or 0) if summary_row else 0
    rows = []
    for index, row in enumerate(file_rows, start=1):
        rows.append({
            "id": row["id"],
            "s_no": index,
            "file_number": row["file_number"],
            "inward_no": row["inward_no"],
            "memo_number": row["memo_number"],
            "file_date": str(row["file_date"]) if row["file_date"] else None,
            "file_description": row["description"],
            "received_through": row["type"],
            "from_where": row["from_where"],
            "to_whom": row["to_whom"],
            "assign_to": row["assign_to"],
            "file_assigned_date": str(row["created_at"]) if row["created_at"] else None,
            "status": "Created",
            "remarks": row["remarks"],
            "document_desc": row["document_desc"],
            "file_path": row["file_path"],
            "created_at": str(row["created_at"]) if row["created_at"] else None,
        })
    return {
        "summary": {"total_files": total_files, "open_files": total_files, "closed_files": 0},
        "rows": rows,
    }

def create_agent_verification_remark(data):
    query = text(
        """
        INSERT INTO agent_verification_remarks_t (
            application_no, document_name, verification_team, is_shortfall,
            status, remarks, document_path, verified_by, updated_at
        )
        VALUES (
            :application_no, :document_name, :verification_team, :is_shortfall,
            :status, :remarks, :document_path, :verified_by, CURRENT_TIMESTAMP
        )
        RETURNING *
        """
    )
    params = {
        "application_no": data.get("application_no"),
        "document_name": data.get("document_name"),
        "verification_team": data.get("verification_team"),
        "is_shortfall": bool(data.get("is_shortfall", False)),
        "status": data.get("status") or "pending",
        "remarks": _clean_optional(data.get("remarks")),
        "document_path": _clean_optional(data.get("document_path")),
        "verified_by": _clean_optional(data.get("verified_by")),
    }
    row = db.session.execute(query, params).mappings().first()
    db.session.commit()
    return dict(row) if row else None

def get_agent_verification_remarks(application_no, document_name=None, verification_team=None):
    query = text(
        """
        SELECT * FROM agent_verification_remarks_t
        WHERE TRIM(application_no) = TRIM(:application_no)
          AND (:document_name IS NULL OR document_name = :document_name)
          AND (:verification_team IS NULL OR verification_team = :verification_team)
        ORDER BY created_at DESC, id DESC
        """
    )
    params = {
        "application_no": application_no,
        "document_name": _clean_optional(document_name),
        "verification_team": _clean_optional(verification_team),
    }
    rows = db.session.execute(query, params).mappings().all()
    
    # Needs created_at string formatting
    results = []
    for row in rows:
        d = dict(row)
        d['created_at'] = str(d['created_at']) if d.get('created_at') else None
        d['updated_at'] = str(d['updated_at']) if d.get('updated_at') else None
        results.append(d)
    return results

def create_agent_final_verification(data):
    query = text("""
        INSERT INTO agent_verification_final_status_t (
            application_no, status, is_shortfall, verified_by, remarks
        )
        VALUES (
            :application_no, 'verified', :is_shortfall, :verified_by, :remarks
        )
        ON CONFLICT (application_no, verified_by)
        DO UPDATE SET
            status = 'verified',
            is_shortfall = EXCLUDED.is_shortfall,
            verified_by = EXCLUDED.verified_by,
            remarks = EXCLUDED.remarks,
            verified_at = CURRENT_TIMESTAMP
        RETURNING *;
    """)
    row = db.session.execute(query, data).mappings().first()
    db.session.commit()
    d = dict(row)
    d['verified_at'] = str(d['verified_at']) if d.get('verified_at') else None
    return d

def get_agent_final_status(application_no):
    query = text("""
        SELECT * FROM agent_verification_final_status_t
        WHERE TRIM(application_no) = TRIM(:application_no)
    """)
    rows = db.session.execute(query, {"application_no": application_no}).mappings().all()
    results = []
    for row in rows:
        d = dict(row)
        d['verified_at'] = str(d['verified_at']) if d.get('verified_at') else None
        results.append(d)
    return results