from flask import Blueprint, request, jsonify
from app.services.chat_service import ChatService

chat_bp = Blueprint("chat_bp", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Message is required"}), 400

    user_message = data["message"]
    response = ChatService.process_message(user_message)

    return jsonify({"response": response}), 200