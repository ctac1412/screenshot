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

# hand = 'As6s2d6hKc'
# flop.checkPair(hand)

hand = ''
threshold = 0.98
for item in range(4):

    hand = ''
    print(threshold)
    for value in image_processing.getCards():
        path = '1537096477.png'
        img_rgb = cv2.imread(path, 0)
        template = cv2.imread(str(value['image_path']), 0)
        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        if len(loc[0]) != 0:
            hand += value['alias']
        if len(hand) == 6:
            print(hand)
            break
    threshold -= 0.01
print(hand)
