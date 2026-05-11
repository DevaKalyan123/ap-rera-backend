from flask import Blueprint, jsonify
from app.models.database import db
from sqlalchemy import text

admin_requests_bp = Blueprint("admin_requests_bp", __name__)

# Get all pending requests
@admin_requests_bp.route("/admin/requests", methods=["GET"])
def get_requests():

    result = db.session.execute(
        text("SELECT id, pan_number, status FROM change_requests")
    )

    requests = []

    for row in result:
        requests.append({
            "id": row.id,
            "pan_number": row.pan_number,
            "status": row.status
        })

    return jsonify(requests)