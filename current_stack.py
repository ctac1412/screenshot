import os
import math
import time
import datetime
import cv2
import image_processing
import error_log
import session_log
import headsup
import db_query

DEFAULT_STACK = 22


def search_current_stack(screen_area, stack_collection, db):
    try:
        image_name = str(math.floor(time.time())) + ".png"
        folder_name = "images/" + str(datetime.datetime.now().date())
        save_stack_image(screen_area, image_name, folder_name, db)
        for item in db_query.get_last_screen(db_query.get_stack_area(screen_area, db), db):
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
        screen_area = db_query.get_opponent_stack_area(screen_area, db)
        for item in db_query.get_last_screen(screen_area, db):
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


def save_stack_image(screen_area, image_name, folder_name, db):
    try:
        for val in db_query.get_stack_data(db_query.get_stack_area(screen_area, db), db):
            image_path = os.path.join(folder_name, str(db_query.get_stack_area(screen_area, db)), image_name)
            image_processing.imaging(val['x_coordinate'], val['y_coordinate'], val['width'], val['height'], image_path,
                                     str(val['screen_area']), db)
    except Exception as e:
        error_log.error_log('saveStackImage', str(e))
        print(e)


def save_opponent_stack_image(screen_area, folder_name, opponent_area, db):
    image_name = int(math.floor(time.time()))
    for val in db_query.get_opponent_stack_data(screen_area, opponent_area, db):
        image_path = folder_name + "/" + str(val['screen_area']) + "/" + str(image_name) + ".png"
        image_processing.imaging(val['x_coordinate'], val['y_coordinate'], val['width'], val['height'], image_path,
                                 str(val['screen_area']), db)
        image_name += 1


def save_allin_stack_image(screen_area, db):
    try:
        image_name = str(math.floor(time.time())) + ".png"
        folder_name = 'images/' + str(datetime.datetime.now().date())
        for val in db_query.get_stack_data(db_query.get_allin_stack_area(screen_area, db), db):
            image_path = os.path.join(folder_name, str(db_query.get_allin_stack_area(screen_area, db)), image_name)
            image_processing.imaging(val['x_coordinate'], val['y_coordinate'], val['width'], val['height'], image_path,
                                     val['screen_area'], db)
    except Exception as e:
        error_log.error_log('saveAllinStackImage', str(e))
        print(e)


def search_allin_stack(screen_area, db):
    try:
        save_allin_stack_image(screen_area, db)
        screen_area = db_query.get_allin_stack_area(screen_area, db)
        for item in db_query.get_last_screen(screen_area, db):
            path = item['image_path']
            img_rgb = cv2.imread(path, 0)
            for value in db_query.get_allin_stack_images(db):
                if image_processing.cv_data_template(value['image_path'], img_rgb) > 0:
                    all_in_stack = int(value['stack_value'])
                    return all_in_stack
        return DEFAULT_STACK
    except Exception as e:
        error_log.error_log('searchAllinStack', str(e))
        print(e)


def save_bank_stack_image(screen_area, db):
    try:
        image_name = str(math.floor(time.time())) + ".png"
        folder_name = 'images/' + str(datetime.datetime.now().date())
        for val in db_query.get_stack_data(db_query.get_bank_stack_area(screen_area, db), db):
            image_path = os.path.join(folder_name, str(db_query.get_bank_stack_area(screen_area, db)), image_name)
            image_processing.imaging(val['x_coordinate'], val['y_coordinate'], val['width'], val['height'], image_path,
                                     val['screen_area'], db)
    except Exception as e:
        error_log.error_log('saveAllinStackImage', str(e))
        print(e)


def search_bank_stack(screen_area, db):
    try:
        save_bank_stack_image(screen_area, db)
        screen_area = db_query.get_bank_stack_area(screen_area, db)
        for item in db_query.get_last_screen(screen_area, db):
            path = item['image_path']
            img_rgb = cv2.imread(path, 0)
            for value in db_query.get_bank_stack_images(db):
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
    elif stack in range(18, 22):
        stack = 21
    elif stack in range(14, 18):
        stack = 17
    elif stack in range(11, 14):
        stack = 13
    elif stack in range(8, 11):
        stack = 10
    return stack


def get_actual_game_data(screen_area, stack_collection, db):
    row = session_log.get_last_row_from_log_session(screen_area, db)
    position = row[0]['current_position']
    hand = row[0]['hand']
    opponent_data = processing_opponent_data(screen_area, stack_collection, db)
    is_headsup = opponent_data[0]
    if position == 'button':
        is_headsup = 0
    stack = opponent_data[1]
    stack = convert_stack(stack)
    if len(hand) > 4:
        session_log.update_is_headsup_postflop(str(screen_area), is_headsup, db)
    session_log.update_current_stack_log_session(str(screen_area), str(stack), db)
    return stack


def processing_opponent_data(screen_area, stack_collection, db):
    data = []
    stack = search_current_stack(screen_area, stack_collection, db)
    opponent_data = headsup.search_opponent_card(screen_area, db, stack_collection)
    is_headsup = opponent_data[0]
    data.append(is_headsup)
    opponent_data.pop(0)
    if len(opponent_data) > 0:
        opponent_actual_stack = sorted(opponent_data, reverse=True)
        if int(opponent_actual_stack[0]) == 666:
            all_in_stack = search_allin_stack(screen_area, db)
            opponent_actual_stack[0] = all_in_stack
        opponent_actual_stack = max(opponent_actual_stack)
        if int(opponent_actual_stack) < int(stack):
            stack = opponent_actual_stack
    data.append(stack)
    return data
