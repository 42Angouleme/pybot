from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    redirect,
    current_app,
    session,
    abort,
)
from sqlalchemy_media import StoreManager
from pybot.module_webapp.dao import user
from pybot.module_webapp.app import db
from functools import wraps

import json

admin_bp = Blueprint("admin", __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not "user" in session or not session["user"]["admin"]:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@admin_bp.route("/list")
@login_required
def list_page():
    name = request.args.get("name")
    users = user.search(name) if name else user.getAll()
    with StoreManager(db.session):
        return render_template("admin/list.html", users=users)


@admin_bp.route("/login")
def login():
    return render_template("admin/login.html")


@admin_bp.route("/login", methods=["POST"])
def login_post():
    password = request.form["password"]
    if password != current_app.secret_key:
        return render_template("admin/login.html", log=True)
    else:
        session["user"] = {"admin": True}
        return render_template("admin/index.html")


@admin_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("admin.login"))


@admin_bp.route("/")
@login_required
def index():
    return render_template("admin/index.html")


@admin_bp.route("/search")
@login_required
def search_page():
    return render_template("admin/search.html")


@admin_bp.route("/add")
@login_required
def add_page():
    return render_template("admin/add.html")


# @admin_bp.route("/record/<time>")
# def record_audio(time):
#    if time.isdigit():
#        # relevant code for registering audio
#        return "recording..."
#    return "Invalid arguments"


@admin_bp.route("/profile/<int:id>")
def profile_page(id):
    with StoreManager(db.session):
        u = user.get(id)
        if u is None:
            abort(404, description="User not found")
        return render_template(
            "admin/edit.html", user=u
        )
