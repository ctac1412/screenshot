import db_conf
import postgresql
import image_processing
import cv2
import numpy as np
import math
import time
import datetime
import current_stack

def searchOpponentCard(screen_area, stack_collection=0, is_postflop=False):
    try:
        folder_name = 'images/' + str(datetime.datetime.now().date())
        opponent_area = saveOpponentCardImage(str(screen_area), folder_name)[0]
        check_is_headsup = 0
        card_area = getOpponentCardArea(str(screen_area))
        opponent_data = []
        last_screen = image_processing.getLastScreen(card_area, '2')
        last_screen = last_screen[::-1]
        for item in last_screen:
            path = item['image_path']
            img_rgb = cv2.imread(path, 0)
            template = cv2.imread('is_headsup/is_headsup.png', 0)
            res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.98
            loc = np.where(res >= threshold)
            if len(loc[0]) != 0:
                check_is_headsup += 1
                if is_postflop is False:
                    opponent_data.append(current_stack.searchOpponentStack(screen_area, opponent_area, stack_collection))
            opponent_area += 1
        if check_is_headsup != 1:
            check_is_headsup = 0
        opponent_data.insert(0, check_is_headsup)
        return opponent_data
    except Exception as e:
        print(e)

def saveOpponentCardImage(screen_area, folder_name):
    image_name = int(math.floor(time.time()))
    opponent_area = []
    for val in getOpponentCardData(str(screen_area)):
        image_path = folder_name + "/" + str(val['screen_area']) + "/" + str(image_name) + ".png"
        image_processing.imaging(val['x_coordinate'], val['y_coordinate'], val['width'], val['height'], image_path, val['screen_area'])
        image_name += 1
        opponent_area.append(val['opponent_area'])
    return opponent_area

def getOpponentCardArea(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select headsup_area from screen_coordinates where screen_area = " + screen_area)
    return data[0]['headsup_area']

def getOpponentCardData(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select opp.x_coordinate,opp.y_coordinate,opp.width,opp.height,opp.screen_area,opp.opponent_area "
                    "from screen_coordinates as sc "
                    "inner join opponent_screen_coordinates as opp on sc.headsup_area = opp.screen_area "
                    "where sc.screen_area = " + str(screen_area) + " order by opp.opponent_area")
    return data
