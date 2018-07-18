# import cv2
# import numpy as np
# import screen
# import image_processing
import random

# def errorLog(module_name,error_message):
#     db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
#     insert = db.prepare("insert into error_log (module_name,error_message) values($1,$2)")
#     insert(module_name, error_message)

# print(round(random.uniform(0.2, 0.7),2))
# for item in range(10):
#     print(item)
#     while(item < 5):
#         exit()
#     print('done')
#
# import cv2
# import numpy as np
# import screen
# import postgresql
# import image_processing
# import time
# import pyautogui
# hand = ''
# for value in image_processing.getCards():
#     try:
#         img_rgb = cv2.imread('1531852180.png', 0)
#         template = cv2.imread(str(value['image_path']), 0)
#
#         res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
#         threshold = 0.98
#         loc = np.where(res >= threshold)
#
#         if (len(loc[0]) != 0):
#             hand += value['alias']
#
#     except Exception as e:
#         print('error')
# print(hand)

# for item in range(5):
#     pyautogui.press('q')
#     time.sleep(2)
# for item in image_processing.getScreenData():
    # image_name = str(math.floor(time.time()))
    # image_path = folder_name + "/" + str(item['screen_area']) + "/" + image_name + ".png"
    # # # Делаем скрин указанной области экрана
    # image = ImageGrab.grab(bbox=(item['x_coordinate'], item['y_coordinate'], item['width'], item['height']))
    # # Сохраняем изображение на жестком диске
    # image.save(image_path, "PNG")
    # # Сохраняем инфо в бд
    # image_processing.insertImagePathIntoDb(image_path, str(item['screen_area']))

    # Если последняя строка для текущей области имеет статус отличный от null
    # print(item['screen_area'])
    # hand = image_processing.searchPlayerHand(item['screen_area'])
    # if image_processing.getLastScreen(item['screen_area'] is not None):

    # Если рука обнаружена на скрине
    # if hand != '':
    #     session_log.insertIntoLogSession(str(item['screen_area']), hand)
    # print(hand)

# print(image_processing.getLastScreen(4)[0]['image_path'])
# db = postgresql.open('pq://postgres:postgres@localhost:5432/postgres')
# data = db.query("select * from screen_coordinates where screen_area = 6")
# print(data[0])
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
# hand = ''
# for value in screen.getCards():
#     try:
#         img_rgb = cv2.imread('1531641212.png', 0)
#         # img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
#         template = cv2.imread(str(value['image_path']), 0)
#         # w, h = template.shape[::-1]
#
#         res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
#         threshold = 0.98
#         loc = np.where(res >= threshold)
#
#         if (len(loc[0]) != 0):
#             hand += value['alias']
#             # for pt in zip(*loc[::-1]):
#             # print(value['card'] + value['alias'])
#
#     except Exception as e:
#         print(str(value['image_path']))
# print(hand)




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