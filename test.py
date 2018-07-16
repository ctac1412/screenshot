import cv2
import numpy as np
import screen
# img_rgb = cv2.imread('ace.png')
# img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
# template = cv2.imread('cards/ace_dimonds.png',0)
# w, h = template.shape[::-1]
#
# res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
# threshold = 0.8
# loc = np.where(res >= threshold)
# if (len(loc[0]) != 0):
#     print('test')
hand = ''
for value in screen.getCards():
    try:
        img_rgb = cv2.imread('1531641212.png', 0)
        # img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(str(value['image_path']), 0)
        # w, h = template.shape[::-1]

        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.98
        loc = np.where(res >= threshold)

        if (len(loc[0]) != 0):
            hand += value['alias']
            # for pt in zip(*loc[::-1]):
            # print(value['card'] + value['alias'])

    except Exception as e:
        print(str(value['image_path']))
print(hand)




# img_rgb = cv2.imread('ace.png')
# img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
# template = cv2.imread('ace_dimonds.png',0)
# w, h = template.shape[::-1]
#
# res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
# threshold = 0.8
# loc = np.where( res >= threshold)
# if(len(loc[0]) != 0):
#     print('yes')
# else:print('no')
# for pt in zip(*loc[::-1]):
#     cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
#
# cv2.imwrite('res.png',img_rgb)