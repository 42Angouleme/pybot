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


def raise_NoResultFound_if_none(user, id):
    if user is None:
        raise NoResultFound(f"User with ID {id} not found.")


class UserDAO(object):
    """User Data Access Object to manipulates `User` with CRUD-like methods."""

    def getAll(self) -> UserResponse:
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
        return user

    def create(self, user: UserCreate) -> UserResponse:
        """Create a new user.

        Keyword arguments:
        user -- The user fields dictionary.
        """
        with StoreManager(db.session):
            file = user["picture"]
            img = DrawingModel.create_from(file)
            new_user = User(**(user | {"picture": img}))
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
                with StoreManager(db.session):
                    user.picture = DrawingModel.create_from(user_patch["picture"])
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
        user = User.query.get(id)
        raise_NoResultFound_if_none(user, id)
        db.session.delete(user)
        db.session.commit()
        return user


user = UserDAO()
"""A ready to use User Data Access Object instance."""
