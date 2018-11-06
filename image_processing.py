import cv2
import numpy as np
import postgresql
import os
import datetime
import error_log
import db_conf
from PIL import ImageGrab
import introduction

images_folder = "images"

def searchCards(screen_area, deck, list_length):
    hand = ''
    try:
        for item in getLastScreen(str(screen_area)):
            path = item['image_path']
            img_rgb = cv2.imread(path, 0)
            threshold = 0.98
            for value in deck:
                template = cv2.imread(str(value['image_path']), 0)
                res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
                loc = np.where(res >= threshold)
                if len(loc[0]) != 0:
                    hand += value['alias']
                if len(hand) == list_length:
                    return hand
    except Exception as e:
        error_log.errorLog('searchCards', str(e))
        print(e)
    if len(hand) < 4:
        hand = '72o'
    return hand

def insertImagePathIntoDb(image_path, screen_area):
    try:
        db = postgresql.open(db_conf.connectionString())
        insert = db.prepare("insert into screenshots (image_path,screen_area) values($1,$2)")
        insert(image_path, int(screen_area))
    except Exception as e:
        print('insertImagePathIntoDb ' + str(e))
        error_log.errorLog('insertImagePathIntoDb',str(e))

def getScreenData():
    try:
        db = postgresql.open(db_conf.connectionString())
        data = db.query("select x_coordinate,y_coordinate,width,height,screen_area,x_mouse,y_mouse "
                        "from screen_coordinates where active = 1 and alias = 'workspace'")
        return data
    except Exception as e:
        error_log.errorLog('getScreenData',str(e))

def checkIsFolderExist():
    folder_name = os.path.join(images_folder, str(datetime.datetime.now().date()))
    if not os.path.exists(str(folder_name)):
        os.makedirs(str(folder_name))
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select screen_area from screen_coordinates "
                    "union select screen_area from opponent_screen_coordinates")
    for value in data:
        if not os.path.exists(str(folder_name) + "/" + str(value['screen_area'])):
            os.makedirs(str(folder_name) + "/" + str(value['screen_area']))

def getCards():
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select trim(image_path) as image_path, trim(alias) as alias from cards")
    return data

def getFlopCards():
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select trim(image_path) as image_path,card,suit,trim(alias) as alias from flop_cards")
    return data

def getStackImages():
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select trim(image_path) as image_path, stack_value from stack where active = 1 order by id desc")
    return data

def getAllinStackImages():
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select trim(image_path) as image_path, stack_value from all_in_stack order by id desc")
    return data

def getActionsButtons():
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select trim(image_path) as image_path,trim(opponent_action) as opponent_action, "
                    "trim(alias) as alias from opponent_last_action")
    return data

def getLastScreen(screen_area, limit='1'):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select trim(image_path)as image_path from screenshots where screen_area = " +
                    str(screen_area) + " order by id desc limit " + limit)
    return data

def getUIButtonData(alias):
    try:
        db = postgresql.open(db_conf.connectionString())
        data = db.query("select x_coordinate,y_coordinate,width,height,screen_area,x_mouse,y_mouse "
                        "from screen_coordinates where active = 1 and alias = '" + alias + "'")
        return data
    except Exception as e:
        error_log.errorLog('getUIButtonData',str(e))
        print(e)

def madeScreenshot(x_coordinate, y_coordinate, width, height):
    image = ImageGrab.grab(bbox=(x_coordinate, y_coordinate, width, height))
    return image

def imaging(x_coordinate, y_coordinate, width, height, image_path, screen_area):
    image = madeScreenshot(x_coordinate, y_coordinate, width, height)
    image.save(image_path, "PNG")
    insertImagePathIntoDb(image_path, screen_area)

def searchElement(screen_area, elements, folder):
    for item in elements:
        path = getLastScreen(screen_area)
        path = path[0]['image_path']
        img_rgb = cv2.imread(path, 0)
        template = cv2.imread(folder + item + '.png', 0)
        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.98
        loc = np.where(res >= threshold)

        if len(loc[0]) != 0:
            return True
        return False

def searchLastOpponentAction(screen_area):
    element_area = introduction.saveElement(screen_area, 'limp_area')
    threshold = 0.98
    path = getLastScreen(element_area)
    path = path[0]['image_path']
    img_rgb = cv2.imread(path, 0)
    for item in getActionsButtons():
        template = cv2.imread(str(item['image_path']), 0)
        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        if len(loc[0]) != 0:
            return item
    return 'push'

def checkIsCbetAvailable(screen_area):
    element_area = introduction.saveElement(screen_area, 'limp_area')
    threshold = 0.98
    path = getLastScreen(element_area)
    path = path[0]['image_path']
    img_rgb = cv2.imread(path, 0)
    template = cv2.imread('action_buttons/check.png', 0)
    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    if len(loc[0]) > 0:
        return True


def getCurrentCards(condition):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select trim(image_path) as image_path, trim(alias) as alias from cards where alias in(" + condition + ")")
    return data

def convertHand(hand):
    hand = '\'' +  hand[0] + hand[1] + '\'' + ',' + '\'' + hand[2] + hand[3] + '\''
    return hand

def checkCurrentHand(screen_area, hand):
    current_hand = convertHand(hand)
    deck = getCurrentCards(current_hand)
    if len(searchCards(screen_area, deck, 4)) == 4:
        return True
    else:
        return False