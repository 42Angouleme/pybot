import os
import functools
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_media import (
    StoreManager,
    FileSystemStore,
)

db = SQLAlchemy()

from .views import frontend_bp
from .api import api_bp


def create_app():
    # Flask
    app = Flask(__name__, static_folder="../static", static_url_path="/static")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

    # Static media storage with sqlalchemy_media
    WORKING_DIR = os.path.abspath(os.getcwd())
    TEMP_PATH = os.path.join(WORKING_DIR, "static")
    StoreManager.register(
        "fs",
        functools.partial(FileSystemStore, TEMP_PATH, "/static"),
        default=True,
    )

    # Database
    db.init_app(app)
    with app.app_context():
        db.create_all()  # ensure db table creation as defined by our models

    # Blueprints
    app.register_blueprint(api_bp)
    app.register_blueprint(frontend_bp)

    return app
