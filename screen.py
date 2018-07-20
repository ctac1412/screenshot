from PIL import Image, ImageGrab
import time
import datetime
import math
import image_processing
import session_log
import pyautogui
import logic
import keyboard
import mouse

images_folder = "images/"

def start():
    folder_name = images_folder + str(datetime.datetime.now().date())
    time.sleep(2)
    for item in image_processing.getScreenData():
        image_name = str(math.floor(time.time()))
        image_path = folder_name + "/" + str(item['screen_area']) + "/" + image_name + ".png"
        # Делаем скрин указанной области экрана
        image = ImageGrab.grab(bbox=(item['x_coordinate'], item['y_coordinate'], item['width'], item['height']))
        # Сохраняем изображение на жестком диске
        image.save(image_path, "PNG")
        # Сохраняем инфо в бд
        image_processing.insertImagePathIntoDb(image_path, (item['screen_area']))

        #перемещаем курсор на рабочую область
        mouse.moveMouse(item['x_mouse'],item['y_mouse'])

        # Если последняя строка для текущей области имеет статус отличный от null
        if session_log.getLastRowActionFromLogSession(str(item['screen_area']))[0]['action'] is not None:
            hand = image_processing.searchPlayerHand(str(item['screen_area']))
            #Если рука обнаружена на скрине
            if hand != '':
                #Вставляем новую запись в session_log
                session_log.insertIntoLogSession((item['screen_area']), hand)
                # print(hand)
                time.sleep(2)
                hand = (session_log.getLastHandFromLogSession(str(item['screen_area']))[0]['hand'])
                if logic.getDecision(hand) == 1:
                    keyboard.push()
                    session_log.updateActionLogSession('push', str(item['screen_area']))
                else:
                    keyboard.checkFold()
                    session_log.updateActionLogSession('fold', str(item['screen_area']))
        # Если статус null
        # else:
        #     #Получаем руку из последней записи и нажимаем соответствующий хоткей. Обновляем action
        #     # Получаем руку из последней записи
        #     hand = (session_log.getLastHandFromLogSession(str(item['screen_area']))[0]['hand'])
        #     if logic.getDecision(hand) == 1:
        #         keyboard.push()
        #         session_log.updateActionLogSession('push', str(item['screen_area']))
        #     else:
        #         keyboard.checkFold()
        #         session_log.updateActionLogSession('fold', str(item['screen_area']))

