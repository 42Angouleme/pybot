from flask_restx import Resource
from sqlalchemy_media.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError

from module_webapp.dao import user

from werkzeug.datastructures import FileStorage
from flask_restx import fields
from ..api import api

ns = api.namespace("users", description="USER operations")

create_user_parser = api.parser()
create_user_parser.add_argument(
    "picture", location="files", type=FileStorage, required=True
)
create_user_parser.add_argument("name", type=str, help="Some param", location="form")

api_user_model = api.model(
    "User",
    {
        "id": fields.Integer(readonly=True, description="The user unique identifier"),
        "name": fields.String(required=True, description="The student name"),
    },
)


@ns.route("/")
class UserList(Resource):
    """Shows a list of all users, and lets you POST to add new users"""

    @ns.doc("list_users")
    @ns.marshal_list_with(api_user_model)
    def get(self):
        """List all users"""
        return user.getAll()

    @ns.doc("create_user")
    @api.expect(create_user_parser)
    @api.response(400, "Bad request")
    @ns.marshal_with(api_user_model, code=201)
    def post(self):
        """Create a new user"""
        args = create_user_parser.parse_args()
        try:
            data = user.create(args)
            return data, 201
        except ValidationError as e:
            api.abort(400, e)
        except IntegrityError as e:
            api.abort(400, "Integrity constraint violation.")


@ns.route("/<int:id>")
@ns.response(404, "User not found")
@ns.param("id", "The user identifier")
class UserResource(Resource):
    """Show a single user item and lets you delete and patch them"""

    @ns.doc("get_user")
    @ns.response(200, "User fetched")
    @ns.marshal_with(api_user_model)
    def get(self, id):
        """Fetch a given resource"""
        fetched_user = user.get(id)
        if fetched_user is None:
            api.abort(404, f"User with ID {id} not found.")
        return fetched_user

    @ns.doc("delete_user")
    @ns.response(200, "User deleted")
    @ns.marshal_with(api_user_model)
    def delete(self, id):
        """Delete a user given its identifier"""
        deleted_user = user.delete(id)
        if deleted_user is None:
            api.abort(404, f"User with ID {id} not found. Can't deleted.")
        return deleted_user

    @ns.doc("update_user")
    @ns.expect(api_user_model)
    @ns.response(200, "User updated")
    @ns.marshal_with(api_user_model)
    def patch(self, id):
        """Update a user given its identifier"""
        updated_user = user.update(id, api.payload)
        if updated_user is None:
            api.abort(404, f"User with ID {id} not found. Can't update.")
        return updated_user, 200
