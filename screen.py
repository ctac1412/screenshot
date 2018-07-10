from PIL import Image, ImageGrab
import time
import datetime
import os
import math


def start():
    folder_name = datetime.datetime.now().date()
    if not os.path.exists(str(folder_name)):
        os.makedirs(str(folder_name))

    if not os.path.exists(str(folder_name) + "/1"):
        os.makedirs(str(folder_name) + "/1")

    if not os.path.exists(str(folder_name) + "/2"):
        os.makedirs(str(folder_name) + "/2")

    for iteration in range(3):
        # img_name = time.strftime("%H-%M-%S")
        img_name = math.floor(time.time())
        time.sleep(1)
        img1 = ImageGrab.grab(bbox=(0, 0, 300, 300))
        img1.save(str(folder_name) + "/1/" + str(img_name) + ".png", "PNG")

        img2 = ImageGrab.grab(bbox=(300, 0, 600, 300))
        img2.save(str(folder_name) + "/2/" + str(img_name) + ".png", "PNG")