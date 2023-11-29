from sqlalchemy_media import ImageProcessor, ImageValidator

from .image import image_model_factory

DrawingModel = image_model_factory(
    ImageValidator(
        minimum=(20, 20),
        maximum=(4000, 4000),
        min_aspect_ratio=0.8,
        content_types=["image/jpeg", "image/png"],
    ),
    ImageProcessor(fmt="png"),
)
"""A preconfigured sqlalchemy_media `Image` class. Performs image validation and resizing."""
