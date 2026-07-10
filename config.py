import os
import urllib.parse

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "chave-secreta-rh-2026-change-me")

    # Se DATABASE_URL estiver definido (producao), usa ele
    # Senao, usa SQLite local para desenvolvimento
    database_url = os.environ.get("DATABASE_URL")

    if database_url:
        # PostgreSQL em producao (Railway, etc)
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # SQLite local para desenvolvimento
        db_path = os.path.join(basedir, "instance", "rh.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    } if database_url else {}


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}