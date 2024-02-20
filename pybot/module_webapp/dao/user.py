from sqlalchemy.exc import IntegrityError
from pybot.module_webapp.app import db, StoreManager
from pybot.module_webapp.models import (
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


def raise_NoResultFound_if_none(user, id):
    if user is None:
        raise NoResultFound(f"User with ID {id} not found.")


class UserDAO(object):
    """User Data Access Object to manipulates `User` with CRUD-like methods."""

    def getAll(self) -> List[UserResponse]:
        """
        Get all users.
        """
        tab = User.query.all()
        for t in tab:
            with StoreManager(db.session):
                t.picture_path = t.picture.locate()
        return tab

    def get(self, id: UserId) -> UserResponse:
        """Get one user by ID.

        Keyword arguments:
        id -- The user ID.
        """
        user = User.query.get(id)
        raise_NoResultFound_if_none(user, id)
        print(user)
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
        with StoreManager(db.session, delete_orphan=True):
            user = User.query.get(id)
            raise_NoResultFound_if_none(user, id)

            if "picture" in user_patch:
                if user_patch["picture"] is not None:
                    # TODO handle error when img is invalid, AttributeError: 'StreamDescriptor' object has no attribute 'readline'
                    user.picture = DrawingModel.create_from(user_patch["picture"])
                    user.picture.get_thumbnail(width=48, auto_generate=True)
                del user_patch["picture"]

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
        with StoreManager(db.session, delete_orphan=True):
            user = User.query.get(id)
            raise_NoResultFound_if_none(user, id)
            db.session.delete(user)
            db.session.commit()
            return user

    def search(self, first_name: str) -> List[UserResponse]:
        return User.query.filter(User.first_name.like(f"%{first_name}%")).all()


user = UserDAO()
"""A ready to use User Data Access Object instance."""
