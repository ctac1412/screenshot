import image_processing
import logic
import keyboard
import mouse
import cv2
import datetime
import math
import time
import numpy as np
import os

images_folder = "images"

def checkIsGameEnd():
    for item in image_processing.getUIButtonData("register_button"):
        image_path = os.path.join(images_folder, str(datetime.datetime.now().date()), str(item['screen_area']), str(math.floor(time.time())))
        image_processing.imaging(item['x_coordinate'], item['y_coordinate'], item['width'], item['height'], image_path,
                                 item['screen_area'])

        if searchRegisterButton(str(item['screen_area'])):
            mouse.moveMouse(item['x_mouse'], item['y_mouse'])
            mouse.leftClick()
            mouse.moveMouse(1240, 730)
            keyboard.doubleSpace()
    logic.updateIterationTimer("register_button")

#Поиск кнопки register
def searchRegisterButton(screen_area):
    path = image_processing.getLastScreen(screen_area)
    path = path[0]['image_path']
    img_rgb = cv2.imread(path, 0)
    template = cv2.imread('register_button/register_button.png', 0)

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.98
    loc = np.where(res >= threshold)

    if (len(loc[0]) != 0):
        return True
    else:
        return False