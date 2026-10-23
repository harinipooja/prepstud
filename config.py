import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-placement-prep-secret-key")
    # Use "mysql" (default) or "sqlite" for quick local demo without MySQL
    DB_ENGINE = os.getenv("DB_ENGINE", "mysql").lower()

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "placement_prep")

    if DB_ENGINE == "sqlite":
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'placement_prep.db'}"
    else:
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
