import image_processing
import logic
import mouse
import cv2
import datetime
import math
import time
import numpy as np

images_folder = "images/"

def searchSitoutButton(screen_area):
    path = image_processing.getLastScreen(screen_area)
    path = path[0]['image_path']
    img_rgb = cv2.imread(path, 0)
    template = cv2.imread('sitout_button/sitout_button.png', 0)

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.98
    loc = np.where(res >= threshold)

    if (len(loc[0]) != 0):
        return True
    else:
        return False

def checkIsSitout():
    folder_name = images_folder + str(datetime.datetime.now().date())
    for val in image_processing.getUIButtonData("sitout_button"):
        image_name = str(math.floor(time.time()))
        image_path = folder_name + "/" + str(val['screen_area']) + "/" + image_name + ".png"
        image_processing.imaging(val['x_coordinate'], val['y_coordinate'], val['width'], val['height'], image_path,
                                 val['screen_area'])

        if searchSitoutButton(str(val['screen_area'])):
            mouse.moveMouse(val['x_mouse'], val['y_mouse'])
            mouse.leftClick()
    logic.updateIterationTimer("sitout_button")