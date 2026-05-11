# app/controllers/location_controller.py

from flask import Blueprint, jsonify
from app.models.location_models import LocationModel

location_bp = Blueprint("location", __name__)

# -------------------------
# GET STATES
# -------------------------
@location_bp.route("/states", methods=["GET"])
def get_states():
    data = LocationModel.get_states()
    return jsonify(data), 200


# -------------------------
# GET DISTRICTS BY STATE
# -------------------------
@location_bp.route("/districts/<int:state_id>", methods=["GET"])
def get_districts(state_id):
    data = LocationModel.get_districts_by_state(state_id)
    return jsonify(data), 200


# -------------------------
# GET MANDALS BY DISTRICT
# -------------------------
@location_bp.route("/mandals/<int:district_id>", methods=["GET"])
def get_mandals(district_id):
    data = LocationModel.get_mandals_by_district(district_id)
    return jsonify(data), 200


# -------------------------
# GET VILLAGES BY MANDAL
# -------------------------
@location_bp.route("/villages/<int:mandal_id>", methods=["GET"])
def get_villages(mandal_id):
    data = LocationModel.get_villages_by_mandal(mandal_id)
    return jsonify(data), 200
