import postgresql
import db_conf
import cv2
import numpy as np
import error_log
import introduction
import mouse
import current_stack
import math
import datetime
import image_processing
import flop

hand = 0.98
# for value in image_processing.getCards():
#     path = '1536059100.png'
#     img_rgb = cv2.imread(path, 0)
#     template = cv2.imread(str(value['image_path']), 0)
#     res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
#     threshold = 0.98
#     loc = np.where(res >= threshold)
#     if len(loc[0]) != 0:
#         hand += value['alias']
#     # if len(hand) == 6:
#     #     print(hand)
#     #     break
# print(hand)

for iten in range(3):
    print(hand)
    hand -= 0.01

