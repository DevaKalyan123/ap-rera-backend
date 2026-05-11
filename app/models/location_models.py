from sqlalchemy import text
from app.models.database import db


class LocationModel:
    """
    LocationModel
    ----------------
    Uses RAW SQL queries for:
    - States
    - Districts
    - Mandals
    - Villages
    """

    # -----------------------------
    # GET ALL STATES
    # -----------------------------
    @staticmethod
    def get_states():
        query = text("""
            SELECT id, state_code, state_name
            FROM states_t
            ORDER BY state_name
        """)
        result = db.session.execute(query).fetchall()

        return [
            {"id": r.id, "state_code": r.state_code, "state_name": r.state_name}
            for r in result
        ]

    # -----------------------------
    # GET DISTRICTS BY STATE
    # -----------------------------
    @staticmethod
    def get_districts_by_state(state_id):
        query = text("""
            SELECT id, district_name
            FROM districts_t
            WHERE state_id = :state_id and id > 10
            ORDER BY district_name
        """)
        result = db.session.execute(query, {"state_id": state_id}).fetchall()

        return [
            {"id": r.id, "name": r.district_name}
            for r in result
        ]

    # -----------------------------
    # GET MANDALS BY DISTRICT
    # -----------------------------
    @staticmethod
    def get_mandals_by_district(district_id):
        query = text("""
            SELECT id, mandal_name
            FROM mandals_t
            WHERE district_id = :district_id
            ORDER BY mandal_name
        """)
        result = db.session.execute(query, {"district_id": district_id}).fetchall()

        return [
            {"id": r.id, "name": r.mandal_name}
            for r in result
        ]

    # -----------------------------
    # GET VILLAGES BY MANDAL
    # -----------------------------
    @staticmethod
    def get_villages_by_mandal(mandal_id):
        query = text("""
            SELECT id, village_code, village_name
            FROM villages_t
            WHERE mandal_id = :mandal_id
            ORDER BY village_name
        """)
        result = db.session.execute(query, {"mandal_id": mandal_id}).fetchall()

        return [
            {
                "id": r.id,
                "code": r.village_code,
                "name": r.village_name
            }
            for r in result
        ]

    # -----------------------------
    # VALIDATIONS (OPTIONAL)
    # -----------------------------
    @staticmethod
    def validate_district_state(district_id, state_id):
        query = text("""
            SELECT 1
            FROM districts_t
            WHERE id = :district_id
              AND state_id = :state_id
        """)
        return db.session.execute(
            query,
            {"district_id": district_id, "state_id": state_id}
        ).fetchone() is not None

    @staticmethod
    def validate_mandal_district(mandal_id, district_id):
        query = text("""
            SELECT 1
            FROM mandals_t
            WHERE id = :mandal_id
              AND district_id = :district_id
        """)
        return db.session.execute(
            query,
            {"mandal_id": mandal_id, "district_id": district_id}
        ).fetchone() is not None

    @staticmethod
    def validate_village_mandal(village_id, mandal_id):
        query = text("""
            SELECT 1
            FROM villages_t
            WHERE id = :village_id
              AND mandal_id = :mandal_id
        """)
        return db.session.execute(
            query,
            {"village_id": village_id, "mandal_id": mandal_id}
        ).fetchone() is not None
