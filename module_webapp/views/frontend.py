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
from module_webapp.dao import user
from module_webapp.app import db
from functools import wraps
from module_webapp.models import User

import json

frontend_bp = Blueprint("frontend", __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not "user" in session or not session["user"]["admin"]:
            return redirect(url_for("frontend.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@frontend_bp.route("/list")
@login_required
def list_page():
    name = request.args.get("name")
    users = user.search(name) if name else user.getAll()
    with StoreManager(db.session):
        return render_template("list.html", users=users)


@frontend_bp.route("/login")
def login():
    return render_template("login.html")


@frontend_bp.route("/login", methods=["POST"])
def login_post():
    password = request.form["password"]
    if password != current_app.secret_key:
        return render_template("login.html", log=True)
    else:
        session["user"] = {"admin": True}
        return render_template("index.html")


@frontend_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("frontend.login"))


@frontend_bp.route("/")
@login_required
def index():
    return render_template("index.html")


@frontend_bp.route("/search")
@login_required
def result_page():
    return render_template("search.html")


@frontend_bp.route("/add")
@login_required
def add_page():
    return render_template("add.html")


# @frontend_bp.route("/record/<time>")
# def record_audio(time):
#    if time.isdigit():
#        # relevant code for registering audio
#        return "recording..."
#    return "Invalid arguments"


@frontend_bp.route("/edit/<int:id>")
def profile_page(id):
    with StoreManager(db.session):
        u = user.get(id)
        if u is None:
            abort(404, description="User not found")
        return render_template(
            "edit.html",
            user=u,
            openai_chat_messages=json.dumps(u.openai_chat_messages, indent=2),
        )
