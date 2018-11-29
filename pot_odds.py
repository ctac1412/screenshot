import datetime
import math
import time
import current_stack


def get_pot_odds(hand_value, element, db):
    element = element + '_odds'
    sql = "select " + element + " from pot_odds where hand_value = $1"
    data = db.query.first(sql, str(hand_value))
    return data


def check_is_call_valid(screen_area, hand_value, element, stack_collection, db):
    image_name = str(math.floor(time.time())) + ".png"
    folder_name = "images/" + str(datetime.datetime.now().date())
    current_stack.save_stack_image(screen_area, image_name, folder_name, db)
    cur_stack = current_stack.search_current_stack(screen_area, stack_collection, db)
    bank_size = current_stack.search_bank_stack(screen_area, db)
    call_size = current_stack.search_allin_stack(screen_area, db)
    current_pot_odds = round(bank_size / call_size)
    if cur_stack <= call_size:
        element = 'river'
    necessary_pot_odds = get_pot_odds(hand_value, element, db)
    if int(current_pot_odds) >= int(necessary_pot_odds):
        return True
    else:
        return False