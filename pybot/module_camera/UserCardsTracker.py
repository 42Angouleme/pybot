from cardscan import (
    scan,
    card_contours_transform,
    rotate_top_left_corner_low_density_transform,
)
from ..module_webapp.dao import user
from ..module_webapp.app import db
import cv2
import os
from cv2.typing import MatLike
from typing import List, Tuple

from sqlalchemy_media import StoreManager
from .compare_images import ImageComparator
from flask import Flask

from ..module_webapp.models.user import UserResponse

import pygame as pg


class UserCardsTracker:
    def __init__(self, app: Flask):
        self.users, user_image_paths = self._get_users_info(app)
        self.image_comparator = ImageComparator(user_image_paths)

    @staticmethod
    def _get_users_info(app: Flask):
        """Fetch the db users and return 2 arrays, the user formatted names, and the users picture path. Both in the same order."""
        with app.app_context():
            users = user.getAll()
            with StoreManager(db.session):
                img_paths = [
                    os.path.join(app.static_folder, user.picture.path) for user in users
                ]
        return users, img_paths

    @staticmethod
    def _get_user_fullname(u: UserResponse) -> str:
        return f"{u.first_name} {u.last_name}"

    def get_detected_card(self, frame: MatLike, min_threshold, stop_threshold) -> Tuple[MatLike, MatLike]:
        """
            Find cards in the given `frame`.
            Highlighted the cards contours.

            Params
                - frame: 2D Frame
                - min_threshold: Sufficient threshold to interpret frame as similar card
                - stop_threshold: Threshold to interpret frame as corresponding card
            Returns
                Tuple:
                    - frame: with card framed detected card
                    - card detected as image
        """
        # Convert pygame.surface -> np_array
        frame = pg.surfarray.array3d(frame)
        # Returns array of images in frame that seems to be a card
        contours, candidate_images = scan(
            frame.copy(),
            keep_results=[
                card_contours_transform,
                rotate_top_left_corner_low_density_transform,
            ],
        )
        frame = cv2.drawContours(frame, contours, -1, (0, 255, 255), 3)
        card_detected = None
        for candidate_idx, candidate_img in enumerate(candidate_images):
            user_idx = self.image_comparator.get_match_idx(
                    candidate_img,
                    min_threshold,
                    stop_threshold)
            if user_idx is not None:
                continue
            # Store only card that does not match any user card
            card_detected = candidate_img

        # convert np_array -> pyagame_surface
        frame = pg.surfarray.make_surface(frame)
        if card_detected is not None:
            # Perform image manip to get same image as real one
            card_detected = cv2.flip(card_detected, 0)
            M = cv2.getRotationMatrix2D(center=(100, 100), angle=-90, scale=1.0)
            card_detected = cv2.warpAffine(card_detected, M, (200, 200))
            # convert np_array -> pyagame_surface
            card_detected = pg.surfarray.make_surface(card_detected)
        return frame, card_detected

    def get_detected_user(self, frame: MatLike, min_threshold, stop_threshold) -> Tuple[MatLike, List[UserResponse]]:
        """
        Find the matching user cards in the given `frame`.
        Highlighted the card contours.

        Params
            - frame: 2D Frame
            - min_threshold: Sufficient threshold to interpret frame as similar card
            - stop_threshold: Threshold to interpret frame as corresponding card
        Returns
            Tuple:
                - frame: with card framed detected card
                - user found that matches the most
        """
        # Convert pygame.surface -> np_array
        frame = pg.surfarray.array3d(frame)
        # Returns array of images in frame that seems to be a card
        contours, candidate_images = scan(
            frame.copy(),
            keep_results=[
                card_contours_transform,
                rotate_top_left_corner_low_density_transform,
            ],
        )
        frame = cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
        user_match = None
        for candidate_idx, candidate_img in enumerate(candidate_images):
            user_idx = self.image_comparator.get_match_idx(candidate_img, min_threshold, stop_threshold)
            if user_idx is None:
                continue
            u = self.users[user_idx]
            user_match = u
            #       --  Text handling  --
            #   Issue: Text written vertically

            # contour = contours[candidate_idx]
            # text = self._get_user_fullname(u)
            # font = cv2.FONT_HERSHEY_SIMPLEX
            # bottom_left = max(contour, key=lambda edge: edge[0][0])[0]
            # text_size = cv2.getTextSize(text, font, 0.7, 2)[0]
            # textY = bottom_left[1] - 10
            # textX = bottom_left[0] - text_size[0] // 2
            # text_pos = (textX, textY)
            # cv2.putText(
            #   img=frame,
            #   text=text,
            #   org=text_pos,
            #   fontFace=font,
            #   fontScale=0.7,
            #   color=(200, 0, 255, 127),
            #   thickness=2,
            #   lineType=cv2.LINE_AA,
            #   bottomLeftOrigin=True)

        # convert np_array -> pyagame_surface
        frame = pg.surfarray.make_surface(frame)
        return frame, user_match
