import current_stack
import image_processing
import db_query


def check_is_call_valid(screen_area, hand_value, element, stack_collection, db):
    cur_stack = current_stack.search_current_stack(screen_area, stack_collection, db)
    bank_size = current_stack.search_bank_stack(screen_area, db)
    call_size = image_processing.search_last_opponent_action(screen_area, db)
    if not isinstance(call_size, str):
        call_size = call_size['alias']
    else:
        return False
    if call_size == '0.5':
        call_size = float(call_size)
    else:
        call_size = int(call_size)
    current_pot_odds = round(bank_size / call_size, 1)
    if cur_stack <= call_size:
        element = 'river'
    necessary_pot_odds = db_query.get_pot_odds(hand_value, element, db)
    if int(current_pot_odds) >= int(necessary_pot_odds):
        return True
    else:
        return False


def check_is_call_after_opponent_river_agression(screen_area, hand_value, stack_collection, action, db):
    cur_stack = current_stack.search_current_stack(screen_area, stack_collection, db)
    bank_size = current_stack.search_bank_stack(screen_area, db)
    call_size = image_processing.search_last_opponent_action(screen_area, db)
    if not isinstance(call_size, str):
        call_size = call_size['alias']
    else:
        return False
    if call_size == '0.5':
        call_size = float(call_size)
    else:
        call_size = int(call_size)
    if action == 'river_cbet' and cur_stack > bank_size and call_size not in ('1', '2', '3') \
            and hand_value in ('low_two_pairs', 'two_pairs', 'top_pair', 'low_top_pair'):
        return False
    elif action == 'river_cbet' and cur_stack > bank_size and call_size in ('1', '2', '3') \
            and hand_value in ('low_two_pairs', 'two_pairs', 'top_pair', 'low_top_pair'):
        return True

