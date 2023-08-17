"""Module Camera"""

from skimage.metrics import structural_similarity as ssim
import cv2
import os
import numpy as np

def _ssi(image1, image2):
    """Compare two images

    Arguments:
        image1 {numpy.ndarray} -- First image
        image2 {numpy.ndarray} -- Second image

    Returns:
        float -- Similarity between the two images
    """

    if image1 is None or image2 is None:
        raise ValueError("One of the images is None")

    # Convert the images to grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Check for same size and ratio and report accordingly
    image1_height, image1_width, _ = image1.shape
    image2_height, image2_width, _ = image2.shape

    if image1_height * image1_width > image2_height * image2_width:
        gray1 = cv2.resize(gray1, (image2_width, image2_height))
    elif image1_height * image1_width < image2_height * image2_width:
        gray2 = cv2.resize(gray2, (image1_width, image1_height))

    return ssim(gray1, gray2)


def _compare_card(frame, small_frame, card_file, i):
    card = cv2.imread(f"module_camera/cards/{card_file}", cv2.IMREAD_COLOR)
    similarity = _ssi(small_frame, card)
    diff = cv2.absdiff(small_frame, card)

    name = None
    if similarity > 0.8:
        cv2.putText(diff, "X", (0, 24), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        name = card_file[:-4]

    x = i * 64 % 640
    y = x // 640 * 48
    frame[y:y+48, x:x+64] = diff
    return frame, name


def run():
    """Run the module"""
    cam = cv2.VideoCapture(4)
    cv2.namedWindow("module_camera", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('module_camera', cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)
    filgrane = cv2.imread("module_camera/card_filgrane.png", cv2.IMREAD_COLOR)

    card = cv2.imread("card.png", cv2.IMREAD_COLOR)
    name = None
    while True:
        ret, frame = cam.read()
        if not ret:
            break

        small_frame = cv2.resize(frame, (64, 48))
        names = []
        for i, file in enumerate(os.listdir("module_camera/cards")):
            frame, name_tmp = _compare_card(frame, small_frame, file, i)
            if name_tmp is not None:
                names.append(name_tmp)
        if len(names) > 0:
            name = ", ".join(names)
        else:
            name = None

        frame = cv2.absdiff(filgrane, frame)
        cv2.flip(frame, 1)
        print(name)
        if name is not None:
            cv2.putText(frame, name, (0, 470), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.imshow("module_camera", frame)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break
        if key == ord("s"):
            cv2.imwrite("card.png", small_frame)

    cam.release()
    cv2.destroyAllWindows()
