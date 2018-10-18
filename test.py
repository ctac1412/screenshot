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

# hand_value = flop.checkPair('3d6d6s5cQh', '2')
#
# if hand_value == True:
#     print('true')
# print(flop.checkPair('3d6d6s5cQh', '2'))
screen_area = '1'
hand = '3d6d4s5d7h'
hand_value = flop.checkPair(hand, screen_area)
if hand_value != True:
    hand_value = flop.checkFlushDraw(hand, screen_area, hand_value)
if hand_value != True:
    flop.checkStraightDraw(hand,screen_area, hand_value)
