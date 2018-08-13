import image_processing
from PIL import Image, ImageGrab
import cv2
import datetime
import math
import time
import numpy as np
import session_log
import current_stack

images_folder = "images/"

def actionAfterOpen(screen_area, image_name, folder_name):
    checkIsFold(screen_area, image_name, folder_name)
    checkIsFlop(screen_area)
    checkIsRaiseTo(screen_area)
    checkIsCall(screen_area)

#Проверка, есть ли карты на столе
def checkIsFlop(screen_area):
    folder_name = images_folder + str(datetime.datetime.now().date())
    for item in image_processing.getUIButtonData("green_board"):
        image_name = str(math.floor(time.time()))
        image_path = folder_name + "/" + str(item['screen_area']) + "/" + image_name + ".png"
        # Делаем скрин указанной области экрана
        image = ImageGrab.grab(bbox=(item['x_coordinate'], item['y_coordinate'], item['width'], item['height']))
        # Сохраняем изображение на  жестком диске
        image.save(image_path, "PNG")
        # Сохраняем инфо в бд
        image_processing.insertImagePathIntoDb(image_path, (item['screen_area']))

        if searchEmptyBoard(str(item['screen_area'])) == 0:
            session_log.updateActionLogSession('flop', screen_area)
            return

#Поиск "зеленого сукна", если нет значит раздали флоп
def searchEmptyBoard(screen_area):
    path = image_processing.getLastScreen(screen_area)
    path = path[0]['image_path']
    img_rgb = cv2.imread(path, 0)
    template = cv2.imread('green_board/green_board.png', 0)

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.98
    loc = np.where(res >= threshold)

    if (len(loc[0]) != 0):
        return 1
    else: return 0

#Проверка, есть ли кнопка "Raise To"
def checkIsRaiseTo(screen_area):
    folder_name = images_folder + str(datetime.datetime.now().date())
    for item in image_processing.getUIButtonData("raise_to"):
        image_name = str(math.floor(time.time()))
        image_path = folder_name + "/" + str(item['screen_area']) + "/" + image_name + ".png"
        # Делаем скрин указанной области экрана
        image = ImageGrab.grab(bbox=(item['x_coordinate'], item['y_coordinate'], item['width'], item['height']))
        # Сохраняем изображение на  жестком диске
        image.save(image_path, "PNG")
        # Сохраняем инфо в бд
        image_processing.insertImagePathIntoDb(image_path, (item['screen_area']))

        if searchRaiseToButton(str(item['screen_area'])) == 1:
            # push/fold
            # session_log.updateActionLogSession('push/fold', screen_area)
            return

#Поиск кнопки "Raise To"
def searchRaiseToButton(screen_area):
    path = image_processing.getLastScreen(screen_area)
    path = path[0]['image_path']
    img_rgb = cv2.imread(path, 0)
    template = cv2.imread('action_buttons/raise_to.png', 0)

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.98
    loc = np.where(res >= threshold)

    if (len(loc[0]) != 0):
        return 1
    else: return 0

#Проверка, есть ли кнопка "Call"
def checkIsCall(screen_area):
    folder_name = images_folder + str(datetime.datetime.now().date())
    for item in image_processing.getUIButtonData("call"):
        image_name = str(math.floor(time.time()))
        image_path = folder_name + "/" + str(item['screen_area']) + "/" + image_name + ".png"
        # Делаем скрин указанной области экрана
        image = ImageGrab.grab(bbox=(item['x_coordinate'], item['y_coordinate'], item['width'], item['height']))
        # Сохраняем изображение на  жестком диске
        image.save(image_path, "PNG")
        # Сохраняем инфо в бд
        image_processing.insertImagePathIntoDb(image_path, (item['screen_area']))

        if searchCallButton(str(item['screen_area'])) == 1:
            # push/fold
            # session_log.updateActionLogSession('push/fold', screen_area)
            return

#Поиск кнопки "Call"
def searchCallButton(screen_area):
    path = image_processing.getLastScreen(screen_area)
    path = path[0]['image_path']
    img_rgb = cv2.imread(path, 0)
    template = cv2.imread('action_buttons/call.png', 0)

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.98
    loc = np.where(res >= threshold)

    if (len(loc[0]) != 0):
        return 1
    else: return 0

#Проверка, слелали ли противники фолд
def checkIsFold(screen_area, image_name, folder_name):
    last_stack = session_log.getLastHandFromLogSession(screen_area)[0]['current_stack']
    current_stack.saveStackImage(screen_area, image_name, folder_name)
    cur_stack = current_stack.searchCurrentStack(screen_area)
    if last_stack != cur_stack:
        session_log.updateActionLogSession('end', screen_area)
        return