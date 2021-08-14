# -*- coding: utf-8 -*-
import os
import ctypes
from threading import Thread
import time
import numpy as np
import cv2
from mss import mss
from win32api import GetSystemMetrics

import config
from repositories import detector_repo
from repositories import fishing_repo
from repositories import render_repo

config.PID = os.getpid()
config.SCREEN_WIDTH = int(GetSystemMetrics(0))
config.SCREEN_HEIGHT = int(GetSystemMetrics(1))

sct = mss()
ctypes.windll.kernel32.SetConsoleTitleW(
    config.TITLE + ' ' + str(config.VERSION))
# Clear console
os.system('cls' if os.name in ('nt', 'dos') else 'clear')

print("RO:X Next Generation - Auto Fishing version %s" % config.VERSION)
print("Made by Thanapat Maliphan. (fb.com/thanatos1995)\n")

print("Screen resolution")
print("width = ", config.SCREEN_WIDTH)
print("height = ", config.SCREEN_HEIGHT)

print("\nPress 'R' button to reset limit.")
print("Press 'H' button to toggle fishing.")
print("Press 'Q' button to exit program.\n")


def main_function():
    while True:
        # Reset when reaching the limit
        if config.COUNT - config.LIMIT == 0:
            fishing_repo.set_limit()
        # ดักปุ่มกด
        key = cv2.waitKey(25)
        # Press "R" button to Reset
        if key & 0xFF == ord('r'):
            fishing_repo.set_limit()
        # Press "H" button to Hold
        if key & 0xFF == ord('h'):
            config.HOLD ^= True
        # Press "Q" button to exit program
        if key & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

        # เวลาปัจจุบัน
        config.CURRENT_TIME = time.time()

        # Crop
        render_repo.crop_screenshot(sct=sct)

        # แปลงสีภาพ
        config.FRAME = cv2.cvtColor(
            np.array(config.FRAME), cv2.COLOR_BGR2RGB)
        hsv_frame = cv2.cvtColor(config.FRAME, cv2.COLOR_BGR2HSV)

        # Detect green color
        detector = detector_repo.detect_green_color(hsv_frame=hsv_frame)

        # Render window
        render_repo.show(detector=detector)

        # ระยะเวลาที่ห่างจากการคลิกครั้งล่าสุด
        last_click_sec = config.CURRENT_TIME - config.LAST_CLICK_TIME

        # ตรวจจับพื้นที่สีเขียว
        if not config.HOLD and config.LOOP != 0:
            if cv2.countNonZero(detector["mask"]) > 0:  # เขียวแล้ว
                if config.IS_FISHING and last_click_sec > 2:  # รออย่างน้อย 2 วินาที เพื่อกดใหม่
                    fishing_repo.gotcha()
            else:   # ยังไม่เขียว
                if not config.IS_FISHING and last_click_sec > 4 and config.COUNT > 0:  # รอโยนเบ็ดครั้งถัดไปในอีก 4 วินาที
                    fishing_repo.throw_fishing_rod()


if __name__ == "__main__":
    thread = Thread(target=main_function)
    thread.start()
    thread.join()
