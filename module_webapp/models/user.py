from ..app import db
from .image_model_preset import DrawingModel


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    picture = db.Column(DrawingModel.as_mutable_json())
