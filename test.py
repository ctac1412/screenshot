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
# screen_area = '1'
# hand = '8s7d7c8c'
# print(hand)
# # session_log.updateHandAfterFlop(screen_area, hand)
# hand_value = flop.checkPair(hand, screen_area)
# print(hand_value)
# if hand_value != True:
#     hand_value = flop.checkFlushDraw(hand, screen_area, hand_value)
#     print(hand_value)
# if hand_value != True:
#     print(hand_value)
#     flop.checkStraightDraw(hand,screen_area, hand_value)
# hand_value = session_log.getHandValue(screen_area)
#
# lst = ['top_pair', 'two_pairs', 'set', 'flush', 'straight']
# print(hand_value in lst )
# if hand_value in lst:
#     print(1)
# is_headsup = 0
# if is_headsup == 0 and hand_value in ['top_pair', 'two_pairs', 'set', 'flush', 'straight']:
#     keyboard.press('b')
#     session_log.updateActionLogSession('cbet', str(screen_area))
#     session_log.updateActionLogSession('push', str(screen_area))
# elif is_headsup == 1 and hand_value.find('.') != -1 or \
#         hand_value in ['top_pair', 'two_pairs', 'set', 'flush', 'straight', 'middle_pair', 'straight_draw',
#                        'flush_draw']:
#     keyboard.press('b')
#     session_log.updateActionLogSession('cbet', str(screen_area))
# elif hand_value in ['trash']:
#     keyboard.press('f')
#     session_log.updateActionLogSession('fold', str(screen_area))
# print(hand_value)