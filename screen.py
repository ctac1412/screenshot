from PIL import Image, ImageGrab
import time
import datetime
import math
import image_processing
import session_log
import logic
import keyboard
import mouse
import end_game
import sitout
import determine_position
import current_stack
import btn_open
import flop

images_folder = "images/"

def start():
    folder_name = images_folder + str(datetime.datetime.now().date())
    for item in image_processing.getScreenData():
        # if logic.getIterationTimer("register_button") >= 40:
        #     end_game.checkIsGameEnd()
        # if logic.getIterationTimer("sitout_button") >= 30:
        #     sitout.checkIsSitout()
        image_name = str(math.floor(time.time()))
        image_path = folder_name + "/" + str(item['screen_area']) + "/" + image_name + ".png"
        # Делаем скрин указанной области экрана
        image = ImageGrab.grab(bbox=(item['x_coordinate'], item['y_coordinate'], item['width'], item['height']))
        # Сохраняем изображение на жестком диске
        image.save(image_path, "PNG")
        # Сохраняем инфо в бд
        image_processing.insertImagePathIntoDb(image_path, item['screen_area'])
        #перемещаем курсор на рабочую область
        mouse.moveMouse(item['x_mouse'],item['y_mouse'])
        hand = image_processing.searchPlayerHand(str(item['screen_area']))
        # Если последняя строка для текущей области имеет конечный статус
        if session_log.getLastRowActionFromLogSession(str(item['screen_area'])) in ['push', 'fold', 'end']:
            # Сохраняем скрин блайндов для текущего окна
            determine_position.saveBlindImage(str(item['screen_area']), image_name, folder_name)
            # Сохраняем скрин стека для текущего окна
            current_stack.saveStackImage(str(item['screen_area']), image_name, folder_name)
            #Если рука обнаружена на скрине
            condition = session_log.checkConditionsBeforeInsert(hand,(item['screen_area']))
            if condition != False:
                print(condition)
                logic.getDecision(condition[0]['hand'], condition[0]['current_stack'],condition[0]['current_position'], item['screen_area'])
        # Если Если последняя строка для текущей области имеет статус open
        elif session_log.getLastRowActionFromLogSession(str(item['screen_area'])) == 'open':
            btn_open.actionAfterOpen(str(item['screen_area']), image_name, folder_name)
        # Если Если последняя строка для текущей области имеет статус flop
        elif session_log.getLastRowActionFromLogSession(str(item['screen_area'])) == 'flop':
            if flop.makeFlopDecision(str(item['screen_area']),hand) == True:
                keyboard.push()
                session_log.updateActionLogSession('push', str(item['screen_area']))
            else:
                keyboard.checkFold()
                session_log.updateActionLogSession('fold', str(item['screen_area']))
        # Если статус null или не конечный
        else:
            #Получаем руку из последней записи и нажимаем соответствующий хоткей. Обновляем action
            # Получаем руку из последней записи
            hand = session_log.getLastHandFromLogSession(str(item['screen_area']))
            logic.getDecision(hand[0]['hand'], hand[0]['current_stack'], hand[0]['current_position'],item['screen_area'])
