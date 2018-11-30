import os
import math
import time
import datetime
import cv2
import image_processing
import error_log
import session_log

DEFAULT_STACK = 22


def search_current_stack(screen_area, stack_collection, db):
    try:
        image_name = str(math.floor(time.time())) + ".png"
        folder_name = "images/" + str(datetime.datetime.now().date())
        save_stack_image(screen_area, image_name, folder_name, db)
        for item in image_processing.get_last_screen(get_stack_area(screen_area, db), db):
            path = item['image_path']
            img_rgb = cv2.imread(path, 0)
            for value in stack_collection:
                if image_processing.cv_data_template(value['image_path'], img_rgb) > 0:
                    current_stack = int(value['stack_value'])
                    return current_stack
        return DEFAULT_STACK
    except Exception as e:
        error_log.error_log('searchCurrentStack', str(e))
        print(e)


def search_opponent_stack(screen_area, opponent_area, stack_collection, db):
    try:
        folder_name = 'images/' + str(datetime.datetime.now().date())
        save_opponent_stack_image(screen_area, folder_name, opponent_area, db)
        screen_area = get_opponent_stack_area(screen_area, db)
        for item in image_processing.get_last_screen(screen_area, db):
            path = item['image_path']
            img_rgb = cv2.imread(path, 0)
            for value in stack_collection:
                if image_processing.cv_data_template(value['image_path'], img_rgb) > 0:
                    opponent_stack = int(value['stack_value'])
                    return opponent_stack
        return DEFAULT_STACK
    except Exception as e:
        error_log.error_log('searchOpponentStack', str(e))
        print(e)


def get_stack_area(screen_area, db):
    sql = "select stack_area from screen_coordinates where screen_area = $1"
    data = db.query.first(sql, int(screen_area))
    return data


def get_opponent_stack_area(screen_area, db):
    sql = "select opponent_stack_area from screen_coordinates where screen_area = $1"
    data = db.query.first(sql, int(screen_area))
    return data


def get_stack_images(db):
    data = db.query("select trim(image_path) as image_path, stack_value from stack where active = 1 order by id desc")
    return data


def get_stack_data(screen_area, db):
    sql = "select x_coordinate,y_coordinate,width,height,screen_area from screen_coordinates where screen_area = $1"
    data = db.query(sql, screen_area)
    return data


def get_opponent_stack_data(screen_area, opponent_area, db):
    sql = "select opp.x_coordinate,opp.y_coordinate,opp.width,opp.height,opp.screen_area " \
          "from screen_coordinates as sc inner join opponent_screen_coordinates as opp " \
          "on sc.opponent_stack_area = opp.screen_area " \
          "where sc.screen_area = $1 and opp.opponent_area = $2"
    data = db.query(sql, int(screen_area), int(opponent_area))
    return data


def save_stack_image(screen_area, image_name, folder_name, db):
    try:
        for val in get_stack_data(get_stack_area(screen_area, db), db):
            image_path = os.path.join(folder_name, str(get_stack_area(screen_area, db)), image_name)
            image_processing.imaging(val['x_coordinate'], val['y_coordinate'], val['width'], val['height'], image_path,
                                     str(val['screen_area']), db)
    except Exception as e:
        error_log.error_log('saveStackImage', str(e))
        print(e)


def save_opponent_stack_image(screen_area, folder_name, opponent_area, db):
    image_name = int(math.floor(time.time()))
    for val in get_opponent_stack_data(screen_area, opponent_area, db):
        image_path = folder_name + "/" + str(val['screen_area']) + "/" + str(image_name) + ".png"
        image_processing.imaging(val['x_coordinate'], val['y_coordinate'], val['width'], val['height'], image_path,
                                 str(val['screen_area']), db)
        image_name += 1


def get_allin_stack_area(screen_area, db):
    sql = "select all_in_stack_area from screen_coordinates where screen_area = $1"
    data = db.query.first(sql, int(screen_area))
    return data


def save_allin_stack_image(screen_area, db):
    try:
        image_name = str(math.floor(time.time())) + ".png"
        folder_name = 'images/' + str(datetime.datetime.now().date())
        for val in get_stack_data(get_allin_stack_area(screen_area, db), db):
            image_path = os.path.join(folder_name, str(get_allin_stack_area(screen_area, db)), image_name)
            image_processing.imaging(val['x_coordinate'], val['y_coordinate'], val['width'], val['height'], image_path,
                                     val['screen_area'], db)
    except Exception as e:
        error_log.error_log('saveAllinStackImage', str(e))
        print(e)


def search_allin_stack(screen_area, db):
    try:
        save_allin_stack_image(screen_area, db)
        screen_area = get_allin_stack_area(screen_area, db)
        for item in image_processing.get_last_screen(screen_area, db):
            path = item['image_path']
            img_rgb = cv2.imread(path, 0)
            for value in image_processing.get_allin_stack_images(db):
                if image_processing.cv_data_template(value['image_path'], img_rgb) > 0:
                    all_in_stack = int(value['stack_value'])
                    return all_in_stack
        return DEFAULT_STACK
    except Exception as e:
        error_log.error_log('searchAllinStack', str(e))
        print(e)


def get_bank_stack_area(screen_area, db):
    sql = "select bank_stack_area from screen_coordinates where screen_area = $1"
    data = db.query.first(sql, int(screen_area))
    return data


def save_bank_stack_image(screen_area, db):
    try:
        image_name = str(math.floor(time.time())) + ".png"
        folder_name = 'images/' + str(datetime.datetime.now().date())
        for val in get_stack_data(get_bank_stack_area(screen_area, db), db):
            image_path = os.path.join(folder_name, str(get_bank_stack_area(screen_area, db)), image_name)
            image_processing.imaging(val['x_coordinate'], val['y_coordinate'], val['width'], val['height'], image_path,
                                     val['screen_area'], db)
    except Exception as e:
        error_log.error_log('saveAllinStackImage', str(e))
        print(e)


def search_bank_stack(screen_area, db):
    try:
        save_bank_stack_image(screen_area, db)
        screen_area = get_bank_stack_area(screen_area, db)
        for item in image_processing.get_last_screen(screen_area, db):
            path = item['image_path']
            img_rgb = cv2.imread(path, 0)
            for value in image_processing.get_bank_stack_images(db):
                if image_processing.cv_data_template(value['image_path'], img_rgb) > 0:
                    bank_stack = int(value['stack_value'])
                    return bank_stack
        return DEFAULT_STACK
    except Exception as e:
        error_log.error_log('searchBankStack', str(e))
        print(e)


def compare_bank_with_available_stack(screen_area, stack_collection, db):
    stack = search_current_stack(screen_area, stack_collection, db)
    bank = search_bank_stack(screen_area, db)
    if stack >= bank:
        return 'turn_cbet'
    elif stack < bank:
        return 'push'


def convert_stack(stack):
    if stack >= 22:
        stack = 22
    elif stack in range(17, 22):
        stack = 21
    elif stack in range(13, 17):
        stack = 17
    elif stack in range(10, 13):
        stack = 13
    elif stack in range(7, 10):
        stack = 10
    elif stack == 0:
        stack = 0
    return stack


def get_actual_stack(screen_area, stack_collection, db):
    stack = search_current_stack(screen_area, stack_collection, db)
    stack = convert_stack(stack)
    session_log.update_current_stack_log_session(str(screen_area), str(stack), db)
    return stack
