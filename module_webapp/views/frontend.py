from flask import Blueprint, render_template
from sqlalchemy_media import StoreManager
from module_webapp.dao import user
from module_webapp.app import db

frontend_bp = Blueprint("frontend", __name__)


@frontend_bp.route("/list")
def list_page():
    with StoreManager(db.session):
        return render_template("list.html", users=user.getAll())
