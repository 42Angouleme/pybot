from ..app import db, StoreManager
from . import User, DrawingModel


class UserDAO(object):
    def getAll(self):
        return User.query.all()

    def get(self, id):
        return User.query.get_or_404(id)

    def create(self, user):
        with StoreManager(db.session):
            file = user["file"]
            img = DrawingModel.create_from(file)
            new_user = User(name=user["name"], picture=img)
            db.session.add(new_user)
            db.session.commit()
            db.session.refresh(new_user)
            return new_user

    def update(self, id, data):
        user = User.query.get_or_404(id)
        if "name" in data:
            user.name = data.name
            # TODO
        db.session.commit()
        db.session.refresh(user)
        return user

    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()


user = UserDAO()
