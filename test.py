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
from urllib.request import urlopen
# print(flop.checkFlushDraw('7c8dJc2sAs', '1', 'trash'))
db = postgresql.open(db_query.connection_string())
hand = '9sTsJc5s6s7h4s'
screen_area = '1'
# print(flop.get_hand_value(hand, screen_area, db))
# row = session_log.get_last_row_from_log_session(screen_area, db)
# # print(row)
# print(postflop.check_is_board_danger('TsKdQc9sThAhAd'))
# if postflop.check_is_board_danger('2cTd2hJdTh3hJh'):
#     print(1)
# else:
#     print(0)
# print(hand_value)
# row = session_log.get_last_row_from_log_session(3)
# print(pot_odds.check_is_call_valid(3, 'flus_draw', 'turn', db_query.get_stack_images(DB), DB))
# print(postflop.check_is_four_flush_board(hand))
row = session_log.get_last_row_from_log_session(screen_area, db)
print(introduction.get_reaction_to_opponent(row, db))

