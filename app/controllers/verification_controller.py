from flask import Blueprint, jsonify
from app.utils.geo_utils import calculate_distance, get_timeline_gap
from app import db  # or your DB connection
from sqlalchemy import text

verification_bp = Blueprint('verification', __name__)

@verification_bp.route('/verify/<app_no>', methods=['GET'])
def verify(app_no):

    query = """
    SELECT 
        p.project_latitude,
        p.project_longitude,
        d.image_url,
        d.image_latitude,
        d.image_longitude,
        d.captured_date
    FROM project_registration p
    JOIN development_details d
    ON p.application_number = d.application_number
    WHERE p.application_number = :app_no
    ORDER BY d.captured_date DESC
    """

    rows = db.session.execute(text(query), {"app_no": app_no}).fetchall()

    if not rows:
        return jsonify({"error": "No data found"}), 404

    latest = rows[0]

    # ✅ Extract values
    proj_lat = latest[0]
    proj_lng = latest[1]
    img_lat = latest[3]
    img_lng = latest[4]

    # ✅ Validate project location
    if not proj_lat or not proj_lng:
        return jsonify({"error": "Project location missing"}), 400

    try:
        proj_lat = float(proj_lat)
        proj_lng = float(proj_lng)
    except ValueError:
        return jsonify({"error": "Invalid project coordinates"}), 400

    # ✅ Handle image location (optional now)
    if img_lat and img_lng:
        try:
            img_lat = float(img_lat)
            img_lng = float(img_lng)

            distance = calculate_distance(proj_lat, proj_lng, img_lat, img_lng)
            location_valid = distance <= 0.5
        except ValueError:
            distance = None
            location_valid = False
    else:
        distance = None
        location_valid = False

    # ✅ Timeline
    dates = [str(r[5]) for r in rows if r[5]]
    timeline_gap = get_timeline_gap(dates)

    # ✅ Images
    images = [
        {"url": r[2], "date": str(r[5])}
        for r in rows[:2]
    ]

    return jsonify({
    "location_valid": location_valid,
    "distance_km": distance,
    "timeline_gap": timeline_gap,
    "lat": proj_lat,
    "lng": proj_lng,
    "img_lat": img_lat if img_lat else None,
    "img_lng": img_lng if img_lng else None,
    "images": images,
    "note": "Image location not available" if not img_lat else None
})