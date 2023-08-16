"""Module Camera"""

from skimage.metrics import structural_similarity as ssim
import cv2

def _ssi(image1, image2_path):
    """Compare two images

    Arguments:
        image1_path {str} -- Path to the first image
        image2_path {str} -- Path to the second image

    Returns:
        float -- Similarity between the two images
    """

    # Import images
    image2 = cv2.imread(image2_path, cv2.IMREAD_COLOR)
    if image1 is None or image2 is None:
        raise Exception("One or both images could not be found. Check input.")

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


def run():
    """Run the module"""
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("normal")

    while True:
        ret, frame = cam.read()
        if not ret:
            break
        cv2.imshow("normal", frame)

        frame = cv2.resize(frame, (32, 24))
        similarity = _ssi(frame, "./test.png")
        print(f"Similarity: {similarity:.2%}")

        key = cv2.waitKey(1)
        if key == ord("q"):
            break
        elif key == ord("s"):
            cv2.imwrite("test.png", frame)

    cam.release()
    cv2.destroyAllWindows()
