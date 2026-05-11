# from flask import Blueprint, request, jsonify
# from app.models.project_agent import AgentModel
# from app.models.database import db

# project_agent_bp = Blueprint("project_agent", __name__)

# @project_agent_bp.route("/associate/project-agent", methods=["POST"])
# def create_project_agent():
#     try:
#         data = request.get_json()

#         required_fields = [
#             "rera_registration_no",
#             "agent_name",
#             "agent_address",
#             "mobile_number"
#         ]

#         for field in required_fields:
#             if not data.get(field):
#                 return jsonify({
#                     "success": False,
#                     "message": f"{field} is required"
#                 }), 400

#         agent = AgentModel(
#             rera_registration_no=data["rera_registration_no"],
#             agent_name=data["agent_name"],
#             agent_address=data["agent_address"],
#             mobile_number=data["mobile_number"],
#         )

#         db.session.add(agent)
#         db.session.commit()  # 🔥 THIS WAS MISSING IN YOUR PROJECT

#         return jsonify({
#             "success": True,
#             "data": {
#                 "id": agent.id
#             }
#         }), 201

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({
#             "success": False,
#             "message": str(e)
#         }), 500
