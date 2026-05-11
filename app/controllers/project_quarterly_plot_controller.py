# app/controllers/project_quarterly_plot_controller.py

from flask import Blueprint, request, jsonify
import json
from app.models.project_quarterly_plot_model import ProjectQuarterlyPlotModel
from app.utils.file_upload import save_file   # use your existing util

project_quarterly_plot_bp = Blueprint(
    "project_quarterly_plot_bp", __name__
)


@project_quarterly_plot_bp.route(
    "/api/project/quarterly/plot/save", methods=["POST"]
)
def save_quarterly_plot_details():

    try:
        project_id = request.form.get("project_id")
        quarter = request.form.get("quarter")
        rows = json.loads(request.form.get("rows"))

        for index, row in enumerate(rows):

            # ---------- SALE DOCUMENT ----------
            sale_doc = request.files.get(f"saleDoc_{index}")
            if sale_doc:
                row["sale_document_path"] = save_file(
                    sale_doc, "project_sale_docs"
                )
            else:
                row["sale_document_path"] = None

            # ---------- PHOTOS ----------
            photo_paths = []
            photos = request.files.getlist(f"photos_{index}")
            for photo in photos:
                photo_paths.append(
                    save_file(photo, "project_photos")
                )

            row["photo_paths"] = photo_paths

        payload = {
            "project_id": project_id,
            "quarter": quarter,
            "rows": rows
        }

        return ProjectQuarterlyPlotModel.insert_quarterly_plot_details(payload)

    except Exception as e:
        return {"success": False, "message": str(e)}