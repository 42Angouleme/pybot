from sqlalchemy_media import ImageProcessor, ImageValidator

from .image import image_model_factory

DrawingModel = image_model_factory(
    ImageValidator(
        minimum=(80, 80),
        maximum=(900, 900),
        min_aspect_ratio=0.8,
        content_types=["image/jpeg", "image/png"],
    ),
    ImageProcessor(fmt="png", width=400),
)
"""A preconfigured sqlalchemy_media `Image` class. Performs image validation and resizing."""
