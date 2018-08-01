import db_conf
import postgresql
import image_processing
import cv2
import numpy as np

#Определение текущего стека
def searchCurrentStack(screen_area):
    current_stack = ''
    for value in getStackData():
        path = image_processing.getLastScreen(getStackArea(screen_area))
        path = path[0]['image_path']
        img_rgb = cv2.imread(path, 0)
        template = cv2.imread(str(value['image_path']), 0)

        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.98
        loc = np.where(res >= threshold)

        if (len(loc[0]) != 0):
            current_stack += value['stack_value']
        if len(current_stack) > 0:
            return current_stack
    return 0

#Получаем номер области экрана, на которой нужно искать элемент для текущего стола
def getStackArea(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select stack_area from screen_coordinates where screen_area = " + screen_area)
    return data[0]['stack_area']

#Получение путей к изображениям шаблонов стеков
def getStackData():
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select trim(image_path) as image_path, stack_value from stack")
    return data