import os
import time
import datetime
import math
import image_processing
import session_log
import logic
import mouse
import determine_position
import current_stack
import introduction
import bar as metka
import postflop

IMAGES_FOLDER = "images/"
FOLDER_NAME = IMAGES_FOLDER + str(datetime.datetime.now().date())
SCREEN_DATA = image_processing.getScreenData()
DECK = image_processing.getCards()
STACK_COLLECTION = image_processing.getStackImages()

def start():
    for item in SCREEN_DATA:
        mouse.moveMouse(item['x_mouse'],item['y_mouse'])
        if metka.searchBar(str(item['screen_area'])):
            image_name = str(math.floor(time.time())) + ".png"
            image_path = os.path.join(IMAGES_FOLDER, str(datetime.datetime.now().date()), str(item['screen_area']), image_name)
            last_row_action = session_log.getLastRowActionFromLogSession(str(item['screen_area']))
            if last_row_action in ('push', 'fold', 'end'):
                image_processing.imaging(item['x_coordinate'], item['y_coordinate'], item['width'], item['height'],
                                         image_path, item['screen_area'])
                hand = image_processing.searchCards((item['screen_area']), DECK, 4)
                determine_position.saveBlindImage(str(item['screen_area']), image_name, FOLDER_NAME)
                current_stack.saveStackImage(str(item['screen_area']), image_name, FOLDER_NAME)
                session_log.checkConditionsBeforeInsert(hand, item['screen_area'], STACK_COLLECTION)
                logic.getDecision(item['screen_area'])
            elif last_row_action in ('open', 'call', 'check'):
                introduction.actionAfterOpen(item['x_coordinate'], item['y_coordinate'], item['width'], item['height'],
                                             image_path, str(item['screen_area']), last_row_action, image_name, FOLDER_NAME, DECK, STACK_COLLECTION)
            elif last_row_action == 'cbet':
                postflop.actionAfterCbet(item['x_coordinate'], item['y_coordinate'], item['width'], item['height'],
                                         image_path, str(item['screen_area']), DECK)
            elif last_row_action in ('turn_cbet', 'river_cbet'):
                postflop.actionAfterTurnCbet(item['x_coordinate'], item['y_coordinate'], item['width'], item['height'],
                                             image_path, str(item['screen_area']), DECK)
            elif last_row_action == 'cc_postflop':
                postflop.actionAfterCCPostflop(str(item['screen_area']), DECK, item['x_coordinate'], item['y_coordinate'],
                                               item['width'], item['height'], image_path)
            elif last_row_action == 'value_bet':
                postflop.actionAfterValueBet(str(item['screen_area']), item['x_coordinate'], item['y_coordinate'],
                                               item['width'], item['height'], image_path)
            else:
                hand = session_log.getLastRowFromLogSession(str(item['screen_area']))
                if image_processing.checkCurrentHand(str(item['screen_area']), hand[0]['hand']):
                    logic.getDecision(str(item['screen_area']))
                else:
                    print('else-end')
                    session_log.updateActionLogSession('end', str(item['screen_area']))