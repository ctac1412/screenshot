import image_processing
import cv2
import math
import time
import datetime
import error_log


def search_bar(screen_area, db):
    save_bar_image(screen_area, str(math.floor(time.time())), 'images/', db)
    path = image_processing.get_last_screen(get_bar_area(screen_area, db), db)
    path = path[0]['image_path']
    img_rgb = cv2.imread(path, 0)
    template_path = 'bar/red_mark.png'
    if image_processing.cv_data_template(template_path, img_rgb) > 0:
        return True

    return False


def get_bar_area(screen_area, db):
    sql = "select action_btn_area from screen_coordinates where screen_area = $1 and active = 1"
    data = db.query.first(sql, int(screen_area))
    return data


def get_bar_data(screen_area, db):
    sql = "select x_coordinate,y_coordinate,width,height,screen_area from screen_coordinates where screen_area = $1"
    data = db.query(sql, int(screen_area))
    return data


def save_bar_image(screen_area, image_name, folder_name, db):
    try:
        folder_name = folder_name + str(datetime.datetime.now().date())
        for value in get_bar_data(get_bar_area(screen_area, db), db):
            image_path = folder_name + "/" + str(get_bar_area(str(screen_area), db)) + "/" + image_name + ".png"
            image_processing.imaging(value['x_coordinate'], value['y_coordinate'], value['width'], value['height'],
                                     image_path, value['screen_area'], db)
    except Exception as e:
        error_log.error_log('red_mark', str(e))
        print(e)
