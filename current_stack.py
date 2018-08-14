import db_conf
import postgresql
import image_processing
import cv2
import numpy as np
from PIL import Image, ImageGrab

#Определение текущего стека
def searchCurrentStack(screen_area):
    current_stack = ''
    for value in getStackImages():
        path = image_processing.getLastScreen(str(getStackArea(screen_area)))
        path = path[0]['image_path']
        img_rgb = cv2.imread(path, 0)
        template = cv2.imread(str(value['image_path']), 0)

        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.98
        loc = np.where(res >= threshold)

        if (len(loc[0]) != 0):
            current_stack = str(value['stack_value'])
        if len(current_stack) > 0:
            return str(current_stack)
    return 20

#Получаем номер области экрана, на которой нужно искать элемент для текущего стола
def getStackArea(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select stack_area from screen_coordinates where screen_area = " + screen_area + " and active = 1")
    return data[0]['stack_area']

#Получение путей к изображениям шаблонов стеков
def getStackImages():
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select trim(image_path) as image_path, stack_value from stack")
    return data

def getStackData(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select x_coordinate,y_coordinate,width,height,screen_area from screen_coordinates "
                    "where screen_area = "  + screen_area)
    return data

def saveStackImage(screen_area,image_name,folder_name):
    for val in getStackData(str(getStackArea(str(screen_area)))):
        image_path = folder_name + "/" + str(getStackArea(str(screen_area))) + "/" + image_name + ".png"
        # Делаем скрин указанной области экрана
        image = ImageGrab.grab(bbox=(val['x_coordinate'], val['y_coordinate'], val['width'], val['height']))
        # Сохраняем изображение на жестком диске
        image.save(image_path, "PNG")
        # Сохраняем инфо в бд
        image_processing.insertImagePathIntoDb(image_path, val['screen_area'])