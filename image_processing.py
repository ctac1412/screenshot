import os
import datetime
import cv2
import numpy as np
import postgresql
from PIL import ImageGrab
import error_log
import db_conf
import introduction

IMAGES_FOLDER = "images"


def search_cards(screen_area, deck, list_length):
    hand = ''
    try:
        for item in get_last_screen(screen_area):
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


def insert_image_path_into_db(image_path, screen_area):
    try:
        db = postgresql.open(db_conf.connection_string())
        insert = db.prepare("insert into screenshots (image_path,screen_area) values($1,$2)")
        insert(image_path, int(screen_area))
    except Exception as e:
        print('insertImagePathIntoDb ' + str(e))
        error_log.error_log('insertImagePathIntoDb', str(e))


def get_screen_data():
    try:
        db = postgresql.open(db_conf.connection_string())
        data = db.query("select x_coordinate,y_coordinate,width,height,screen_area,x_mouse,y_mouse "
                        "from screen_coordinates where active = 1 and alias = 'workspace'")
        return data
    except Exception as e:
        error_log.error_log('getScreenData', str(e))


def check_is_folder_exist():
    folder_name = os.path.join(IMAGES_FOLDER, str(datetime.datetime.now().date()))
    if not os.path.exists(str(folder_name)):
        os.makedirs(str(folder_name))
    db = postgresql.open(db_conf.connection_string())
    data = db.query("select screen_area from screen_coordinates "
                    "union select screen_area from opponent_screen_coordinates")
    for value in data:
        if not os.path.exists(str(folder_name) + "/" + str(value['screen_area'])):
            os.makedirs(str(folder_name) + "/" + str(value['screen_area']))


def get_cards():
    db = postgresql.open(db_conf.connection_string())
    data = db.query("select trim(image_path) as image_path, trim(alias) as alias from cards")
    return data


def get_flop_cards():
    db = postgresql.open(db_conf.connection_string())
    data = db.query("select trim(image_path) as image_path,card,suit,trim(alias) as alias from flop_cards")
    return data


def get_stack_images():
    db = postgresql.open(db_conf.connection_string())
    data = db.query("select trim(image_path) as image_path, stack_value from stack where active = 1 order by id desc")
    return data


def get_allin_stack_images():
    db = postgresql.open(db_conf.connection_string())
    data = db.query("select trim(image_path) as image_path, stack_value from all_in_stack order by id desc")
    return data


def get_bank_stack_images():
    db = postgresql.open(db_conf.connection_string())
    data = db.query("select trim(image_path) as image_path, stack_value from bank_stack order by id desc")
    return data


def get_actions_buttons():
    db = postgresql.open(db_conf.connection_string())
    data = db.query("select trim(image_path) as image_path,trim(opponent_action) as opponent_action, "
                    "trim(alias) as alias from opponent_last_action")
    return data


def get_last_screen(screen_area, limit=1):
    db = postgresql.open(db_conf.connection_string())
    sql = "select trim(image_path)as image_path from screenshots where screen_area = $1 order by id desc limit $2"
    data = db.query(sql, int(screen_area), limit)
    return data


def get_ui_button_data(alias):
    try:
        db = postgresql.open(db_conf.connection_string())
        sql = "select x_coordinate,y_coordinate,width,height,screen_area,x_mouse,y_mouse " \
              "from screen_coordinates where active = 1 and alias = $1"
        data = db.query(sql, alias)
        return data
    except Exception as e:
        error_log.error_log('getUIButtonData', str(e))
        print(e)


def made_screenshot(x_coordinate, y_coordinate, width, height):
    image = ImageGrab.grab(bbox=(x_coordinate, y_coordinate, width, height))
    return image


def imaging(x_coordinate, y_coordinate, width, height, image_path, screen_area):
    image = made_screenshot(x_coordinate, y_coordinate, width, height)
    image.save(image_path, "PNG")
    insert_image_path_into_db(image_path, screen_area)


def search_element(screen_area, elements, folder):
    for item in elements:
        path = get_last_screen(screen_area)
        path = path[0]['image_path']
        img_rgb = cv2.imread(path, 0)
        template_path = folder + item + '.png'
        if cv_data_template(template_path, img_rgb):
            return True
        return False


def search_last_opponent_action(screen_area):
    element_area = introduction.save_element(screen_area, 'limp_area')
    path = get_last_screen(element_area)
    path = path[0]['image_path']
    img_rgb = cv2.imread(path, 0)
    for item in get_actions_buttons():
        if cv_data_template(item['image_path'], img_rgb) > 0:
            return item
    return 'push'


def check_is_cbet_available(screen_area):
    element_area = introduction.save_element(screen_area, 'limp_area')
    path = get_last_screen(element_area)
    path = path[0]['image_path']
    img_rgb = cv2.imread(path, 0)
    template_path = 'action_buttons/check.png'
    if cv_data_template(template_path, img_rgb) > 0:
        return True


def get_current_cards(condition):
    db = postgresql.open(db_conf.connection_string())
    sql = "select trim(image_path) as image_path, trim(alias) as alias from cards where alias in ($1)"
    data = db.query.first(sql, condition)
    return data


def convert_hand(hand):
    hand = '\'' + hand[0] + hand[1] + '\'' + ',' + '\'' + hand[2] + hand[3] + '\''
    return hand


def check_current_hand(screen_area, hand):
    current_hand = convert_hand(hand)
    deck = get_current_cards(current_hand)
    if len(search_cards(screen_area, deck, 4)) == 4:
        return True
    else:
        return False


def cv_data_template(image_path, img_rgb):
    template = cv2.imread(str(image_path), 0)
    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.98)
    return len(loc[0])
