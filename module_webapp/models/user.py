from typing import Optional
from module_webapp.app import db
from .image_model_preset import DrawingModel

UserId = int


class UserBase:
    name: str
    picture: bytes


class UserCreate(UserBase):
    pass


class UserPatch:
    name: Optional[str]
    picture: Optional[bytes]


class UserResponse(UserBase):
    id: UserId


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    # chat = db.Column(db.JSON)
    picture = db.Column(DrawingModel.as_mutable_json())
