import db_conf
import postgresql
import image_processing
import cv2
import error_log
import math
import time
import datetime
import os
import session_log

default_stack = 22

def searchCurrentStack(screen_area, stack_collection):
    try:
        for item in image_processing.getLastScreen(getStackArea(screen_area)):
            path = item['image_path']
            img_rgb = cv2.imread(path, 0)
            for value in stack_collection:
                if image_processing.cvDataTemplate(value['image_path'], img_rgb) > 0:
                    current_stack = int(value['stack_value'])
                    return current_stack
        return default_stack
    except Exception as e:
        error_log.errorLog('searchCurrentStack', str(e))
        print(e)

def searchOpponentStack(screen_area, opponent_area, stack_collection):
    try:
        folder_name = 'images/' + str(datetime.datetime.now().date())
        saveOpponentStackImage(str(screen_area), folder_name, opponent_area)
        screen_area = getOpponentStackArea(screen_area)
        for item in image_processing.getLastScreen(str(screen_area)):
            path = item['image_path']
            img_rgb = cv2.imread(path, 0)
            for value in stack_collection:
                if image_processing.cvDataTemplate(value['image_path'], img_rgb) > 0:
                    opponent_stack = int(value['stack_value'])
                    return opponent_stack
        return default_stack
    except Exception as e:
        error_log.errorLog('searchOpponentStack', str(e))
        print(e)

def getStackArea(screen_area):
    db = postgresql.open(db_conf.connectionString())
    sql = "select stack_area from screen_coordinates where screen_area = $1"
    data = db.query.first(sql, int(screen_area))
    return data

def getOpponentStackArea(screen_area):
    db = postgresql.open(db_conf.connectionString())
    sql = "select opponent_stack_area from screen_coordinates where screen_area = $1"
    data = db.query.first(sql, int(screen_area))
    return data

#Получение путей к изображениям шаблонов стеков
def getStackImages():
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select trim(image_path) as image_path, stack_value from stack where active = 1 order by id desc")
    return data

#Получение путей к конкретному изображению
def getStackImage(stack_value):
    db = postgresql.open(db_conf.connectionString())
    sql = "select trim(image_path) as image_path from stack where stack_value = $1"
    data = db.query.first(sql, stack_value)
    if len(data) == 0:
        return False
    return data


def getStackData(screen_area):
    db = postgresql.open(db_conf.connectionString())
    sql = "select x_coordinate,y_coordinate,width,height,screen_area from screen_coordinates where screen_area = $1"
    data = db.query(sql, screen_area)
    return data

def getOpponentStackData(screen_area, opponent_area):
    db = postgresql.open(db_conf.connectionString())
    sql = "select opp.x_coordinate,opp.y_coordinate,opp.width,opp.height,opp.screen_area " \
          "from screen_coordinates as sc inner join opponent_screen_coordinates as opp " \
          "on sc.opponent_stack_area = opp.screen_area " \
          "where sc.screen_area = $1 and opp.opponent_area = $2"
    data = db.query(sql, int(screen_area), int(opponent_area))
    return data

def saveStackImage(screen_area, image_name, folder_name):
    try:
        for val in getStackData(getStackArea(screen_area)):
            image_path = os.path.join(folder_name, str(getStackArea(screen_area)), image_name)
            image_processing.imaging(val['x_coordinate'], val['y_coordinate'], val['width'], val['height'], image_path,
                                     str(val['screen_area']))
    except Exception as e:
        error_log.errorLog('saveStackImage', str(e))
        print(e)

def saveOpponentStackImage(screen_area, folder_name, opponent_area):
    image_name = int(math.floor(time.time()))
    for val in getOpponentStackData(str(screen_area), str(opponent_area)):
        image_path = folder_name + "/" + str(val['screen_area']) + "/" + str(image_name) + ".png"
        image_processing.imaging(val['x_coordinate'], val['y_coordinate'], val['width'], val['height'], image_path, str(val['screen_area']))
        image_name += 1

