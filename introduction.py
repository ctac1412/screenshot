import os
import datetime
import math
import time
import image_processing
import session_log
import keyboard
import flop
import headsup
import current_stack
import determine_position
import error_log
import db_query
import sklansky_chubukov

IMAGES_FOLDER = "images"


def check_conditions_before_insert(hand, screen_area, stack_collection, image_name, folder_name, db):
    try:
        position = str(determine_position.seacrh_blind_chips(screen_area, image_name, folder_name, db))
        opponent_data = current_stack.processing_opponent_data(screen_area, stack_collection, db)
        is_headsup = opponent_data[0]
        stack = opponent_data[1]
        if position == 'button':
            is_headsup = 0
        stack = current_stack.convert_stack(stack)
        if position == 'big_blind' or (position == 'small_blind' and is_headsup == 0):
            last_opponent_action = image_processing.search_last_opponent_action(screen_area, db)
            last_opponent_action = get_last_opponent_action(position, last_opponent_action)
        else:
            last_opponent_action = None
        session_log.insert_into_log_session(screen_area, hand, db, position, str(stack), is_headsup=is_headsup,
                                            last_opponent_action=last_opponent_action)
    except Exception as e:
        error_log.error_log('checkConditionsBeforeInsert', str(e))
        print(e)


def action_after_open(x_coordinate, y_coordinate, width, height, image_path, screen_area, action, image_name,
                      folder_name, flop_deck, stack_collection, db):
    if check_is_flop(screen_area, image_name, folder_name, flop_deck, stack_collection, db): return
    if action == 'open':
        if check_is_fold(screen_area, x_coordinate, y_coordinate, width, height, image_path, db): return
        current_stack.get_actual_game_data(screen_area, stack_collection, db)
    if check_is_action_buttons(screen_area, db): return


def save_element(screen_area, element_name, db):
    element_area = db_query.get_element_area(screen_area, element_name, db)
    for item in db_query.get_element_data(element_area, db):
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
    cur_hand = image_processing.search_cards(screen_area, db_query.get_cards(db), 4, db)
    if last_hand != cur_hand:
        folder_name = IMAGES_FOLDER + '/' + str(datetime.datetime.now().date())
        image_name = str(math.floor(time.time())) + ".png"
        session_log.update_action_log_session('end', str(screen_area), db)
        current_stack.save_stack_image(screen_area, image_name, folder_name, db)
        check_conditions_before_insert(cur_hand, int(screen_area), db_query.get_stack_images(db), image_name, folder_name, db)
        get_decision(screen_area, db)
        return True


def get_reaction_to_opponent(row, db):
    hand = hand_converting(row[0]['hand'])
    stack = current_stack.convert_stack(int(row[0]['current_stack']))
    last_opponent_action = row[0]['last_opponent_action']
    position = row[0]['current_position']
    is_headsup = row[0]['is_headsup']
    action = row[0]['action']
    if last_opponent_action is None:
        last_opponent_action = ' is null'
    else:
        last_opponent_action = " = '" + last_opponent_action + '\''
    return db_query.get_reaction_to_opponent(hand, position, is_headsup, last_opponent_action, stack, action, db)


def get_last_opponent_action(position, last_opponent_action):
    if isinstance(last_opponent_action, str):
        last_opponent_action = 'push'
    elif position == 'big_blind' and last_opponent_action['alias'] == '1':
        last_opponent_action = 'min_raise'
    elif position == 'big_blind' and last_opponent_action['alias'] in ('2', '3'):
        last_opponent_action = 'open'
    elif position == 'small_blind' and last_opponent_action['alias'] == '2':
        last_opponent_action = 'min_raise'
    elif position == 'small_blind' and last_opponent_action['alias'] == '3':
        last_opponent_action = 'open'
    elif last_opponent_action['alias'] in ('check', '0.5'):
        last_opponent_action = 'limp'
    else:
        last_opponent_action = 'push'
    return last_opponent_action

def get_decision(screen_area, db):
    try:
        row = get_action_from_preflop_chart(screen_area, db)
        action = row[0]
        stack = row[1]
        if action == 'push':
            keyboard.press('q')
        elif action == 'fold':
            keyboard.press('f')
        elif action == 'open':
            if int(stack) > 17:
                keyboard.press('r')
            else:
                keyboard.press('o')
        elif action == 'call':
            keyboard.press('c')
        elif action == 'check':
            keyboard.press('h')
        session_log.update_action_log_session(action, str(screen_area), db)
    except Exception as e:
        error_log.error_log('getDecision', str(e))
        print(e)


def get_action_from_preflop_chart(screen_area, db):
    row = session_log.get_last_row_from_log_session(screen_area, db)
    last_opponent_action = row[0]['last_opponent_action']
    hand = hand_converting(row[0]['hand'])
    stack = int(row[0]['current_stack'])
    position = row[0]['current_position']
    is_headsup = row[0]['is_headsup']
    if 0 < stack <= 6:
        return sklansky_chubukov.get_action(hand, stack, last_opponent_action, position, db)
    elif stack == 0:
        data = ['push']
        data.append(stack)
        return data
    if last_opponent_action is None:
        last_opponent_action = ' is null'
    else:
        last_opponent_action = " = '" + last_opponent_action + '\''
    data = db_query.get_action_from_preflop_chart(hand, position, is_headsup, last_opponent_action, stack, db)
    if len(data) == 0:
        return sklansky_chubukov.get_action(hand, stack, last_opponent_action, position, db)
    data = [data[0]['action']]
    data.append(stack)
    return data



def hand_converting(hand):
    if hand[1] == hand[3]:
        hand = hand[0] + hand[2] + 's'
    else:
        hand = hand[0] + hand[2] + 'o'
    return hand