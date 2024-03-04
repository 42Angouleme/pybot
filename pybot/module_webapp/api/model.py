from .api import api

from werkzeug.datastructures import FileStorage
from flask_restx import fields

create_user_parser = api.parser()
create_user_parser.add_argument(
    "picture", location="files", type=FileStorage, required=True
)
create_user_parser.add_argument(
    "first_name", type=str, help="The user first name", location="form", required=True
)
create_user_parser.add_argument(
    "last_name", type=str, help="The user last name", location="form", required=True
)
create_user_parser.add_argument(
    "conversation_summary", type=str, help="The user chat history", location="form"
)

patch_user_parser = api.parser()
patch_user_parser.add_argument("picture", location="files", type=FileStorage)
patch_user_parser.add_argument(
    "first_name", type=str, help="The user first name", location="form"
)
patch_user_parser.add_argument(
    "last_name", type=str, help="The user last name", location="form"
)
patch_user_parser.add_argument(
    "conversation_summary", type=str, help="The user chat history", location="form"
)

api_user_model = api.model(
    "User",
    {
        "id": fields.Integer(readonly=True, description="The user unique identifier"),
        "first_name": fields.String(required=True, description="The user first name"),
        "last_name": fields.String(required=True, description="The user last name"),
        "conversation_summary": fields.String(required=False, description="The user openai chat messages history"),
        "created_at": fields.DateTime(description="User creation timestamp"),
    },
)

api_error_model = api.model(
    "Error",
    {
        "message": fields.String(description="Error message"),
    },
)

img_parser = api.parser()
img_parser.add_argument("image", location="files", type=FileStorage)

img_model = api.model(
    "Image",
    {
        "card": fields.Raw(description="Card image file"),
    },
)
