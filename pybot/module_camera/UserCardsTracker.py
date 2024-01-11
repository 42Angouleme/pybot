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

    def draw(self, frame: MatLike, min_threshold=0.75, stop_threshold=0.85) -> Tuple[MatLike, List[UserResponse]]:
        """
        Params
            - frame: 2D Frame of the card detected
            - min_threshold: Sufficient threshold to interpret frame as similar card
            - stop_threshold: Threshold to interpret frame as corresponding card
        Returns
            Tuple:
                - frame: with card framed detected card
                - user found that matches the most
        """

        """Find the matching user cards in the given `frame`. Highlighted the card contours and write their name next to it. Also return the array of matching users."""
        # Convert pygame.surface -> np_array
        frame = pg.surfarray.array3d(frame)
        contours, candidate_images = scan(
            frame.copy(),
            keep_results=[
                card_contours_transform,
                rotate_top_left_corner_low_density_transform,
            ],
        )
        frame = cv2.drawContours(frame, contours, -1, (0, 255, 255), 3)
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
