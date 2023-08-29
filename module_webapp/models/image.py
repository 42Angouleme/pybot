from flask import Flask, render_template, url_for, jsonify
from flask_restx import Api, Resource, fields, reqparse
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import os
import io
from sqlalchemy_media import (
    StoreManager,
    FileSystemStore,
    Image,
    ImageAnalyzer,
    ImageValidator,
    ImageProcessor,
)
from flask_restx.apidoc import apidoc
import functools
from sqlalchemy_media.exceptions import ValidationError


import json

from sqlalchemy import TypeDecorator, Unicode


class Json(TypeDecorator):
    impl = Unicode

    def process_bind_param(self, value, engine):
        return json.dumps(value)

    def process_result_value(self, value, engine):
        if value is None:
            return None

        return json.loads(value)


def image_model_factory(validator=ImageValidator(), processor=ImageProcessor()):
    class ImageModel(Image):
        __pre_processors__ = [
            ImageAnalyzer(),
            validator,
            processor,
        ]

        @staticmethod
        def as_mutable_json():
            return ImageModel.as_mutable(Json)

    return ImageModel
