import os
import functools
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_media import (
    StoreManager,
    FileSystemStore,
)

db = SQLAlchemy()

from .views import admin_bp, frontend_bp
from .api import api_bp


def create_app():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    """The directory containing the current Python file as the root directory"""

    STATIC_DIR = os.path.join(ROOT_DIR, "static")
    DATABASE_PATH = os.path.join(ROOT_DIR, "database.db")

    # Flask
    app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="/static")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_PATH}"

    # Login hardcoded password
    app.config["SECRET KEY"] = "hello"
    app.secret_key = "hello"

    # Static media storage with sqlalchemy_media
    StoreManager.register(
        "fs",
        functools.partial(FileSystemStore, STATIC_DIR, "/static"),
        default=True,
    )

    # Database
    db.init_app(app)
    with app.app_context():
        db.create_all()  # ensure db table creation as defined by our models

    # Blueprints
    app.register_blueprint(api_bp)  # prefix '/api' is already included
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(frontend_bp)

    return app
