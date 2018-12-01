import os
import datetime
import math
import time
import image_processing
import session_log
import logic
import keyboard
import flop
import headsup
import current_stack

IMAGES_FOLDER = "images"


def action_after_open(x_coordinate, y_coordinate, width, height, image_path, screen_area, action, image_name,
                      folder_name, flop_deck, stack_collection, db):
    if check_is_flop(screen_area, image_name, folder_name, flop_deck, stack_collection, db): return
    if action == 'open':
        if check_is_fold(screen_area, x_coordinate, y_coordinate, width, height, image_path, db): return
        current_stack.get_actual_game_data(screen_area, stack_collection, db)
    if check_is_action_buttons(screen_area, db): return


def save_element(screen_area, element_name, db):
    element_area = get_element_area(screen_area, element_name, db)
    for item in get_element_data(element_area, db):
        image_name = str(math.floor(time.time())) + ".png"
        image_path = os.path.join(IMAGES_FOLDER, str(datetime.datetime.now().date()), str(item['screen_area']),
                                  image_name)
        image_processing.imaging(item['x_coordinate'], item['y_coordinate'], item['width'], item['height'], image_path,
                                 item['screen_area'], db)
    return element_area


def check_is_flop(screen_area, image_name, folder_name, flop_deck, stack_collection, db):
    element_area = save_element(screen_area, 'green_board_area', db)
    if image_processing.search_element(element_area, ['green_board'], 'green_board/', db) is False:
        last_row = session_log.get_last_row_from_log_session(screen_area, db)
        hand = last_row[0][0]
        stack = last_row[0][1]
        action = last_row[0][3]
        is_headsup = last_row[0][4]
        if is_headsup == 0 and headsup.search_opponent_card(screen_area, db, is_postflop=True)[0] == 1:
            is_headsup = 1
            session_log.update_is_headsup_postflop(str(screen_area), is_headsup, db)
        if len(hand) == 4:
            if action == 'open':
                stack = current_stack.get_actual_game_data(screen_area, stack_collection, db)
            flop.make_flop_decision(screen_area, hand, image_name, folder_name, stack, action, is_headsup,
                                    flop_deck, stack_collection, db)
        else:
            session_log.update_action_log_session('end', str(screen_area), db)
        return True


def check_is_action_buttons(screen_area, db):
    row = session_log.get_last_row_from_log_session(screen_area, db)
    try:
        reaction_to_opponent = get_reaction_to_opponent(row, db)[0]['reaction_to_opponent']
        if not isinstance(reaction_to_opponent, str):
            reaction_to_opponent = 'fold'
    except:
        reaction_to_opponent = 'fold'
    last_opponnet_action = image_processing.search_last_opponent_action(screen_area, db)
    if not isinstance(last_opponnet_action, str):
        bb_count = last_opponnet_action['alias']
        if reaction_to_opponent == 'fold' and bb_count == '1' and int(row[0]['current_stack']) > 10:
            reaction_to_opponent = 'call'
        elif reaction_to_opponent == 'fold' and bb_count == '2' and int(row[0]['current_stack']) > 17:
            reaction_to_opponent = 'call'
    if reaction_to_opponent == 'push':
        keyboard.press('q')
    elif reaction_to_opponent == 'call':
        keyboard.press('c')
    else:
        keyboard.press('f')
    session_log.update_action_log_session(reaction_to_opponent, str(screen_area), db)


def check_is_fold(screen_area, x_coordinate, y_coordinate, width, height, image_path, db):
    last_hand = session_log.get_last_row_from_log_session(screen_area, db)[0]['hand']
    last_hand = last_hand[:4]
    image_processing.imaging(x_coordinate, y_coordinate, width, height, image_path, screen_area, db)
    cur_hand = image_processing.search_cards(screen_area, image_processing.get_cards(db), 4, db)
    if last_hand != cur_hand:
        folder_name = IMAGES_FOLDER + '/' + str(datetime.datetime.now().date())
        image_name = str(math.floor(time.time())) + ".png"
        session_log.update_action_log_session('end', str(screen_area), db)
        current_stack.save_stack_image(screen_area, image_name, folder_name, db)
        session_log.check_conditions_before_insert(cur_hand, int(screen_area), current_stack.get_stack_images(db), image_name, folder_name, db)
        logic.get_decision(screen_area, db)
        return True


def get_element_area(screen_area, element, db):
    sql = "select " + element + " from screen_coordinates where screen_area = $1 and active = 1"
    data = db.query.first(sql, int(screen_area))
    return data


def get_element_data(screen_area, db):
    sql = "select x_coordinate,y_coordinate,width,height,screen_area from screen_coordinates " \
          "where active = 1 and screen_area = $1"
    data = db.query(sql, int(screen_area))
    return data


def get_reaction_to_opponent(row, db):
    hand = logic.hand_converting(row[0]['hand'])
    stack = current_stack.convert_stack(int(row[0]['current_stack']))
    last_opponent_action = row[0]['last_opponent_action']
    position = row[0]['current_position']
    is_headsup = row[0]['is_headsup']
    action = row[0]['action']
    if last_opponent_action is None:
        last_opponent_action = ' is null'
    else:
        last_opponent_action = " = '" + last_opponent_action + '\''
    data = db.query("select trim(reaction_to_opponent) as reaction_to_opponent from preflop_chart "
                    "where hand = '" + hand + '\'' + " and position = '" + position + '\'' +
                    " and is_headsup = '" + str(is_headsup) + '\'' + " and opponent_last_action" +
                    last_opponent_action + ' and stack = ' + str(stack) + " and action = '" + action + '\'')
    return data
