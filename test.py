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
db = postgresql.open(db_query.connection_string())
hand = '3c6h3h4dKh5h2h'
screen_area = '3'
row = session_log.get_last_row_from_log_session(screen_area, db)
# print(row)
print(introduction.get_reaction_to_opponent(row, db)[0]['reaction_to_opponent'])
# if postflop.check_is_board_danger('2cTd2hJdTh3hJh'):
#     print(1)
# else:
#     print(0)
# print(hand_value)
# row = session_log.get_last_row_from_log_session(3)
# print(pot_odds.check_is_call_valid(3, 'flus_draw', 'turn', db_query.get_stack_images(DB), DB))