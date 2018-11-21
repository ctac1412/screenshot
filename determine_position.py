import os
import cv2
import postgresql
import image_processing
import db_conf
import error_log

def seacrhBlindChips(screen_area):
    blinds = ('big_blind', 'small_blind')
    path = image_processing.getLastScreen(getBlindArea(screen_area))
    path = path[0]['image_path']
    img_rgb = cv2.imread(path, 0)
    for blind in blinds:
        template_path = 'blinds/' + blind + '.png'
        if image_processing.cvDataTemplate(template_path, img_rgb) > 0:
            return blind
    return 'button'

def getBlindArea(screen_area):
    db = postgresql.open(db_conf.connectionString())
    sql = "select blind_area from screen_coordinates where screen_area = $1 and active = 1"
    data = db.query.first(sql, int(screen_area))
    return data

def getBlindData(screen_area):
    db = postgresql.open(db_conf.connectionString())
    sql = "select x_coordinate,y_coordinate,width,height,screen_area from screen_coordinates where screen_area = $1"
    data = db.query(sql, int(screen_area))
    return data

def saveBlindImage(screen_area,image_name,folder_name):
    try:
        for value in getBlindData(str(getBlindArea(str(screen_area)))):
            image_path = os.path.join(folder_name, str(getBlindArea(str(screen_area))), image_name)
            image_processing.imaging(value['x_coordinate'], value['y_coordinate'], value['width'], value['height'],
                                     image_path, value['screen_area'])
    except Exception as e:
        error_log.errorLog('saveBlindImage', str(e))
        print(e)
