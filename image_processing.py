import os
import datetime
import cv2
import numpy as np
import postgresql
from PIL import ImageGrab
import error_log
import db_query
import introduction

IMAGES_FOLDER = "images"


def search_cards(screen_area, deck, list_length, db):
    hand = ''
    try:
        for item in db_query.get_last_screen(screen_area, db):
            path = item['image_path']
            img_rgb = cv2.imread(path, 0)
            for value in deck:
                if cv_data_template(value['image_path'], img_rgb) > 0:
                    hand += value['alias']
                if len(hand) == list_length:
                    return hand
    except Exception as e:
        error_log.error_log('searchCards', str(e))
        print(e)
    if len(hand) < 4 and list_length > 2:
        print(hand)
        hand = '7h2d'
    return hand


def check_is_folder_exist():
    folder_name = os.path.join(IMAGES_FOLDER, str(datetime.datetime.now().date()))
    if not os.path.exists(str(folder_name)):
        os.makedirs(str(folder_name))
    db = postgresql.open(db_query.connection_string())
    data = db.query("select screen_area from screen_coordinates "
                    "union select screen_area from opponent_screen_coordinates")
    for value in data:
        if not os.path.exists(str(folder_name) + "/" + str(value['screen_area'])):
            os.makedirs(str(folder_name) + "/" + str(value['screen_area']))


def made_screenshot(x_coordinate, y_coordinate, width, height):
    image = ImageGrab.grab(bbox=(x_coordinate, y_coordinate, width, height))
    return image


def imaging(x_coordinate, y_coordinate, width, height, image_path, screen_area, db):
    image = made_screenshot(x_coordinate, y_coordinate, width, height)
    image.save(image_path, "PNG")
    db_query.insert_image_path_into_db(image_path, screen_area, db)


def search_element(screen_area, elements, folder, db):
    for item in elements:
        path = db_query.get_last_screen(screen_area, db)
        path = path[0]['image_path']
        img_rgb = cv2.imread(path, 0)
        template_path = folder + item + '.png'
        if cv_data_template(template_path, img_rgb):
            return True
        return False


def search_last_opponent_action(screen_area, db):
    element_area = introduction.save_element(screen_area, 'limp_area', db)
    path = db_query.get_last_screen(element_area, db)
    path = path[0]['image_path']
    img_rgb = cv2.imread(path, 0)
    for item in db_query.get_actions_buttons(db):
        if cv_data_template(item['image_path'], img_rgb) > 0:
            return item
    return 'push'


def check_is_cbet_available(screen_area, db):
    element_area = introduction.save_element(screen_area, 'limp_area', db)
    path = db_query.get_last_screen(element_area, db)
    path = path[0]['image_path']
    img_rgb = cv2.imread(path, 0)
    template_path = 'action_buttons/check.png'
    if cv_data_template(template_path, img_rgb) > 0:
        return True


def convert_hand(hand):
    hand = '\'' + hand[0] + hand[1] + '\'' + ',' + '\'' + hand[2] + hand[3] + '\''
    return hand


def check_current_hand(screen_area, hand, db):
    current_hand = convert_hand(hand)
    deck = db_query.get_current_cards(current_hand, db)
    if len(search_cards(screen_area, deck, 4, db)) == 4:
        return True
    else:
        return False


def cv_data_template(image_path, img_rgb):
    template = cv2.imread(str(image_path), 0)
    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.98)
    return len(loc[0])
