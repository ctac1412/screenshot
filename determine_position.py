import os
import cv2
import postgresql
import image_processing
import db_conf
import error_log


def seacrh_blind_chips(screen_area, db):
    blinds = ('big_blind', 'small_blind')
    path = image_processing.get_last_screen(get_blind_area(screen_area), db)
    path = path[0]['image_path']
    img_rgb = cv2.imread(path, 0)
    for blind in blinds:
        template_path = 'blinds/' + blind + '.png'
        if image_processing.cv_data_template(template_path, img_rgb) > 0:
            return blind
    return 'button'


def get_blind_area(screen_area):
    db = postgresql.open(db_conf.connection_string())
    sql = "select blind_area from screen_coordinates where screen_area = $1 and active = 1"
    data = db.query.first(sql, int(screen_area))
    return data


def get_blind_data(screen_area):
    db = postgresql.open(db_conf.connection_string())
    sql = "select x_coordinate,y_coordinate,width,height,screen_area from screen_coordinates where screen_area = $1"
    data = db.query(sql, int(screen_area))
    return data


def save_blind_image(screen_area, image_name, folder_name, db):
    try:
        for value in get_blind_data(get_blind_area(screen_area)):
            image_path = os.path.join(folder_name, str(get_blind_area(str(screen_area))), image_name)
            image_processing.imaging(value['x_coordinate'], value['y_coordinate'], value['width'], value['height'],
                                     image_path, value['screen_area'], db)
    except Exception as e:
        error_log.error_log('saveBlindImage', str(e))
        print(e)
