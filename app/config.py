import os
from dotenv import load_dotenv

# =========================================
# LOAD ENV VARIABLES
# =========================================

load_dotenv()

# =========================================
# BASE DIRECTORY
# =========================================

BASE_DIR = os.path.abspath(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

# =========================================
# BOOLEAN HELPER
# =========================================

def str_to_bool(value, default=False):

    if value is None:
        return default

    return value.lower() in (
        "true",
        "1",
        "yes"
    )

# =========================================
# CONFIG CLASS
# =========================================

class Config:

    # =====================================
    # FLASK
    # =====================================

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-secret-key"
    )

    DEBUG = str_to_bool(
        os.getenv("FLASK_DEBUG"),
        False
    )

    PORT = int(
        os.getenv("PORT", 8080)
    )

    # =====================================
    # CORS
    # =====================================

    ALLOWED_ORIGINS = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173,"
        "http://127.0.0.1:5173,"
        "https://ap-rera-frontend.vercel.app"
    )

    # =====================================
    # DATABASE
    # =====================================

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if not SQLALCHEMY_DATABASE_URI:

        raise RuntimeError(
            "DATABASE_URL is not set"
        )

    # =====================================
    # RESEND EMAIL CONFIG
    # =====================================

    RESEND_API_KEY = os.getenv(
        "RESEND_API_KEY"
    )

    FROM_EMAIL = os.getenv(
        "FROM_EMAIL",
        "onboarding@resend.dev"
    )

    # =====================================
    # PUBLIC URL
    # =====================================

    PUBLIC_BASE_URL = os.getenv(
        "PUBLIC_BASE_URL"
    )

    # =====================================
    # FILE UPLOADS
    # =====================================

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "app",
        "uploads",
        "complint_doc"
    )

# =========================================
# CREATE UPLOAD FOLDER
# =========================================

os.makedirs(
    Config.UPLOAD_FOLDER,
    exist_ok=True
)