def getAllinStackArea(screen_area):
    db = postgresql.open(db_conf.connectionString())
    sql = "select all_in_stack_area from screen_coordinates where screen_area = $1"
    data = db.query.first(sql, int(screen_area))
    return data

def saveAllinStackImage(screen_area):
    try:
        image_name = str(math.floor(time.time())) + ".png"
        folder_name = 'images/' + str(datetime.datetime.now().date())
        for val in getStackData(str(getAllinStackArea(str(screen_area)))):
            image_path = os.path.join(folder_name, str(getAllinStackArea(str(screen_area))), image_name)
            image_processing.imaging(val['x_coordinate'], val['y_coordinate'], val['width'], val['height'], image_path,
                                     val['screen_area'])
    except Exception as e:
        error_log.errorLog('saveAllinStackImage', str(e))
        print(e)

def searchAllinStack(screen_area):
    try:
        saveAllinStackImage(screen_area)
        screen_area = getAllinStackArea(str(screen_area))
        for item in image_processing.getLastScreen(str(screen_area)):
            path = item['image_path']
            img_rgb = cv2.imread(path, 0)
            for value in image_processing.getAllinStackImages():
                if image_processing.cvDataTemplate(value['image_path'], img_rgb) > 0:
                    all_in_stack = int(value['stack_value'])
                    return all_in_stack
        return default_stack
    except Exception as e:
        error_log.errorLog('searchAllinStack', str(e))
        print(e)

def getBankStackArea(screen_area):
    db = postgresql.open(db_conf.connectionString())
    sql = "select bank_stack_area from screen_coordinates where screen_area = $1"
    data = db.query(sql, int(screen_area))
    return data

def saveBankStackImage(screen_area):
    try:
        image_name = str(math.floor(time.time())) + ".png"
        folder_name = 'images/' + str(datetime.datetime.now().date())
        for val in getStackData(getBankStackArea(screen_area)):
            image_path = os.path.join(folder_name, str(getBankStackArea(str(screen_area))), image_name)
            image_processing.imaging(val['x_coordinate'], val['y_coordinate'], val['width'], val['height'], image_path,
                                     val['screen_area'])
    except Exception as e:
        error_log.errorLog('saveAllinStackImage', str(e))
        print(e)

def searchBankStack(screen_area):
    try:
        saveBankStackImage(screen_area)
        screen_area = getBankStackArea(str(screen_area))
        for item in image_processing.getLastScreen(str(screen_area)):
            path = item['image_path']
            img_rgb = cv2.imread(path, 0)
            for value in image_processing.getBankStackImages():
                if image_processing.cvDataTemplate(value['image_path'], img_rgb) > 0:
                    bank_stack = int(value['stack_value'])
                    return bank_stack
        return default_stack
    except Exception as e:
        error_log.errorLog('searchBankStack', str(e))
        print(e)

def compareBankAndAvailableStack(screen_area, stack_collection):
    stack = searchCurrentStack(screen_area, stack_collection)
    bank = searchBankStack(screen_area)
    if stack >= bank:
        return 'turn_cbet'
    elif stack < bank:
        return 'push'

def convertStack(stack):
    if stack >= 22:
        stack = 22
    elif stack in range(17, 22):
        stack = 21
    elif stack in range(13, 17):
        stack = 17
    elif stack in range(10, 13):
        stack = 13
    elif stack in range(7, 10):
        stack = 10
    elif stack == 0:
        stack = 0
    return stack

def getActualStack(screen_area, stack_collection, folder_name):
    image_name = str(math.floor(time.time())) + ".png"
    saveStackImage(str(screen_area), image_name, folder_name)
    stack = searchCurrentStack(screen_area, stack_collection)
    stack = convertStack(stack)
    session_log.updateCurrentStackLogSession(str(screen_area), str(stack))
    return stack