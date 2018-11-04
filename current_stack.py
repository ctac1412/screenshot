import db_conf
import postgresql
import image_processing
import cv2
import numpy as np
import error_log
import math
import time
import datetime
import os

def searchCurrentStack(screen_area, stack_collection):
    try:
        current_stack = 22
        for item in image_processing.getLastScreen(getStackArea(screen_area)):
            path = item['image_path']
            img_rgb = cv2.imread(path, 0)
            for value in stack_collection:
                template = cv2.imread(str(value['image_path']), 0)
                res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
                threshold = 0.98
                loc = np.where(res >= threshold)
                if len(loc[0]) != 0:
                    current_stack = int(value['stack_value'])
                    return current_stack
        return current_stack
    except Exception as e:
        error_log.errorLog('searchCurrentStack', str(e))
        print(e)
def searchOpponentStack(screen_area, opponent_area, stack_collection):
    try:
        folder_name = 'images/' + str(datetime.datetime.now().date())
        saveOpponentStackImage(str(screen_area), folder_name, opponent_area)
        opponent_stack = 22
        screen_area = getOpponentStackArea(str(screen_area))
        for item in image_processing.getLastScreen(str(screen_area)):
            path = item['image_path']
            img_rgb = cv2.imread(path, 0)
            for value in stack_collection:
                template = cv2.imread(str(value['image_path']), 0)
                res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
                threshold = 0.98
                loc = np.where(res >= threshold)
                if len(loc[0]) != 0:
                    opponent_stack = int(value['stack_value'])
                    return opponent_stack
        return opponent_stack
    except Exception as e:
        error_log.errorLog('searchOpponentStack', str(e))
        print(e)


#Поиск конкретного стека
def searchConctreteStack(screen_area, last_stack):
    path = image_processing.getLastScreen(str(getStackArea(str(screen_area))))
    path = path[0]['image_path']
    img_rgb = cv2.imread(path, 0)
    template = getStackImage(last_stack)
    if template == 0:
        return False
    template = cv2.imread(template, 0)
    if len(template) == 0:
        return False

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.98
    loc = np.where(res >= threshold)

    if len(loc[0]) > 0:
        return True
    else:
        return False

def getStackArea(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select stack_area from screen_coordinates where screen_area = " + screen_area + " and active = 1")
    return data[0]['stack_area']

def getOpponentStackArea(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select opponent_stack_area from screen_coordinates where screen_area = " + screen_area)
    return data[0]['opponent_stack_area']

#Получение путей к изображениям шаблонов стеков
def getStackImages():
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select trim(image_path) as image_path, stack_value from stack where active = 1 order by id desc")
    return data

#Получение путей к конкретному изображению
def getStackImage(stack_value):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select trim(image_path) as image_path from stack where stack_value = " + stack_value)
    if len(data) == 0:
        return False
    return data[0]['image_path']


def getStackData(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select x_coordinate,y_coordinate,width,height,screen_area from screen_coordinates "
                    "where screen_area = " + screen_area)
    return data

def getOpponentStackData(screen_area, opponent_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select opp.x_coordinate,opp.y_coordinate,opp.width,opp.height,opp.screen_area "
                    "from screen_coordinates as sc "
                    "inner join opponent_screen_coordinates as opp on sc.opponent_stack_area = opp.screen_area "
                    "where sc.screen_area = " + str(screen_area) + " and opp.opponent_area = " + opponent_area)
    return data

def saveStackImage(screen_area, image_name, folder_name):
    try:
        for val in getStackData(str(getStackArea(str(screen_area)))):
            image_path = os.path.join(folder_name, str(getStackArea(str(screen_area))), image_name)
            image_processing.imaging(val['x_coordinate'], val['y_coordinate'], val['width'], val['height'], image_path,
                                     val['screen_area'])
    except Exception as e:
        error_log.errorLog('saveStackImage', str(e))
        print(e)

def saveOpponentStackImage(screen_area, folder_name, opponent_area):
    image_name = int(math.floor(time.time()))
    for val in getOpponentStackData(str(screen_area), str(opponent_area)):
        image_path = folder_name + "/" + str(val['screen_area']) + "/" + str(image_name) + ".png"
        image_processing.imaging(val['x_coordinate'], val['y_coordinate'], val['width'], val['height'], image_path, str(val['screen_area']))
        image_name += 1


