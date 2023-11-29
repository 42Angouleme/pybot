from skimage.metrics import structural_similarity as ssim
import cv2
from cv2.typing import MatLike
from typing import List, Tuple

import logging

_warning = logging.getLogger("CompareImage").warning
"""Custom Logger warning function. Print a message only shown when DEBUG mode is activated."""


class ImageComparator:
    def __init__(self, paths: List[str], compare_size=(64, 64), sim_min_threshold=0.8):
        self.compare_size = compare_size
        self.sim_min_threshold = sim_min_threshold
        self.ref_images: List[MatLike] = self._prepare_comparison_img(
            paths, compare_size
        )

    @staticmethod
    def _prepare_comparison_img(
        paths: List[str], size: Tuple[int, int]
    ) -> List[MatLike]:
        """Load the picture for comparison. Resize and grayscale."""
        imgs = []
        for path in paths:
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                img = cv2.resize(img, size)
            else:
                _warning(f"Image at path {path} failed to load.")
            imgs.append(img)
        return imgs

    def get_match_idx(self, frame: MatLike) -> int | None:
        """Return the index of the item in `self.ref_images` matching `frame`. None if no image satisfy the tolerance threshold."""
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        small_frame_gray = cv2.resize(frame_gray, self.compare_size)
        for i, ref_image in enumerate(self.ref_images):
            if ref_image is None:
                continue
            similarity = ssim(small_frame_gray, ref_image)
            if similarity > self.sim_min_threshold:
                return i
        return None
