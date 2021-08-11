import cv2
import pyautogui

import config


def set_limit():
    try:
        config.LIMIT = int(
            input("Number of times fishing\n(default -1 for Unlimit): ") or "-1")
    except ValueError:
        print("Invalid number, set to unlimited.")
        config.LIMIT = -1
    config.LOOP = config.LIMIT
    config.COUNT = 0
    print("Running...\n")


def render_tracking_info(curTime):
    # Initialize FPS variables
    sec = curTime - config.PREV_TIME
    config.PREV_TIME = curTime
    fps = 1 / sec
    count_str = "%d time" % config.COUNT
    fps_str = "FPS: %0.1f" % fps
    # Right side
    cv2.rectangle(config.FRAME, (config.BOUNDING_BOX['width'] - (
        65 if not config.HOLD else 40), config.BOUNDING_BOX['width'] - 15), (config.BOUNDING_BOX['width'] - (
            30 if not config.HOLD else 40) + 70, config.BOUNDING_BOX['height']), (0, 255, 0) if not config.HOLD else (0, 0, 255), -1)
    cv2.putText(config.FRAME, str("Fishing..." if not config.HOLD else "Stop"), (config.BOUNDING_BOX['width'] - (
        60 if not config.HOLD else 35), config.FRAME.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0) if not config.HOLD else (255, 255, 255), 1)
    # Left side
    cv2.putText(config.FRAME, str("Limit: " + str("No" if config.LOOP == -1 else config.LOOP)), (0,
                config.FRAME.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    cv2.putText(config.FRAME, str("Count: " + count_str), (0,
                config.FRAME.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    cv2.putText(config.FRAME, str(
        fps_str), (0, config.FRAME.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)


def render_center_point():
    cv2.circle(config.FRAME, (0 + int(config.BOUNDING_BOX['width'] / 2), 0 + int(
        config.BOUNDING_BOX['height'] / 2)), config.RADIUS, (255, 255, 255), thickness=1, lineType=8, shift=0)
    cv2.rectangle(config.FRAME, (0 + int(config.BOUNDING_BOX['width'] / 2), 0 + int(config.BOUNDING_BOX['height'] / 2)),
                  (0 + int(config.BOUNDING_BOX['width'] / 2),
                   0 + int(config.BOUNDING_BOX['height'] / 2)),
                  (255, 255, 255), 5)


def mouse_click():
    print("Event: mouse left click!")
    config.LAST_CLICK_TIME = config.CURRENT_TIME
    pyautogui.click(config.CENTER_X, config.CENTER_Y)
