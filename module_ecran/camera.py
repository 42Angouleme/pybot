import time
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
        if not ret:
            break
        frame, users = card_tracker.draw(frame)
        if len(users):
            print(f"- Match user (ID: {users[0].id}) {users[0].first_name} {users[0].last_name}")
            print(users[0])
            break
        cv2.imshow("Track users", frame)
        key = cv2.waitKey(1)
        ESC_KEY = 27
        if key == ESC_KEY or key == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()
    return None
