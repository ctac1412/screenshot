import current_stack
import image_processing
import db_query
import error_log


def check_is_call_valid(screen_area, hand_value, element, stack_collection, db):
    try:
        cur_stack = current_stack.search_current_stack(screen_area, stack_collection, db)
        bank_size = current_stack.search_bank_stack(screen_area, db)
        call_size = image_processing.search_last_opponent_action(screen_area, db)
        if not isinstance(call_size, str):
            call_size = call_size['alias']
        else:
            call_size = current_stack.search_allin_stack(screen_area, db)
        if call_size == '0.5':
            call_size = float(call_size)
        elif call_size == 'check':
            call_size = 0
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
    except Exception as e:
        error_log.error_log('check_is_call_valid', str(e))


def check_is_call_after_opponent_river_agression(screen_area, hand_value, stack_collection, action, db):
    try:
        cur_stack = current_stack.search_current_stack(screen_area, stack_collection, db)
        bank_size = current_stack.search_bank_stack(screen_area, db)
        call_size = image_processing.search_last_opponent_action(screen_area, db)
        if not isinstance(call_size, str):
            call_size = call_size['alias']
        else:
            call_size = 5
        if call_size == '0.5':
            call_size = float(call_size)
        elif call_size == 'check':
            call_size = 0
        else:
            call_size = int(call_size)
        if action == 'river_cbet' and cur_stack > bank_size and call_size not in ('0.5', '1', '2', '3', '4') \
                and hand_value in ('low_two_pairs', 'two_pairs', 'top_pair', 'low_top_pair'):
            print(hand_value)
            return False
        elif action == 'river_cbet' and cur_stack > bank_size and call_size in ('0.5', '1', '2', '3', '4') \
                and hand_value in ('low_two_pairs', 'two_pairs', 'top_pair', 'low_top_pair'):
            return True
        else:
            return None
    except Exception as e:
        error_log.error_log('check_is_call_after_opponent_river_agression', str(e))

