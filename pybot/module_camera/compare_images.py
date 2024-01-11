from skimage.metrics import structural_similarity as ssim
import cv2
from cv2.typing import MatLike
from typing import List, Tuple

import logging

_warning = logging.getLogger("CompareImage").warning
"""Custom Logger warning function. Print a message only shown when DEBUG mode is activated."""


class ImageComparator:
    def __init__(self, paths: List[str], compare_size=(64, 64), sim_min_thresholds=(0.8, 0.85)):
        self.compare_size = compare_size
        # Thresholds for interprating as: [0] partial or [1] perfect match
        self.sim_min_thresholds = sim_min_thresholds
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
        best_score = (None, 0.0)
        for i, ref_image in enumerate(self.ref_images):
            if ref_image is None:
                continue
            similarity = ssim(small_frame_gray, ref_image)
            if similarity > self.sim_min_thresholds[1]:
                return i
            elif similarity > self.sim_min_thresholds[0]:
                if similarity > best_score[1]:
                    best_score = (i, similarity)
        return best_score[0]
