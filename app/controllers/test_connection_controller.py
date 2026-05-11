from flask import Blueprint, request, jsonify
from app.models.test_connection import TestConnectionModel

test_connection_bp = Blueprint("test_connection_bp", __name__)

@test_connection_bp.route("/test", methods=["POST"])
def create_test():
    data = request.json
    row = TestConnectionModel.insert(data.get("name"))

    return jsonify({
        "id": row.id,
        "name": row.name
    }), 201


@test_connection_bp.route("/test", methods=["GET"])
def get_tests():
    rows = TestConnectionModel.fetch_all()

    return jsonify([
        {
            "id": r.id,
            "name": r.name,
            "created_at": str(r.created_at)
        } for r in rows
    ])
