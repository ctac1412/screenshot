import image_processing
import cv2
import numpy as np
import postgresql
import db_conf

#Поиск блайндов и соответственно определение позиции за столом
def seacrhBlindChips(screen_area):
    blinds = ['big_blind','small_blind']
    for blind in blinds:
        path = image_processing.getLastScreen(str(getBlindArea(screen_area)))
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
    data = db.query("select blind_area from screen_coordinates where screen_area = " + "'" + str(screen_area) + "'")
    return data[0]['blind_area']