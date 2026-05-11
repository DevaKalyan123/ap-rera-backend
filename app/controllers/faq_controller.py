from flask import Blueprint, jsonify
from app.services.faq_service import FaqService

faq_bp = Blueprint("faq_bp", __name__)

@faq_bp.route("/faq/init", methods=["POST"])
def init_faq():
    result = FaqService.initialize_sample_data()
    return jsonify({"message": result}), 200