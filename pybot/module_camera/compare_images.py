from skimage.metrics import structural_similarity as ssim
import cv2
from cv2.typing import MatLike
from typing import List, Tuple

import logging

_warning = logging.getLogger("CompareImage").warning
"""Custom Logger warning function. Print a message only shown when DEBUG mode is activated."""


class ImageComparator:
    def __init__(self, paths: List[str], compare_size=(64, 64)):
        self.compare_size = compare_size
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

    def get_match_idx(self, frame: MatLike, min_threshold=0.75, stop_threshold=0.85) -> int | None:
        """
        Params
            - frame: 2D Frame of the card detected
            - min_threshold: Sufficient threshold to interpret frame as similar card
            - stop_threshold: Threshold to interpret frame as corresponding card
        Returns
            - index of the item in `self.ref_images` matching `frame`.
            - None if no image satisfy the tolerance threshold.
        """
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        small_frame_gray = cv2.resize(frame_gray, self.compare_size)
        best_score = (None, 0.0)
        for i, ref_image in enumerate(self.ref_images):
            if ref_image is None:
                continue
            similarity = ssim(small_frame_gray, ref_image)
            if similarity >= stop_threshold:
                return i
            elif similarity >= min_threshold:
                if similarity > best_score[1]:
                    best_score = (i, similarity)
        return best_score[0]
