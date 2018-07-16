import cv2
import numpy as np
import screen

def searchPlayerHand(screen_area):
    hand = ''
    for value in screen.getCards():
        try:
            img_rgb = cv2.imread('1531641212.png', 0)
            template = cv2.imread(str(value['image_path']), 0)

            res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.98
            loc = np.where(res >= threshold)

            if (len(loc[0]) != 0):
                hand += value['alias']

        except Exception as e:
            print(str(value['image_path']))
    return hand