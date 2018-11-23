import session_log
import introduction
import image_processing
import keyboard
import flop
import current_stack


def check_is_turn(screen_area, deck):
    element_area = introduction.save_element(screen_area, 'turn_area')
    if image_processing.search_element(element_area, ['turn'], 'green_board/') is False:
        if len(session_log.get_actual_hand(screen_area)) == 10:
            turn = image_processing.search_cards(element_area, deck, 2)
            session_log.update_hand_after_turn(screen_area, turn)
        last_row = session_log.get_last_row_from_log_session(str(screen_area))
        hand = last_row[0][0]
        stack = last_row[0][1]
        if turn_action(screen_area, hand, stack):
            return True
    return False


def turn_action(screen_area, hand, stack):
    opponent_reaction = image_processing.search_last_opponent_action(screen_area)
    if not isinstance(opponent_reaction, str):
        opponent_reaction = opponent_reaction['alias']
    hand_value = flop.check_pair(hand, screen_area)
    if hand_value != True:
        hand_value = flop.check_flush_draw(hand, screen_area, hand_value)
    if hand_value != True:
        flop.check_straight_draw(hand, screen_area, hand_value)
    hand_value = session_log.get_hand_value(screen_area)
    if hand_value in ('top_pair', 'two_pairs', 'set', 'flush', 'straight', 'full_house') \
            and image_processing.check_is_cbet_available(str(screen_area)):
        action = current_stack.compare_bank_with_available_stack(screen_area, image_processing.get_stack_images())
        if action == 'turn_cbet':
            keyboard.press('v')
            session_log.update_action_log_session('turn_cbet', str(screen_area))
            return True
        else:
            keyboard.press('q')
            session_log.update_action_log_session('push', str(screen_area))
            return True
    elif opponent_reaction in ('1', '2') and hand_value in (
    'top_pair', 'two_pairs', 'set', 'flush', 'straight', 'weak_top_pair', 'full_house'):
        keyboard.press('v')
        session_log.update_action_log_session('turn_cbet', str(screen_area))
        return True
    elif hand_value in ('top_pair', 'two_pairs', 'set', 'flush', 'straight', 'full_house'):
        keyboard.press('q')
        session_log.update_action_log_session('push', str(screen_area))
    elif int(stack) <= 10 and (
            hand_value in ('middle_pair', 'straight_draw', 'flush_draw', 'low_two_pairs', 'second_pair')
            or hand_value.find('.')) != -1:
        keyboard.press('q')
        session_log.update_action_log_session('push', str(screen_area))
    elif image_processing.check_is_cbet_available(str(screen_area)):
        keyboard.press('h')
        session_log.update_action_log_session('cc_postflop', str(screen_area))
        return True
    elif opponent_reaction in ('1', '2', '3') and hand_value not in ('trash', 'gutshot', 'bottom_pair'):
        keyboard.press('c')
        session_log.update_action_log_session('cc_postflop', str(screen_area))
        return True
    else:
        keyboard.press('f')
        session_log.update_action_log_session('fold', str(screen_area))
        return True


def action_after_cbet(x_coordinate, y_coordinate, width, height, image_path, screen_area, deck):
    if introduction.check_is_fold(screen_area, x_coordinate, y_coordinate, width, height, image_path): return
    if check_is_turn(screen_area, deck): return
    if check_is_raise_cbet(screen_area): return


def action_after_turn_cbet(x_coordinate, y_coordinate, width, height, image_path, screen_area, deck):
    if introduction.check_is_fold(screen_area, x_coordinate, y_coordinate, width, height, image_path): return
    if check_is_river(screen_area, deck): return
    if check_is_raise_cbet(screen_area): return


def check_is_river(screen_area, deck):
    element_area = introduction.save_element(screen_area, 'river_area')
    if image_processing.search_element(element_area, ['river'], 'green_board/') is False:
        if len(session_log.get_actual_hand(screen_area)) == 12:
            river = image_processing.search_cards(element_area, deck, 2)
            session_log.update_hand_after_turn(screen_area, river)
        last_row = session_log.get_last_row_from_log_session(str(screen_area))
        hand = last_row[0][0]
        stack = last_row[0][1]
        action = last_row[0][3]
        position = last_row[0][2]
        if river_action(screen_area, hand, stack, action, position):
            return True
    return False


