from typing import Optional

from sqlalchemy.engine import create
from module_webapp.app import db
from .image_model_preset import DrawingModel
from datetime import datetime

UserId = int
"""Type for the User ID"""


class UserBase:
    name: str
    picture: bytes
    chat: dict


class UserCreate(UserBase):
    pass


class UserPatch:
    name: Optional[str]
    picture: Optional[bytes]
    chat: Optional[dict]


class UserResponse(UserBase):
    id: UserId
    created_at: datetime


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    chat = db.Column(db.JSON)
    picture = db.Column(DrawingModel.as_mutable_json())
