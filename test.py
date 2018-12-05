import time
import datetime
import math
import image_processing
import session_log
import keyboard
import mouse
import determine_position
import introduction
import bar as metka
import os
import postflop
import flop
import current_stack
import postgresql
import db_query
import pot_odds
import error_log
# print(flop.checkFlushDraw('7c8dJc2sAs', '1', 'trash'))
DB = postgresql.open(db_query.connection_string())
hand = '4h6h4cAs9h6c9s'
screen_area = '1'
hand_value = flop.check_pair(hand, screen_area, DB)
if hand_value != True:
    hand_value = flop.check_flush_draw(hand, screen_area, hand_value, DB)
if hand_value != True:
    flop.check_straight_draw(hand, screen_area, hand_value, DB)
hand_value = session_log.get_hand_value(screen_area, DB)
print(hand_value)
# if postflop.check_is_board_danger('2cTd2hJdTh3hJh'):
#     print(1)
# else:
#     print(0)
# print(hand_value)
# row = session_log.get_last_row_from_log_session(3)
# print(pot_odds.check_is_call_valid(3, 'flus_draw', 'turn', db_query.get_stack_images(DB), DB))