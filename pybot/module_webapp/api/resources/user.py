from flask_restx import Resource
from flask_restx.api import HTTPStatus
from sqlalchemy_media.exceptions import ValidationError, AnalyzeError
from sqlalchemy.exc import IntegrityError

from pybot.module_webapp.dao import user

from ..api import api

from pybot.module_webapp.models import UserId

from sqlalchemy.exc import NoResultFound

from jsonschema.exceptions import ValidationError as JsonSchemaValidationError
from ..model import (
    create_user_parser,
    patch_user_parser,
    api_user_model,
    api_error_model,
)

import json

ns = api.namespace("users", description="USER operations")


@ns.errorhandler(ValidationError)
@ns.errorhandler(AnalyzeError)
@ns.errorhandler(JsonSchemaValidationError)
@ns.errorhandler(json.JSONDecodeError)
@ns.errorhandler(IntegrityError)
@ns.marshal_with(api_error_model, code=HTTPStatus.BAD_REQUEST)
def handle_bad_request_exception(error):
    """This is a custom error"""
    return {"message": error}, HTTPStatus.BAD_REQUEST


@ns.errorhandler(NoResultFound)
@ns.marshal_with(api_error_model, code=HTTPStatus.NOT_FOUND)
def handle_NoResultFound_exception(error):
    """This is a custom error"""
    return {"message": error}, HTTPStatus.NOT_FOUND


@ns.route("/")
class UserList(Resource):
    """Shows a list of all users, and lets you POST to add new users"""

    @ns.doc("list_users")
    @ns.marshal_list_with(api_user_model)
    def get(self):
        """List all users"""
        return user.getAll()

    @ns.doc("create_user")
    @ns.expect(create_user_parser)
    @ns.marshal_with(api_user_model, code=HTTPStatus.CREATED)
    @ns.response(
        code=HTTPStatus.BAD_REQUEST, description="Bad Request", model=api_error_model
    )
    def post(self):
        """Create a new user"""
        args = create_user_parser.parse_args()
        data = user.create(args)
        return data, HTTPStatus.CREATED


@ns.route("/<int:id>")
@ns.response(HTTPStatus.NOT_FOUND, "User not found")
@ns.param("id", "The user identifier")
class UserResource(Resource):
    """Show a single user item and lets you delete and patch them"""

    @ns.doc("get_user")
    @ns.response(HTTPStatus.OK, "User fetched")
    @ns.marshal_with(api_user_model)
    @ns.response(
        code=HTTPStatus.NOT_FOUND, description="Not Found", model=api_error_model
    )
    def get(self, id: UserId):
        """Fetch a given resource"""

        fetched_user = user.get(id)
        return fetched_user

    @ns.doc("delete_user")
    @ns.response(HTTPStatus.OK, "User deleted")
    @ns.marshal_with(api_user_model)
    @ns.response(
        code=HTTPStatus.NOT_FOUND, description="Not Found", model=api_error_model
    )
    def delete(self, id: UserId):
        """Delete a user given its identifier"""
        deleted_user = user.delete(id)
        return deleted_user

    @ns.doc("update_user")
    @ns.expect(patch_user_parser)
    @ns.response(HTTPStatus.OK, "User updated")
    @ns.marshal_with(api_user_model)
    @ns.response(
        code=HTTPStatus.BAD_REQUEST, description="Bad Request", model=api_error_model
    )
    @ns.response(
        code=HTTPStatus.NOT_FOUND, description="Not Found", model=api_error_model
    )
    def patch(self, id: UserId):
        """Update a user given its identifier"""
        patch = patch_user_parser.parse_args()
        updated_user = user.update(id, patch)
        return updated_user, HTTPStatus.OK
