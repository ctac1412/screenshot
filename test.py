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


# print(flop.checkFlushDraw('7c8dJc2sAs', '1', 'trash'))

hand = '3s8sAc7sTs9c'
screen_area = '2'
hand_value = flop.checkPair(hand, screen_area)
if hand_value != True:
    hand_value = flop.checkFlushDraw(hand, screen_area, hand_value)
if hand_value != True:
    flop.checkStraightDraw(hand, screen_area, hand_value)
hand_value = session_log.getHandValue(screen_area)
print(hand_value)


