import cv2
import numpy as np
import postgresql
import os
import datetime
import error_log
from PIL import Image, ImageGrab
import math
import time
import mouse
import keyboard
import logic

images_folder = "images/"

#Поиск карт игрока на скрине
def searchPlayerHand(screen_area):
    try:
        hand = ''
        for value in getCards():
            try:
                path = getLastScreen(screen_area)
                path = path[0]['image_path']
                img_rgb = cv2.imread(path, 0)
                template = cv2.imread(str(value['image_path']), 0)

                res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
                threshold = 0.98
                loc = np.where(res >= threshold)

                if (len(loc[0]) != 0):
                    hand += value['alias']

            except Exception as e:
                error_log.errorLog('searchPlayerHand', e)
        return hand
    except Exception as e:
        error_log.errorLog('searchPlayerHand',e)


#Вставка пути к изображению в бд
def insertImagePathIntoDb(image_path,screen_area):
    try:
        db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
        insert = db.prepare("insert into screenshots (image_path,screen_area) values($1,$2)")
        insert(image_path, screen_area)
    except Exception as e:
        error_log.errorLog('insertImagePathIntoDb',e)


#Получение информации об области экрана, на которой будет делаться скриншот
def getScreenData():
    try:
        db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
        data = db.query("select x_coordinate,y_coordinate,width,height,screen_area,x_mouse,y_mouse from screen_coordinates "
                        "where active = 1 and alias = 'workspace'")
        return data
    except Exception as e:
        error_log.errorLog('getScreenData',e)

#Проверка на существование папок
def checkIsFolderExist():
    folder_name = images_folder + str(datetime.datetime.now().date())
    if not os.path.exists(str(folder_name)):
        os.makedirs(str(folder_name))
    db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
    data = db.query("select screen_area from screen_coordinates")
    for value in data:
        if not os.path.exists(str(folder_name) + "/" + str(value['screen_area'])):
            os.makedirs(str(folder_name) + "/" + str(value['screen_area']))

#Получение путей к изображениям шаблонов карт
def getCards():
    db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
    data = db.query("select trim(image_path) as image_path,card,suit,trim(alias) as alias from cards")
    return data

#Получение последнего скрина для текущей области экрана
def getLastScreen(screen_area):
    db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
    data = db.query("select trim(image_path)as image_path from screenshots where screen_area = " + str(screen_area) + " order by id desc limit 1")
    return data

def getUIButtonData(alias):
    try:
        db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
        data = db.query("select x_coordinate,y_coordinate,width,height,screen_area,x_mouse,y_mouse from screen_coordinates "
                        "where active = 1 and alias = " + alias)
        return data
    except Exception as e:
        error_log.errorLog('getScreenData',e)

def checkIsGameEnd():
    folder_name = images_folder + str(datetime.datetime.now().date())
    for item in getUIButtonData("register_button"):
        image_name = str(math.floor(time.time()))
        image_path = folder_name + "/" + str(item['screen_area']) + "/" + image_name + ".png"
        # Делаем скрин указанной области экрана
        image = ImageGrab.grab(bbox=(item['x_coordinate'], item['y_coordinate'], item['width'], item['height']))
        # Сохраняем изображение на жестком диске
        image.save(image_path, "PNG")
        # Сохраняем инфо в бд
        insertImagePathIntoDb(image_path, (item['screen_area']))

        if searchRegisterButton(str(item['screen_area'])) == 1:
            mouse.moveMouse(item['x_mouse'], item['y_mouse'])
            mouse.leftClick()
            mouse.moveMouse(1150, 650)
            keyboard.doubleSpace()
    logic.updateIterationTimer("register_button")

def searchRegisterButton(screen_area):
    path = getLastScreen(screen_area)
    path = path[0]['image_path']
    img_rgb = cv2.imread(path, 0)
    template = cv2.imread('register_button/register_button.png', 0)

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.98
    loc = np.where(res >= threshold)

    if (len(loc[0]) != 0):
        return 1
    else: return 0

def searchSitoutButton(screen_area):
    path = getLastScreen(screen_area)
    path = path[0]['image_path']
    img_rgb = cv2.imread(path, 0)
    template = cv2.imread('sitout_button/sitout_button.png', 0)

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.98
    loc = np.where(res >= threshold)

    if (len(loc[0]) != 0):
        return 1
    else: return 0

def checkIsSitout():
    folder_name = images_folder + str(datetime.datetime.now().date())
    for item in getUIButtonData("sitout_button"):
        image_name = str(math.floor(time.time()))
        image_path = folder_name + "/" + str(item['screen_area']) + "/" + image_name + ".png"
        # Делаем скрин указанной области экрана
        image = ImageGrab.grab(bbox=(item['x_coordinate'], item['y_coordinate'], item['width'], item['height']))
        # Сохраняем изображение на жестком диске
        image.save(image_path, "PNG")
        # Сохраняем инфо в бд
        insertImagePathIntoDb(image_path, (item['screen_area']))

        if searchSitoutButton(str(item['screen_area'])) == 1:
            mouse.moveMouse(item['x_mouse'], item['y_mouse'])
            mouse.leftClick()
    logic.updateIterationTimer("sitout_button")