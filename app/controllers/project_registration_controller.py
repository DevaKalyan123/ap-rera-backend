import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.models.project_registration_model import (
    insert_project_registration,
    get_project_registration
)
# from app.models.extension_project_application_details_models import (
#     get_project_basic_details_by_pan,
#     insert_extension_project_application
# )



project_registration_bp = Blueprint("project_registration_bp", __name__)

def save_file(file, subfolder):
    if not file:
        return None

    upload_base = current_app.config["UPLOAD_FOLDER"]
    folder = os.path.join(upload_base, subfolder)
    os.makedirs(folder, exist_ok=True)

    filename = secure_filename(file.filename)
    file_path = os.path.join(folder, filename)
    file.save(file_path)
  
    # store relative path in DB
    return f"uploads/{subfolder}/{filename}"
        
@project_registration_bp.route("/project-registration", methods=["POST"])
def project_registration():
    try:
        form = request.form
        files = request.files

        data = {
            "application_number": form.get("applicationNumber"),
            "pan_number": form.get("panNumber"),

            "project_name": form.get("projectName"),
            "project_description": form.get("projectDescription"),
            "project_type": form.get("projectType"),
            "project_status": form.get("projectStatus"),

            "building_plan_no": form.get("buildingPlanNo"),
            "building_permission_from": form.get("buildingPermissionFrom"),
            "building_permission_upto": form.get("buildingPermissionUpto"),
            "date_of_commencement": form.get("dateOfCommencement"),
            "proposed_completion_date": form.get("proposedCompletionDate"),

            "total_area_of_land": form.get("totalAreaOfLand"),
            "building_height": form.get("buildingHeight"),
            "total_plinth_area": form.get("totalPlinthArea"),
            "total_built_up_area": form.get("totalBuiltUpArea"),

            "garages_available_for_sale": form.get("garagesAvailableForSale"),
            "total_garage_area": form.get("totalGarageArea"),
            "open_parking_spaces": form.get("openParkingSpaces"),
            "total_open_parking_area": form.get("totalOpenParkingArea"),
            "covered_parking_spaces": form.get("coveredParkingSpaces"),
            "total_covered_parking_area": form.get("totalCoveredParkingArea"),

            "estimated_construction_cost": form.get("estimatedConstructionCost"),
            "cost_of_land": form.get("costOfLand"),
            "total_open_area": form.get("totalOpenArea"),
            "total_project_cost": form.get("totalProjectCost"),

            "project_address1": form.get("projectAddress1"),
            "project_address2": form.get("projectAddress2"),
            "project_district": form.get("projectDistrict"),
            "project_mandal": form.get("projectMandal"),
            "project_village": form.get("projectVillage"),
            "project_pincode": form.get("projectPincode"),
            "project_latitude": form.get("projectLatitude"),
            "project_longitude": form.get("projectLongitude"),
            "plan_approving_authority": form.get("planApprovingAuthority"),
            "survey_no": form.get("surveyNo"),

            "address_proof_path": save_file(files.get("addressProof"), "address_proofs"),

            "local_address1": form.get("localAddress1"),
            "local_address2": form.get("localAddress2"),
            "local_area": form.get("localArea"),
            "local_landmark": form.get("localLandmark"),
            "local_district": form.get("localDistrict"),
            "local_mandal": form.get("localMandal"),
            "local_village": form.get("localVillage"),
            "local_pincode": form.get("localPincode"),
            "project_website_url": form.get("projectWebsiteURL"),

            "development_completed": form.get("developmentCompleted"),
            "development_pending": form.get("developmentPending"),
            "amount_collected": form.get("amountCollected"),
            "amount_spent": form.get("amountSpent"),
            "balance_amount": form.get("balanceAmount"),
            "plan_modified": form.get("planModified") == "true",

            "architect_certificate_path": save_file(files.get("architectCertificate"), "certificates"),
            "engineer_certificate_path": save_file(files.get("engineerCertificate"), "certificates"),
            "ca_certificate_path": save_file(files.get("caCertificate"), "certificates"),

            "project_delayed": form.get("projectDelayed") == "true",
            "number_of_units": form.get("numberOfUnits"),
            "units_advance_taken": form.get("unitsAdvanceTaken"),
            "units_agreement_sale": form.get("unitsAgreementSale"),
            "units_sold": form.get("unitsSold"),

            "legal_declaration_accepted": form.get("legalDeclarationAccepted") == "true",
        }

        insert_project_registration(data)

        return jsonify({"message": "Project registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    # =====================================
# CHECK + FETCH API  (MAIN API YOU WANT)
# =====================================

@project_registration_bp.route("/get-project-by-application", methods=["POST"])
def get_project_by_application():

    try:

        data = request.get_json()

        application_number = data.get("applicationNumber")
        pan_number = data.get("panNumber")


        if not application_number or not pan_number:
            return jsonify({"error": "Missing data"}), 400


        # 🔹 Check DB
        result = get_project_registration(
            application_number,
            pan_number
        )


        # ✅ If exists → send data
        if result:

            return jsonify({
                "exists": True,
                "data": result
            }), 200


        # ❌ If not exists → allow insert
        return jsonify({
            "exists": False,
            "data": {}
        }), 200


    except Exception as e:

        print("Fetch Error:", e)

        return jsonify({"error": str(e)}), 500
    





# ==========================================================
# ✅ NEW GET API (SEPARATE – SAFE)
# ==========================================================
@project_registration_bp.route("/project-registration/details", methods=["GET"])
def get_project_registration_details():

    try:
        application_number = request.args.get("applicationNumber")
        pan_number = request.args.get("panNumber")

        if not application_number or not pan_number:
            return jsonify({
                "success": False,
                "message": "applicationNumber and panNumber required"
            }), 400

        result = get_project_registration(application_number, pan_number)

        return jsonify({
            "success": True,
            "data": result if result else {}
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
        
        
        
# ==========================================================
# ✅ NEW UPDATE API (FINAL CORRECT VERSION)
# ==========================================================
# @project_registration_bp.route("/project-registration/update", methods=["PUT"])
# def update_project_registration_new():

#     from app.models.project_registration_model import update_project_registration

#     try:
#         data = request.get_json()

#         if not data:
#             return jsonify({
#                 "success": False,
#                 "message": "No data received"
#             }), 400

#         application_number = data.get("applicationNumber")
#         pan_number = data.get("panNumber")

#         if not application_number or not pan_number:
#             return jsonify({
#                 "success": False,
#                 "message": "applicationNumber and panNumber required"
#             }), 400

#         # Add DB format keys
#         data["application_number"] = application_number
#         data["pan_number"] = pan_number

#         rows = update_project_registration(data)

#         if rows > 0:
#             return jsonify({
#                 "success": True,
#                 "message": "Project updated successfully"
#             }), 200
#         else:
#             return jsonify({
#                 "success": False,
#                 "message": "No record updated"
#             }), 200   # Not 404 (important)

#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         return jsonify({
#             "success": False,
#             "error": str(e)
#         }), 500

@project_registration_bp.route("/project-registration/update", methods=["PUT"])
def update_project_registration_new():

    from app.models.project_registration_model import update_project_registration
    from werkzeug.utils import secure_filename
    import os

    try:
        # 🔥 Detect if request is JSON or multipart
        if request.content_type.startswith("multipart/form-data"):
            data = request.form.to_dict()
            files = request.files
        else:
            data = request.get_json()
            files = {}

        if not data:
            return jsonify({
                "success": False,
                "message": "No data received"
            }), 400

        application_number = data.get("applicationNumber")
        pan_number = data.get("panNumber")

        if not application_number or not pan_number:
            return jsonify({
                "success": False,
                "message": "applicationNumber and panNumber required"
            }), 400

        # ✅ Add DB keys
        data["application_number"] = application_number
        data["pan_number"] = pan_number

        # =====================================================
        # 🔹 HANDLE FILE UPDATES (ONLY IF FILES SENT)
        # =====================================================

        if files:

            upload_folder = os.path.join(
                "uploads",
                "project_registration",
                application_number
            )
            os.makedirs(upload_folder, exist_ok=True)

            file_fields = {
                "addressProof": "address_proof_path",
                "architectCertificate": "architect_certificate_path",
                "engineerCertificate": "engineer_certificate_path",
                "caCertificate": "ca_certificate_path",
                "authorizedSignatoryPhoto": "authorized_signatory_photo_path",
                "boardResolutionCopy": "board_resolution_copy_path",
            }

            for frontend_key, db_column in file_fields.items():
                if frontend_key in files:
                    file = files[frontend_key]

                    if file and file.filename:
                        filename = secure_filename(file.filename)
                        filepath = os.path.join(upload_folder, filename)
                        file.save(filepath)

                        # Save path into data for DB update
                        data[db_column] = filepath

        # =====================================================
        # 🔹 CALL YOUR EXISTING UPDATE FUNCTION
        # =====================================================

        rows = update_project_registration(data)

        if rows > 0:
            return jsonify({
                "success": True,
                "message": "Project updated successfully"
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "No record updated"
            }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ------------------------------vamsi anna apis --------------------------------

@project_registration_bp.route("/extension-application", methods=["POST"])
def submit_extension_application():
    from app.models.extension_project_application_details_models import insert_extension_project_application
    try:
        form = request.form
        files = request.files

        def save_extension_file(file, subfolder):
            if not file:
                return None

            upload_base = current_app.config["UPLOAD_FOLDER"]

            # ✅ REQUIRED EXTENSION UPLOAD PATH
            folder = os.path.join(
                upload_base,
                "project_registration_extention",
                subfolder
            )
            os.makedirs(folder, exist_ok=True)

            filename = secure_filename(file.filename)
            file_path = os.path.join(folder, filename)
            file.save(file_path)

            # ✅ store relative path in DB
            return f"uploads/project_registration_extention/{subfolder}/{filename}"

        data = {
            "application_number": form.get("application_number"),
            "project_name": form.get("project_name"),
            "project_id": form.get("project_id"),

            "validity_from": form.get("validity_from"),
            "validity_to": form.get("validity_to"),

            "new_validity_from": form.get("new_validity_from"),
            "new_validity_to": form.get("new_validity_to"),

            # 📂 EXTENSION DOCUMENTS
            "representation_letter": save_extension_file(
                files.get("representation_letter"),
                "representation_letter"
            ),
            "form_b": save_extension_file(files.get("form_b"), "form_b"),
            "consent_letter": save_extension_file(
                files.get("consent_letter"),
                "consent_letter"
            ),
            "form_e": save_extension_file(files.get("form_e"), "form_e"),
            "form_p4": save_extension_file(files.get("form_p4"), "form_p4"),
            "extension_proceeding": save_extension_file(
                files.get("extension_proceeding"),
                "extension_proceeding"
            ),
        }

        insert_extension_project_application(data)

        return jsonify({
            "message": "Extension application submitted successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

    

    
@project_registration_bp.route("/project/basic-details-by-pan", methods=["GET"])
def get_project_basic_details_by_pan_controller():
    from app.models.extension_project_application_details_models import get_project_basic_details_by_pan
    pan_number = request.args.get("pan")

    if not pan_number:
        return jsonify({
            "success": False,
            "message": "pan is required"
        }), 400

    data = get_project_basic_details_by_pan(pan_number)

    return jsonify({
        "success": True,
        "data": data
    }), 200

# =====================================
# ✅ SINGLE PROJECT (AUTO TYPE - BEST API)
# =====================================
@project_registration_bp.route("/planning-single", methods=["GET"])
def planning_single():

    application_number = request.args.get("applicationNumber")
    pan_number = request.args.get("panNumber")

    if not application_number or not pan_number:
        return jsonify({"error": "Missing data"}), 400

    from app.models.planning_documents_model import get_planning_single

    data = get_planning_single(application_number, pan_number)

    if not data:
        return jsonify({"error": "No project found"}), 404

    return jsonify({
        "success": True,
        "data": data
    }), 200


# =====================================
# ✅ ALL PROJECTS (INDIVIDUAL + OTHER)
# =====================================
@project_registration_bp.route("/planning-dashboard-all", methods=["GET"])
def planning_dashboard_all():

    from app.models.planning_documents_model import get_all_planning_dashboard_mixed

    data = get_all_planning_dashboard_mixed()

    return jsonify({
        "success": True,
        "data": data
    }), 200


# =====================================
# ✅ FILTER BY TYPE
# =====================================
@project_registration_bp.route("/planning-dashboard-all-by-type", methods=["GET"])
def planning_dashboard_all_by_type():

    user_type = request.args.get("type")  # individual / other

    if not user_type:
        return jsonify({"error": "type required"}), 400

    from app.models.planning_documents_model import get_all_planning_dashboard_by_type

    data = get_all_planning_dashboard_by_type(user_type)

    return jsonify({
        "success": True,
        "data": data
    }), 200