from threading import Thread
import time
import numpy as np
import cv2
from mss import mss
from PIL import Image
import pyautogui

import config
from repositories import fishing_repo

sct = mss()

print("version %s" % config.VERSION)
print("Made by Thanapat Maliphan. (fb.com/thanatos1995)\n")
print("Press 'R' button to reset limit.")
print("Press 'H' button to toggle fishing.")
print("Press 'Q' button to exit program.\n")

# Get loop number
config.LOOP = int(input("Number of times fishing\n(default -1 for Unlimit): ") or "-1")
print("Running...\n")


def main_function():
    while True:
        # เวลาปัจจุบัน
        config.CURRENT_TIME = time.time()

        # take a screenshot of the screen and store it in memory, then
        # convert the PIL/Pillow image to an OpenCV compatible NumPy array
        # and finally write the image to disk
        config.FRAME = pyautogui.screenshot()

        # Crop
        sct.get_pixels(config.BOUNDING_BOX)
        config.FRAME = Image.frombytes(
            'RGB', (sct.width, sct.height), sct.image)

        # แปลงสีภาพ
        config.FRAME = cv2.cvtColor(
            np.array(config.FRAME), cv2.COLOR_BGR2RGB)
        hsv_frame = cv2.cvtColor(config.FRAME, cv2.COLOR_BGR2HSV)

        # Green color
        low_green = np.array([40, 135, 70])
        high_green = np.array([50, 255, 255])
        mask1 = cv2.inRange(hsv_frame, low_green, high_green)
        mask2 = cv2.inRange(hsv_frame, low_green, high_green)
        mask = cv2.bitwise_or(mask1, mask2)
        green = cv2.bitwise_and(config.FRAME, config.FRAME, mask=mask)

        # แสดงรายละเอียดบนจอ
        fishing_repo.render_tracking_info(config.CURRENT_TIME)

        # Center point
        fishing_repo.render_center_point()

        # Render
        cv2.imshow('RO:X - Auto Fishing v%s' % config.VERSION,
                   np.hstack([config.FRAME]))

        # ระยะเวลาที่ห่างจากการคลิกครั้งล่าสุด
        last_click_sec = config.CURRENT_TIME - config.LAST_CLICK_TIME

        # ตรวจจับพื้นที่สีเขียวq
        if not config.HOLD and config.LOOP != 0:
            if cv2.countNonZero(mask) > 0:  # เขียวแล้ว
                if config.IS_FISHING and last_click_sec > 2:  # รออย่างน้อย 2 วินาที เพื่อกดใหม่
                    print('Gotcha!')
                    fishing_repo.mouse_click()
                    config.COUNT += 1
                    if config.LOOP > 0:
                        config.LOOP -= 1
                    config.IS_FISHING = False
            else:   # ยังไม่เขียว
                if not config.IS_FISHING and last_click_sec > 4 and config.COUNT > 0:  # รอโยนเบ็ดครั้งถัดไปในอีก 4 วินาที
                    print("Fishing!, throw the fishing rod.")
                    fishing_repo.mouse_click()
                    # เข้าสู่สถานะกำลังตกปลา
                    config.IS_FISHING = True
        # Reset
        if config.LOOP == 0:
            config.HOLD = True
            config.LOOP = int(input("Number of times fishing\n(default -1 for Unlimit): ") or "-1")
            print("Running...\n")

        key = cv2.waitKey(25)
        # Press "R" button to Reset
        if key & 0xFF == ord('r'):
            config.LOOP = int(input("Number of times fishing\n(default -1 for Unlimit): ") or "-1")
            print("Running...\n")
        # Press "H" button to Hold
        if key & 0xFF == ord('h'):
            config.HOLD ^= True
        # Press "Q" button to exit program
        if key & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    thread = Thread(target=main_function)
    thread.start()
    thread.join()
