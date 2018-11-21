import time
import datetime
import math
import image_processing
import session_log
import logic
import keyboard
import mouse
import determine_position
import introduction
import bar as metka
import os
import postflop
import flop
import current_stack
# print(flop.checkFlushDraw('7c8dJc2sAs', '1', 'trash'))

# hand = 'TcQcJcJsThTs9h'
# hand = 'TcKsJcTsAs2s'
# screen_area = '2'
# # print(flop.searchHandValue(hand, screen_area))
# hand_value = flop.check_pair(hand, screen_area)
# print(hand_value)
# if hand_value != True:
#     hand_value = flop.check_flush_draw(hand, screen_area, hand_value)
# print(hand_value)
# if hand_value != True:
#     flop.check_straight_draw(hand, screen_area, hand_value)
# hand_value = session_log.get_hand_value(screen_area)
# print(hand_value)
row = session_log.get_last_row_from_log_session(3)
print(row)
print(introduction.get_reaction_to_opponent(row)[0]['reaction_to_opponent'])