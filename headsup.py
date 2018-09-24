import db_conf
import postgresql
import image_processing
import cv2
import numpy as np
import error_log
import math
import time
import datetime

def searchOpponentCard(screen_area):
    try:
        folder_name = 'images/' + str(datetime.datetime.now().date())
        saveOpponentCardImage(str(screen_area), folder_name)
        check_is_headsup = 0
        screen_area = getOpponentCardArea(str(screen_area))
        for item in image_processing.getLastScreen(str(screen_area), '2'):
            path = item['image_path']
            img_rgb = cv2.imread(path, 0)
            template = cv2.imread('is_headsup/is_headsup.png', 0)
            res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.98
            loc = np.where(res >= threshold)
            if len(loc[0]) != 0:
                check_is_headsup +=1
        if check_is_headsup == 1:
            return True
        else: return 0
    except Exception as e:
        print(e)

def saveOpponentCardImage(screen_area, folder_name):
    image_name = int(math.floor(time.time()))
    for val in getOpponentCardData(str(screen_area)):
        image_path = folder_name + "/" + str(val['screen_area']) + "/" + str(image_name) + ".png"
        image_processing.imaging(val['x_coordinate'], val['y_coordinate'], val['width'], val['height'], image_path, val['screen_area'])
        image_name += 1

def getOpponentCardArea(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select opponent_stack_area from screen_coordinates where screen_area = " + screen_area)
    return data[0]['opponent_stack_area']

def getOpponentCardData(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select opp.x_coordinate,opp.y_coordinate,opp.width,opp.height,opp.screen_area "
                    "from screen_coordinates as sc "
                    "inner join opponent_screen_coordinates as opp on sc.opponent_stack_area = opp.screen_area "
                    "where sc.screen_area = " + str(screen_area))
    return data