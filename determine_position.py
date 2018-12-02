import os
import cv2
import image_processing
import db_query
import error_log


def seacrh_blind_chips(screen_area, image_name, folder_name, db):
    save_blind_image(screen_area, image_name, folder_name, db)
    blinds = ('big_blind', 'small_blind')
    path = db_query.get_last_screen(db_query.get_blind_area(screen_area, db), db)
    path = path[0]['image_path']
    img_rgb = cv2.imread(path, 0)
    for blind in blinds:
        template_path = 'blinds/' + blind + '.png'
        if image_processing.cv_data_template(template_path, img_rgb) > 0:
            return blind
    return 'button'


def save_blind_image(screen_area, image_name, folder_name, db):
    try:
        for value in db_query.get_blind_data(db_query.get_blind_area(screen_area, db), db):
            image_path = os.path.join(folder_name, str(db_query.get_blind_area(str(screen_area), db)), image_name)
            image_processing.imaging(value['x_coordinate'], value['y_coordinate'], value['width'], value['height'],
                                     image_path, value['screen_area'], db)
    except Exception as e:
        error_log.error_log('saveBlindImage', str(e))
        print(e)