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
import flop

images_folder = "images/"
green_mark = [{'image_path':'green_board/green_mark.png', 'alias':'mark'}]

def start():
    folder_name = images_folder + str(datetime.datetime.now().date())
    for item in image_processing.getScreenData():
        image_name = str(math.floor(time.time()))
        #перемещаем курсор на рабочую область
        mouse.moveMouse(item['x_mouse'],item['y_mouse'])
        # Если последняя строка для текущей области имеет конечный статус
        last_row_action = session_log.getLastRowActionFromLogSession(str(item['screen_area']))
        if last_row_action in ['push', 'fold', 'end']:
            image_path = folder_name + "/" + str(item['screen_area']) + "/" + image_name + ".png"
            image_processing.imaging(item['x_coordinate'], item['y_coordinate'], item['width'], item['height'], image_path, item['screen_area'])
            if image_processing.searchCards(str(item['screen_area']), green_mark, 4, 1) == 'mark':
                return
            hand = image_processing.searchCards(str(item['screen_area']), image_processing.getCards(), 4, 1)
            if hand != '':
                # Сохраняем скрин блайндов для текущего окна
                determine_position.saveBlindImage(str(item['screen_area']), image_name, folder_name)
                # Сохраняем скрин стека для текущего окна
                current_stack.saveStackImage(str(item['screen_area']), image_name, folder_name)
                # Если рука обнаружена на скрине
                condition = session_log.checkConditionsBeforeInsert(hand, (item['screen_area']))
                if condition is not False:
                    logic.getDecision(condition[0], condition[1], condition[2], item['screen_area'], condition[3])
            else: return
        # Если Если последняя строка для текущей области имеет статус open
        elif last_row_action in ['open', 'call', 'check']:
            introduction.actionAfterOpen(str(item['screen_area']), image_name, folder_name, last_row_action)
        # Если Если последняя строка для текущей области имеет статус flop
        elif last_row_action == 'flop':
            flop.saveFlopImage(str(item['screen_area']), image_name, folder_name)
            hand = session_log.getLastRowFromLogSession(str(item['screen_area']))[0][0]
            if flop.makeFlopDecision(str(item['screen_area']), hand):
                keyboard.press('q')
                session_log.updateActionLogSession('push', str(item['screen_area']))
            else:
                keyboard.press('f')
                session_log.updateActionLogSession('fold', str(item['screen_area']))
        # Если статус null или не конечный
        else:
            #Получаем руку из последней записи и нажимаем соответствующий хоткей. Обновляем action
            hand = session_log.getLastRowFromLogSession(str(item['screen_area']))
            if image_processing.checkCurrentHand(str(item['screen_area']), hand[0]['hand']):
                logic.getDecision(hand[0]['hand'], hand[0]['current_stack'], hand[0]['current_position'], item['screen_area'], hand[0]['action'])
            else:
                session_log.updateActionLogSession('end', str(item['screen_area']))
