import time
import datetime
import math
import image_processing
import session_log
import logic
import keyboard
import mouse
import determine_position
import current_stack
import introduction
import bar as metka
import os
import postflop
import flop
import timeit
import headsup

# print(flop.checkFlushDraw('7c8dJc2sAs', '1', 'trash'))

# hand = '2dJdTcTd2h5hJs'
hand = '2dJd'
screen_area = '1'
# hand_value = flop.checkPair(hand, screen_area)
# if hand_value != True:
#     hand_value = flop.checkFlushDraw(hand, screen_area, hand_value)
# if hand_value != True:
#     flop.checkStraightDraw(hand, screen_area, hand_value)
# hand_value = session_log.getHandValue(screen_area)
# print(hand_value)

# print(postflop.riverAction('1', '8c7d2s7cQd2cAh', 13))


start_time = timeit.default_timer()
# session_log.checkConditionsBeforeInsert(hand, screen_area, image_processing.getStackImages())
# (session_log.checkConditionsBeforeInsert(hand, 1, image_processing.getStackImages()))
logic.getDecision(screen_area)
print(timeit.default_timer() - start_time)

