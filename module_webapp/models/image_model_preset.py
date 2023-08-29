from .image import image_model_factory
from sqlalchemy_media import (
    StoreManager,
    FileSystemStore,
    Image,
    ImageAnalyzer,
    ImageValidator,
    ImageProcessor,
)

DrawingModel = image_model_factory(
    ImageValidator(
        minimum=(80, 80),
        maximum=(900, 900),
        min_aspect_ratio=0.8,
        content_types=["image/jpeg", "image/png"],
    ),
    ImageProcessor(fmt="png", width=400),
)