def river_action(screen_area, hand, stack, action, position):
    if action in ('turn_cbet', 'river_cbet'):
        keyboard.press('q')
        session_log.update_action_log_session('push', str(screen_area))
        return True
    opponent_reaction = image_processing.search_last_opponent_action(screen_area)
    if not isinstance(opponent_reaction, str):
        opponent_reaction = opponent_reaction['alias']
    hand_value = flop.check_pair(hand, screen_area)
    if hand_value != True:
        hand_value = flop.check_flush_draw(hand, screen_area, hand_value)
    if hand_value != True:
        flop.check_straight_draw(hand, screen_area, hand_value)
    hand_value = session_log.get_hand_value(screen_area)
    if hand_value == 'trash':
        keyboard.press('f')
        session_log.update_action_log_session('fold', str(screen_area))
        return True
    elif hand_value in ('top_pair', 'two_pairs', 'set', 'flush', 'straight', 'weak_top_pair', 'full_house') \
            and image_processing.check_is_cbet_available(str(screen_area)):
        keyboard.press('v')
        session_log.update_action_log_session('river_cbet', str(screen_area))
        return True
    elif hand_value in ('top_pair', 'two_pairs', 'set', 'flush', 'straight', 'full_house'):
        keyboard.press('q')
        session_log.update_action_log_session('push', str(screen_area))
        return True
    elif opponent_reaction in ('1', '2', '3') and (
            hand_value in ('middle_pair', 'low_two_pairs', 'second_pair') or hand_value.find(
            'middle_pair') != -1 or hand_value.find('low_two_pairs') or hand_value.find('second_pair')):
        keyboard.press('c')
        session_log.update_action_log_session('cc_postflop', str(screen_area))
        return True
    elif int(stack) <= 10 and hand_value in ('middle_pair', 'low_two_pairs', 'second_pair'):
        keyboard.press('q')
        session_log.update_action_log_session('push', str(screen_area))
    elif (hand_value in ('second_pair', 'low_two_pairs') or hand_value.find('second_pair') != -1 or
          hand_value.find('low_two_pairs') != -1) and image_processing.check_is_cbet_available(str(screen_area)):
        if current_stack.search_bank_stack(screen_area) <= 3:
            keyboard.press('j')
        else:
            keyboard.press('k')
        session_log.update_action_log_session('value_bet', str(screen_area))
        return True
    else:
        keyboard.press('f')
        session_log.update_action_log_session('fold', str(screen_area))
        return True


def check_is_raise_cbet(screen_area):
    hand_value = session_log.get_hand_value(screen_area)
    opponent_reaction = image_processing.search_last_opponent_action(screen_area)
    stack = session_log.get_last_row_from_log_session(screen_area)[0]['current_stack']
    if not isinstance(opponent_reaction, str):
        opponent_reaction = opponent_reaction['alias']
    if hand_value.find('.') != -1 or hand_value in ('top_pair', 'two_pairs', 'set', 'flush', 'straight', 'full_house'):
        keyboard.press('q')
        session_log.update_action_log_session('push', str(screen_area))
        return True
    elif int(stack) <= 10 and hand_value in (
    'middle_pair', 'straight_draw', 'flush_draw', 'low_two_pairs', 'second_pair', 'over_cards'):
        keyboard.press('q')
        session_log.update_action_log_session('push', str(screen_area))
        return True
    elif opponent_reaction in ('1', '2') and hand_value in (
    'middle_pair', 'straight_draw', 'flush_draw', 'low_two_pairs', 'second_pair'):
        keyboard.press('c')
        session_log.update_action_log_session('cc_postflop', str(screen_area))
        return True
    else:
        keyboard.press('f')
        session_log.update_action_log_session('fold', str(screen_area))
        return True


def action_after_cc_postflop(screen_area, deck, x_coordinate, y_coordinate, width, height, image_path):
    if check_is_river(screen_area, deck): return
    if check_is_turn(screen_area, deck): return
    if introduction.check_is_fold(screen_area, x_coordinate, y_coordinate, width, height, image_path): return
    if get_opponent_flop_reaction(screen_area): return


def get_opponent_flop_reaction(screen_area):
    hand_value = session_log.get_hand_value(screen_area)
    if hand_value is None:
        return False
    opponent_reaction = image_processing.search_last_opponent_action(screen_area)
    if not isinstance(opponent_reaction, str):
        opponent_reaction = opponent_reaction['alias']
    if opponent_reaction in ('1', '2') and hand_value not in('trash', 'gutshot', 'bottom_pair'):
        keyboard.press('c')
        session_log.update_action_log_session('cc_postflop', str(screen_area))
        return True
    else:
        keyboard.press('f')
        session_log.update_action_log_session('fold', str(screen_area))
        return True


def check_is_raise_river_value_bet(screen_area):
    opponent_reaction = image_processing.search_last_opponent_action(screen_area)
    if opponent_reaction in ('1', '2'):
        keyboard.press('c')
        session_log.update_action_log_session('end', str(screen_area))
        return True
    else:
        keyboard.press('f')
        session_log.update_action_log_session('fold', str(screen_area))
        return True


def action_after_value_bet(screen_area, x_coordinate, y_coordinate, width, height, image_path):
    if introduction.check_is_fold(screen_area, x_coordinate, y_coordinate, width, height, image_path): return
    if check_is_raise_river_value_bet(screen_area): return


def check_is_board_danger(hand):
    if len(hand) == 12:
        flush_hand = hand[5] + hand[7] + hand[9] + hand[11]
        straight_hand = hand[4] + hand[6] + hand[8] + hand[10]
        straight_hand = flop.straight_collection(straight_hand)
        if len(set(flush_hand)) == 1:
            return True
        elif list(map(int, straight_hand)) == list(range(min(straight_hand), max(straight_hand) + 1)):
            return True
    elif len(hand) == 14:
        flush_hand = hand[5] + hand[7] + hand[9] + hand[11] + hand[13]
        straight_hand = hand[4] + hand[6] + hand[8] + hand[10] + hand[12]
        straight_hand = flop.straight_collection(straight_hand)
        first_straight_hand = straight_hand[-1:]
        second_straight_hand = straight_hand[:1]
        counter = {}
        for item in flush_hand:
            counter[item] = counter.get(item, 0) + 1
        doubles = {element: count for element, count in counter.items() if count > 3}
        if len(doubles) > 0:
            return True
        elif first_straight_hand == list(range(min(first_straight_hand), max(first_straight_hand) + 1)):
            return True
        elif second_straight_hand == list(range(min(second_straight_hand), max(second_straight_hand) + 1)):
            return True
    return False
