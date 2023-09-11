#! venv/bin/python3

from module_webapp import create_app
import threading
import time
import os
import cv2
from interactions import UserCardsTracker


def cam_track_cards_app(app) -> int | None:
    """Run an application that opens the camera, and print the users name next to the matching cards."""
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Track users", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Track users", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    card_tracker = UserCardsTracker(app)

    while True:
        ret, frame = cam.read()
        frame = cv2.flip(frame, 1)
        if not ret:
            break
        frame, users = card_tracker.draw(frame)
        if len(users):
            [
                print(f"- Match user (ID: {u.id}) {u.first_name} {u.last_name}")
                for u in users
            ]
        cv2.imshow("Track users", frame)
        key = cv2.waitKey(1)
        ESC_KEY = 27
        if key == ESC_KEY or key == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()
    return None


def auth():
    time.sleep(2)
    cam_track_cards_app(app)


if __name__ == "__main__":
    app = create_app(root_dir=os.path.dirname(os.path.abspath(__file__)))
    threading.Thread(target=auth).start()
    app.run()
