import image_processing
import cv2
import datetime
import math
import time
import numpy as np
import session_log
import current_stack
import logic
import postgresql
import db_conf

images_folder = "images/"

def actionAfterOpen(screen_area, image_name, folder_name, action):
    if action == 'open':
        if checkIsFold(screen_area, image_name, folder_name) == 1: return
    if checkIsFlop(screen_area) == 1: return
    if checkIsActionButtons(screen_area) == 1: return

def checkIsLimpAvailable(screen_area):
    folder_name = images_folder + str(datetime.datetime.now().date())
    element_area = getElementArea(screen_area, 'limp_area')['limp_area']
    for item in getElementData(element_area):
        image_name = str(math.floor(time.time()))
        image_path = folder_name + "/" + str(item['screen_area']) + "/" + image_name + ".png"
        image_processing.imaging(item['x_coordinate'], item['y_coordinate'], item['width'], item['height'], image_path, item['screen_area'])
    if searchLimpValue(element_area) == 1:
        return True

#Проверка, есть ли карты на столе
def checkIsFlop(screen_area):
    folder_name = images_folder + str(datetime.datetime.now().date())
    element_area = getElementArea(screen_area,'green_board_area')['green_board_area']
    for item in getElementData(element_area):
        image_name = str(math.floor(time.time()))
        image_path = folder_name + "/" + str(item['screen_area']) + "/" + image_name + ".png"
        image_processing.imaging(item['x_coordinate'], item['y_coordinate'], item['width'], item['height'], image_path, item['screen_area'])
    if searchEmptyBoard(element_area) == 0:
        session_log.updateActionLogSession('flop', screen_area)
        return 1

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
def checkIsActionButtons(screen_area):
    folder_name = images_folder + str(datetime.datetime.now().date())
    element_area = getElementArea(screen_area, 'action_btn_area')['action_btn_area']
    for item in getElementData(element_area):
        image_name = str(math.floor(time.time()))
        image_path = folder_name + "/" + str(item['screen_area']) + "/" + image_name + ".png"
        image_processing.imaging(item['x_coordinate'], item['y_coordinate'], item['width'], item['height'], image_path, item['screen_area'])
    if searchActionButtons(element_area) == 1:
        condition = session_log.getLastHandFromLogSession(str(screen_area))
        logic.getDecision(condition[0]['hand'], condition[0]['current_stack'], condition[0]['current_position'],
                          str(screen_area), condition[0]['action'])
        return 1


#Поиск кнопок "Raise To" "Call"
def searchActionButtons(screen_area):
    action_buttons = ['raise_to', 'call']
    for item in action_buttons:
        path = image_processing.getLastScreen(screen_area)
        path = path[0]['image_path']
        img_rgb = cv2.imread(path, 0)
        template = cv2.imread('action_buttons/'+item+'.png', 0)

        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.98
        loc = np.where(res >= threshold)

        if (len(loc[0]) != 0):
            return 1

#Проверка, слелали ли противники фолд
def checkIsFold(screen_area, image_name, folder_name):
    last_stack = session_log.getLastHandFromLogSession(screen_area)[0]['current_stack']
    current_stack.saveStackImage(screen_area, image_name, folder_name)
    cur_stack = current_stack.searchCurrentStack(screen_area)
    if int(last_stack) != int(cur_stack):
        session_log.updateActionLogSession('end', screen_area)
        return 1

def getElementArea(screen_area, element):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select " + element + " from screen_coordinates where screen_area = " + str(screen_area) + " and active = 1")
    return data[0]

def getElementData(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select x_coordinate,y_coordinate,width,height,screen_area from screen_coordinates "
                    "where active = 1 and screen_area = " + str(screen_area))
    return data

def searchLimpValue(screen_area):
    path = image_processing.getLastScreen(screen_area)
    path = path[0]['image_path']
    img_rgb = cv2.imread(path, 0)
    template = cv2.imread('limp/limp.png', 0)

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.98
    loc = np.where(res >= threshold)

    if len(loc[0]) != 0:
        return 1
    else: return 0