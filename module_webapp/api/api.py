from flask import Blueprint
from flask_restx import Api

api_bp = Blueprint("api", __name__)

api = Api(
    api_bp,
    version="1.0",
    title="Sample API",
    description="A sample API with Swagger",
    prefix="/api",
    doc="/api/doc",
)

from .resources import user
