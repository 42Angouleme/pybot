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


def create_app(root_dir: str = os.path.dirname(os.path.abspath(__file__))):
    """Create the flask application.

    Attributes:
        root_dir: The directory containing the `database` directory and the `users.db` file. Defaults to the current Python file.
    """

    STATIC_DIR = os.path.join(root_dir, "database")
    DATABASE_PATH = os.path.join(root_dir, "database/users.db")

    try:
        os.makedirs(STATIC_DIR)
    except FileExistsError:
        pass

    # Flask
    app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="/database")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_PATH}"

    # Login hardcoded password
    app.config["SECRET KEY"] = "hello"
    app.secret_key = "hello"

    # Static media storage with sqlalchemy_media
    StoreManager.register(
        "fs",
        functools.partial(FileSystemStore, STATIC_DIR, "/database"),
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
