import cv2
import numpy as np


class Filtres:
    @staticmethod
    def creer_filtre_teinte(rvb: tuple[int, int, int]):
        def hue_filter(image):
            alpha = 0.4
            color_image = np.zeros_like(image)
            bvr = (rvb[2], rvb[1], rvb[0])
            color_image[:] = bvr
            # Blend the original image and the color image
            return cv2.addWeighted(image, 1 - alpha, color_image, alpha, 0)

        return hue_filter

    @staticmethod
    def ocean(image):
        filtre = Filtres.creer_filtre_teinte((0, 0, 255))
        return filtre(image)

    @staticmethod
    def alien(image):
        filtre = Filtres.creer_filtre_teinte((0, 255, 0))
        return filtre(image)

    @staticmethod
    def rose(image):
        filtre = Filtres.creer_filtre_teinte((255, 192, 203))
        return filtre(image)

    @staticmethod
    def flou(image):
        return cv2.GaussianBlur(image, (15, 15), 0)

    @staticmethod
    def noir_et_blanc(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def tourner(image):
        return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

    @staticmethod
    def vernis(image):
        contrast_factor = 1.5
        brightness_factor = 30
        return cv2.convertScaleAbs(image, alpha=contrast_factor, beta=brightness_factor)

    @staticmethod
    def cartoon(image):
        # colour quantization
        # k value determines the number of colours in the image
        total_color = 8
        k = total_color

        # Transform the image
        data = np.float32(image).reshape((-1, 3))

        # Determine criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)

        # Implementing K-Means
        ret, label, center = cv2.kmeans(
            data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
        )
        center = np.uint8(center)
        result = center[label.flatten()]
        result = result.reshape(image.shape)
        blurred = cv2.bilateralFilter(result, d=10, sigmaColor=250, sigmaSpace=250)
        return blurred
