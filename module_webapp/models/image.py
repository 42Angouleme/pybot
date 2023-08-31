import json
from sqlalchemy import TypeDecorator, Unicode
from sqlalchemy_media import Image, ImageAnalyzer, ImageProcessor, ImageValidator


class Json(TypeDecorator):
    impl = Unicode

    def process_bind_param(self, value, engine):
        return json.dumps(value)

    def process_result_value(self, value, engine):
        if value is None:
            return None

        return json.loads(value)


def image_model_factory(validator=ImageValidator(), processor=ImageProcessor()):
    """A wrapper around sqlalchemy_media `Image` class."""

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
