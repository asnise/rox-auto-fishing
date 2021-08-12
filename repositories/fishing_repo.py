import cv2
import pyautogui

import config


def set_limit():
    # ปิดจอแสดงผล
    cv2.destroyAllWindows()
    # เปลี่ยนสถานะเป็นรอ
    config.HOLD = True
    try:
        config.LIMIT = int(
            input("\nNumber of times fishing\n(default -1 for Unlimit): ") or "-1")
    except ValueError:
        print("Invalid number, set to unlimited.")
        config.LIMIT = -1
    config.LOOP = config.LIMIT
    # เริ่มนับใหม่
    config.COUNT = 0
    print("Running...\n")


def action_click():
    print("Event: mouse left click!")
    config.LAST_CLICK_TIME = config.CURRENT_TIME
    pyautogui.click(config.CENTER_X, config.CENTER_Y)


def gotcha():
    print('Gotcha!')
    action_click()
    config.COUNT += 1
    if config.LOOP > 0:
        config.LOOP -= 1
    # เข้าสู่สถานะรอโยนเบ็ด
    config.IS_FISHING = False


def throw_fishing_rod():
    print("Fishing!, throw the fishing rod.")
    action_click()
    # เข้าสู่สถานะกำลังตกปลา
    config.IS_FISHING = True
