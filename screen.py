import os
import time
import datetime
import math
import postgresql
import image_processing
import session_log
import logic
import mouse
import determine_position
import current_stack
import introduction
import bar as metka
import postflop
import db_conf

IMAGES_FOLDER = "images/"
FOLDER_NAME = IMAGES_FOLDER + str(datetime.datetime.now().date())
DB = postgresql.open(db_conf.connection_string())
SCREEN_DATA = image_processing.get_screen_data(DB)
DECK = image_processing.get_cards(DB)
STACK_COLLECTION = image_processing.get_stack_images(DB)


def start():
    for item in SCREEN_DATA:
        mouse.move_mouse(item['x_mouse'], item['y_mouse'])
        if metka.search_bar(item['screen_area'], DB):
            image_name = str(math.floor(time.time())) + ".png"
            image_path = os.path.join(IMAGES_FOLDER, str(datetime.datetime.now().date()), str(item['screen_area']),
                                      image_name)
            last_row_action = session_log.get_last_row_action_from_log_session(item['screen_area'], DB)
            if last_row_action in ('push', 'fold', 'end'):
                image_processing.imaging(item['x_coordinate'], item['y_coordinate'], item['width'], item['height'],
                                         image_path, item['screen_area'], DB)
                hand = image_processing.search_cards(item['screen_area'], DECK, 4, DB)
                session_log.check_conditions_before_insert(hand, item['screen_area'], STACK_COLLECTION, image_name, FOLDER_NAME, DB)
                logic.get_decision(item['screen_area'], DB)
            elif last_row_action in ('open', 'call', 'check'):
                introduction.action_after_open(item['x_coordinate'], item['y_coordinate'], item['width'],
                                               item['height'],
                                               image_path, item['screen_area'], last_row_action, image_name,
                                               FOLDER_NAME, DECK, STACK_COLLECTION, DB)
            elif last_row_action == 'cbet':
                postflop.action_after_cbet(item['x_coordinate'], item['y_coordinate'], item['width'], item['height'],
                                           image_path, item['screen_area'], DECK, STACK_COLLECTION, FOLDER_NAME, DB)
            elif last_row_action in ('turn_cbet', 'river_cbet'):
                postflop.action_after_turn_cbet(item['x_coordinate'], item['y_coordinate'], item['width'],
                                                item['height'],
                                                image_path, item['screen_area'], DECK, STACK_COLLECTION, DB)
            elif last_row_action == 'cc_postflop':
                postflop.action_after_cc_postflop(item['screen_area'], DECK, item['x_coordinate'],
                                                  item['y_coordinate'],
                                                  item['width'], item['height'], image_path, STACK_COLLECTION, DB)
            elif last_row_action == 'value_bet':
                postflop.action_after_value_bet(item['screen_area'], item['x_coordinate'], item['y_coordinate'],
                                                item['width'], item['height'], image_path, DB)
            else:
                hand = session_log.get_last_row_from_log_session(item['screen_area'], DB)
                if image_processing.check_current_hand(item['screen_area'], hand[0]['hand'], DB):
                    logic.get_decision(str(item['screen_area']), DB)
                else:
                    print('else-end')
                    session_log.update_action_log_session('end', str(item['screen_area']), DB)
