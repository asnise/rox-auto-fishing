import cv2
import numpy as np

import config


def detect_green_color(hsv_frame):
    low_green = np.array([40, 135, 70])
    high_green = np.array([55, 255, 255])
    mask1 = cv2.inRange(hsv_frame, low_green, high_green)
    mask2 = cv2.inRange(hsv_frame, low_green, high_green)
    mask = cv2.bitwise_or(mask1, mask2)
    green = cv2.bitwise_and(config.FRAME, config.FRAME, mask=mask)
    return {
        "mask": mask,
        "green": green
    }
