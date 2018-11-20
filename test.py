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
import timeit
import headsup
import cv2
import numpy as np
import error_log
import current_stack as cs

# print(flop.checkFlushDraw('7c8dJc2sAs', '1', 'trash'))

# hand = 'TcQcJcJsThTs9h'
hand = 'AhKd8d7d5s6cQc'
# screen_area = '1'
# hand_value = flop.checkPair(hand, screen_area)
# if hand_value != True:
#     hand_value = flop.checkFlushDraw(hand, screen_area, hand_value)
# if hand_value != True:
#     flop.checkStraightDraw(hand, screen_area, hand_value)
# hand_value = session_log.getHandValue(screen_area)
# print(hand_value)
# stack = current_stack.searchCurrentStack(3, image_processing.getStackImages())
# print(stack)
def saveOpponentCardImage(screen_area, folder_name):
    image_name = int(math.floor(time.time()))
    opponent_area = []
    for val in headsup.getOpponentCardData(str(screen_area)):
        image_path = folder_name + "/" + str(val['screen_area']) + "/" + str(image_name) + ".png"
        image_processing.imaging(val['x_coordinate'], val['y_coordinate'], val['width'], val['height'], image_path, val['screen_area'])
        image_name += 1
        opponent_area.append(val['opponent_area'])
    return opponent_area
images_folder = "images/"
folder_name = images_folder + str(datetime.datetime.now().date())
print(cs.searchAllinStack(3))
# print(cs.getStackData(cs.getStackArea(1)))
# if hand.find('.') == -1:
#     print(1)
# print(postflop.riverAction('1', '8c7d2s7cQd2cAh', 13))

# start_time = timeit.default_timer()
# session_log.checkConditionsBeforeInsert(hand, screen_area, image_processing.getStackImages())
# (session_log.checkConditionsBeforeInsert(hand, 1, image_processing.getStackImages()))
# logic.getDecision(screen_area)