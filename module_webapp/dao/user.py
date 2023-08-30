from sqlalchemy.exc import IntegrityError
from module_webapp.app import db, StoreManager
from module_webapp.models import (
    User,
    DrawingModel,
    UserCreate,
    UserResponse,
    UserPatch,
    UserId,
)
from sqlalchemy.exc import NoResultFound
import json
from jsonschema import validate
from typing import List

openai_chat_messages_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "role": {
                "type": "string",
                "enum": ["system", "user", "assistant", "function"],
            },
            "content": {"type": ["string", "null"]},
            "name": {"type": "string", "maxLength": 64, "pattern": "^[a-zA-Z0-9_]+$"},
            "function_call": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "arguments": {"type": "string"},
                },
                "required": ["name", "arguments"],
                "additionalProperties": False,
            },
        },
        "required": ["role", "content"],
    },
}
"""The json schema allowed for openai chat messages object as described at https://platform.openai.com/docs/api-reference/chat/create#messages. Note, the schema is not restrictive enough if you read the spec carrefully but that's enough for now."""


def parse_openai_chat_messages(user: User):
    """If the user has openai_chat_messages property, convert it from string to JSON, then validate the JSON schema and reassign the property as dict."""
    if user.openai_chat_messages:
        user.openai_chat_messages = json.loads(user.openai_chat_messages)
        validate(user.openai_chat_messages, openai_chat_messages_schema)


def raise_NoResultFound_if_none(user, id):
    if user is None:
        raise NoResultFound(f"User with ID {id} not found.")


class UserDAO(object):
    """User Data Access Object to manipulates `User` with CRUD-like methods."""

    def getAll(self) -> List[UserResponse]:
        """
        Get all users.
        """
        return User.query.all()

    def get(self, id: UserId) -> UserResponse:
        """Get one user by ID.

        Keyword arguments:
        id -- The user ID.
        """
        user = User.query.get(id)
        raise_NoResultFound_if_none(user, id)
        if user.openai_chat_messages:
            user.openai_chat_messages = json.loads(user.openai_chat_messages)
        return user

    def create(self, user: UserCreate) -> UserResponse:
        """Create a new user.

        Keyword arguments:
        user -- The user fields dictionary.
        """
        with StoreManager(db.session):
            file = user["picture"]
            picture = DrawingModel.create_from(file)
            picture.get_thumbnail(width=48, auto_generate=True)
            new_user = User(**(user | {"picture": picture}))
        parse_openai_chat_messages(new_user)
        db.session.add(new_user)
        db.session.commit()
        # refetch the user from the db for the response to include the generated ID
        db.session.refresh(new_user)
        return new_user

    def update(self, id: UserId, user_patch: UserPatch) -> UserResponse:
        """Update the fields of the user with corresponding ID.

        Keyword arguments:
        id -- The user ID.
        userPatch -- The patch data.
        """
        user = User.query.get(id)
        raise_NoResultFound_if_none(user, id)

        if "picture" in user_patch:
            if user_patch["picture"] is not None:
                with StoreManager(db.session, delete_orphan=True):
                    user.picture = DrawingModel.create_from(user_patch["picture"])
                    user.picture.get_thumbnail(width=48, auto_generate=True)
            del user_patch["picture"]

        parse_openai_chat_messages(user_patch)
        # apply the patch to the user object we just fetched
        for key, value in user_patch.items():
            if value is not None:
                setattr(user, key, value)

        db.session.commit()
        db.session.refresh(user)
        return user

    def delete(self, id: UserId) -> UserResponse:
        """Delete the user with corresponding ID.

        Keyword arguments:
        id -- The user ID.
        """
        user = User.query.get(id)
        raise_NoResultFound_if_none(user, id)
        db.session.delete(user)
        db.session.commit()
        return user

    def search(self, first_name: str) -> List[UserResponse]:
        return User.query.filter(User.first_name.like(f"%{first_name}%")).all()


user = UserDAO()
"""A ready to use User Data Access Object instance."""
