from sqlalchemy import text
from app.models.database import db

class TestConnectionModel:

    @staticmethod
    def insert(name):
        query = text("""
            INSERT INTO test_connection (name)
            VALUES (:name)
            RETURNING id, name
        """)
        result = db.session.execute(query, {"name": name})
        db.session.commit()
        return result.fetchone()

    @staticmethod
    def fetch_all():
        query = text("""
            SELECT id, name, created_at
            FROM test_connection
            ORDER BY id DESC
        """)
        result = db.session.execute(query)
        return result.fetchall()
