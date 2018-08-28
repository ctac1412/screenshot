import image_processing
import cv2
import numpy as np
import postgresql
import db_conf
from PIL import Image, ImageGrab
import error_log

#Поиск блайндов и соответственно определение позиции за столом
def seacrhBlindChips(screen_area):
    blinds = ['big_blind','small_blind']
    for blind in blinds:
        # print((screen_area))
        # print(getBlindArea(str(screen_area)))
        path = image_processing.getLastScreen(getBlindArea(str(screen_area)))
        path = path[0]['image_path']
        img_rgb = cv2.imread(path, 0)
        template = cv2.imread('blinds/' + blind + '.png', 0)

        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.98
        loc = np.where(res >= threshold)

        if (len(loc[0]) != 0):
            return blind

    return 'button'

#Получаем номер области экрана, на которой нужно искать элемент для текущего стола
def getBlindArea(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select blind_area from screen_coordinates where screen_area = " + screen_area + " and active = 1")
    return data[0]['blind_area']

def getBlindData(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select x_coordinate,y_coordinate,width,height,screen_area from screen_coordinates "
                    "where screen_area = "  + screen_area)
    return data

def saveBlindImage(screen_area,image_name,folder_name):
    try:
        for value in getBlindData(str(getBlindArea(str(screen_area)))):
            image_path = folder_name + "/" + str(getBlindArea(str(screen_area))) + "/" + image_name + ".png"
            # Делаем скрин указанной области экрана
            image = ImageGrab.grab(bbox=(value['x_coordinate'], value['y_coordinate'], value['width'], value['height']))
            # Сохраняем изображение на жестком диске
            image.save(image_path, "PNG")
            # Сохраняем инфо в бд
            image_processing.insertImagePathIntoDb(image_path, value['screen_area'])
    except Exception as e:
        error_log.errorLog('saveBlindImage', str(e))
        print(e)
