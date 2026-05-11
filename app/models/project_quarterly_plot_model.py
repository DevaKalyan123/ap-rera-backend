from app.models.database import db
from sqlalchemy import text
import json


class ProjectQuarterlyPlotModel:

    @staticmethod
    def insert_quarterly_plot_details(data):
        try:
            query = text("""
                INSERT INTO project_quarterly_plot_details (
                    project_id,
                    quarter,
                    plot_no,
                    construction_status,
                    sale_status,
                    remarks,
                    sale_document_path,
                    photo_paths,
                    is_saved
                )
                VALUES (
                    :project_id,
                    :quarter,
                    :plot_no,
                    :construction_status,
                    :sale_status,
                    :remarks,
                    :sale_document_path,
                    CAST(:photo_paths AS jsonb),
                    TRUE
                )
            """)

            for row in data["rows"]:

                # ✅ Skip rows where nothing is filled
                if not (
                    row.get("constructionStatus")
                    or row.get("saleStatus")
                    or row.get("remarks")
                    or row.get("sale_document_path")
                    or row.get("photo_paths")
                ):
                    continue

                db.session.execute(query, {
                    "project_id": data["project_id"],
                    "quarter": data["quarter"],
                    "plot_no": row.get("plotNo"),
                    "construction_status": row.get("constructionStatus"),
                    "sale_status": row.get("saleStatus"),
                    "remarks": row.get("remarks"),
                    "sale_document_path": row.get("sale_document_path"),
                    "photo_paths": json.dumps(row.get("photo_paths", []))
                })

            db.session.commit()
            return {"success": True}

        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": str(e)}