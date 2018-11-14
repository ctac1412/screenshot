import image_processing
import cv2
import numpy as np
import postgresql
import db_conf
import math
import time
import error_log
import datetime

def searchBar(screen_area):
    saveBarImage(screen_area, str(math.floor(time.time())), 'images/')
    path = image_processing.getLastScreen(getBarArea(str(screen_area)))
    path = path[0]['image_path']
    img_rgb = cv2.imread(path, 0)
    template_path = 'bar/red_mark.png'
    if image_processing.cvDataTemplate(template_path, img_rgb) > 0:
        return True

    return False

def getBarArea(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select action_btn_area from screen_coordinates where screen_area = " + screen_area + " and active = 1")
    return data[0]['action_btn_area']

def getBarData(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select x_coordinate,y_coordinate,width,height,screen_area from screen_coordinates "
                    "where screen_area = "  + screen_area)
    return data

def saveBarImage(screen_area, image_name, folder_name):
    try:
        folder_name = folder_name + str(datetime.datetime.now().date())
        for value in getBarData(str(getBarArea(str(screen_area)))):
            image_path = folder_name + "/" + str(getBarArea(str(screen_area))) + "/" + image_name + ".png"
            image_processing.imaging(value['x_coordinate'], value['y_coordinate'], value['width'], value['height'], image_path, value['screen_area'])
    except Exception as e:
        error_log.errorLog('red_mark', str(e))
        print(e)
