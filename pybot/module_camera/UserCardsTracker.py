from cardscan import (
    scan,
    card_contours_transform,
    rotate_top_left_corner_low_density_transform,
)
import cv2
import os
from cv2.typing import MatLike
from typing import List, Tuple

from . import ImageComparator


class UserCardsTracker:
    def __init__(self):
        self.users, user_image_paths = self._get_users_info()
        self.image_comparator = ImageComparator(user_image_paths)

    @staticmethod
    def _get_users_info():
        # read all the cards and extract their names as users
        users = ['bob', 'joe', 'tom', 'toto']
        path = os.getcwd() + "/pybot/cards/"
        img_paths = [path + "bob.png", path + "joe.png",
                     path + "tom.png", path + "toto.png"]
        return users, img_paths

    # @staticmethod
    # def _get_user_fullname(u: UserResponse) -> str:
    #     return f"{u.first_name} {u.last_name}"

    def get_users_matches(self, frame: MatLike):
        """Get an array of users which card drawing can be seen in `frame`."""
        candidate_images = scan(frame.copy())

        user_matches = []
        for candidate_img in candidate_images:
            user_idx = self.image_comparator.get_match_idx(candidate_img)
            if user_idx is None:
                continue
            user_matches.append(self.users[user_idx])
        return user_matches

    def draw(self, frame: MatLike):
        """Find the matching user cards in the given `frame`. Highlighted the card contours and write their name next to it. Also return the array of matching users."""
        contours, candidate_images = scan(
            frame.copy(),
            keep_results=[
                card_contours_transform,
                rotate_top_left_corner_low_density_transform,
            ],
        )

        frame = cv2.drawContours(frame, contours, -1, (0, 255, 255), 3)
        # Detection was performed from the camera perspective but output img is flipped for mirror-like effect
        frame = cv2.flip(frame, 1)
        user_matches = []

        for candidate_idx, candidate_img in enumerate(candidate_images):
            user_idx = self.image_comparator.get_match_idx(candidate_img)
            if user_idx is None:
                continue
            u = self.users[user_idx]
            user_matches.append(u)
            contour = contours[candidate_idx]
            text_pos = contour[0][0] - [10, 10]
            # Account for flip
            text_pos[0] = frame.shape[1] - text_pos[0]
            # text = self._get_user_fullname(u)
            text = u

            frame = cv2.putText(
                frame,
                text,
                text_pos,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (200, 0, 255),
                2,
                cv2.LINE_AA,
            )
        return frame, user_matches
