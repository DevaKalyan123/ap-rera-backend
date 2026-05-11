from flask import Blueprint, jsonify
from app.models.occupation_model import Occupation

occupation_controller = Blueprint("occupation_controller", __name__)

@occupation_controller.route("/occupations", methods=["GET"])
def fetch_occupations():
    try:
        occupations = Occupation.get_all()
        data = [
            {
                "occupation_id": o.occupation_id,
                "occupation_name": o.occupation_name
            }
            for o in occupations
        ]

        return jsonify({
            "success": True,
            "data": data
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Failed to fetch occupations",
            "error": str(e)
        }), 500