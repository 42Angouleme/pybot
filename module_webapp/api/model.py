from .api import api

from werkzeug.datastructures import FileStorage
from flask_restx import fields

create_user_parser = api.parser()
create_user_parser.add_argument(
    "picture", location="files", type=FileStorage, required=True
)
create_user_parser.add_argument(
    "name", type=str, help="The user name", location="form", required=True
)
create_user_parser.add_argument(
    "openai_chat_messages", type=str, help="The user chat history", location="form"
)

patch_user_parser = api.parser()
patch_user_parser.add_argument("picture", location="files", type=FileStorage)
patch_user_parser.add_argument("name", type=str, help="The user name", location="form")
patch_user_parser.add_argument(
    "openai_chat_messages", type=str, help="The user chat history", location="form"
)

api_user_model = api.model(
    "User",
    {
        "id": fields.Integer(readonly=True, description="The user unique identifier"),
        "name": fields.String(required=True, description="The user name"),
        "openai_chat_messages": fields.Raw(
            description="The user openai chat messages history"
        ),
        "created_at": fields.DateTime(description="User creation timestamp"),
    },
)

api_error_model = api.model(
    "Error",
    {
        "message": fields.String(description="Error message"),
    },
)
