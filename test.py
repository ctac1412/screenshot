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
def searchCurrentStack(screen_area, stack_collection):
    try:
        for item in image_processing.getLastScreen(cs.getStackArea(screen_area)):
            print(item)
            path = item['image_path']
            img_rgb = cv2.imread(path, 0)
            for value in stack_collection:
                print(cs.getStackArea(screen_area))
                if image_processing.cvDataTemplate(value['image_path'], img_rgb) > 0:
                    current_stack = int(value['stack_value'])
                    return current_stack
        return 22
    except Exception as e:
        error_log.errorLog('searchCurrentStack', str(e))
        print(e)
def saveStackImage(screen_area, image_name, folder_name):
    try:
        for val in cs.getStackData(cs.getStackArea(screen_area)):
            print(val)
            image_path = os.path.join(folder_name, str(cs.getStackArea(screen_area)), image_name)
            print(val['x_coordinate'])
            image_processing.imaging(val['x_coordinate'], val['y_coordinate'], val['width'], val['height'], image_path,
                                     str(val['screen_area']))
    except Exception as e:
        error_log.errorLog('saveStackImage', str(e))
        print(e)
images_folder = "images/"
folder_name = images_folder + str(datetime.datetime.now().date())
def searchOpponentStack(screen_area, opponent_area, stack_collection):
    try:
        folder_name = 'images/' + str(datetime.datetime.now().date())
        cs.saveOpponentStackImage(str(screen_area), folder_name, opponent_area)
        screen_area = cs.getOpponentStackArea(screen_area)
        for item in image_processing.getLastScreen(str(screen_area)):
            path = item['image_path']
            img_rgb = cv2.imread(path, 0)
            for value in stack_collection:
                if image_processing.cvDataTemplate(value['image_path'], img_rgb) > 0:
                    opponent_stack = int(value['stack_value'])
                    return opponent_stack
        return 22
    except Exception as e:
        error_log.errorLog('searchOpponentStack', str(e))
        print(e)
print(cs.getOpponentStackArea(1))
# print(cs.getStackData(cs.getStackArea(1)))
# if hand.find('.') == -1:
#     print(1)
# print(postflop.riverAction('1', '8c7d2s7cQd2cAh', 13))

# start_time = timeit.default_timer()
# session_log.checkConditionsBeforeInsert(hand, screen_area, image_processing.getStackImages())
# (session_log.checkConditionsBeforeInsert(hand, 1, image_processing.getStackImages()))
# logic.getDecision(screen_area)