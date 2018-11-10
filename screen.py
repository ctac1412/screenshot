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
import os
import postflop

images_folder = "images/"
folder_name = images_folder + str(datetime.datetime.now().date())
screen_data = image_processing.getScreenData()
deck = image_processing.getCards()
stack_collection = image_processing.getStackImages()

def start():
    for item in screen_data:
        mouse.moveMouse(item['x_mouse'],item['y_mouse'])
        if metka.seacrhBar(str(item['screen_area'])):
            image_name = str(math.floor(time.time())) + ".png"
            image_path = os.path.join(images_folder, str(datetime.datetime.now().date()), str(item['screen_area']), image_name)
            last_row_action = session_log.getLastRowActionFromLogSession(str(item['screen_area']))
            if last_row_action in ['push', 'fold', 'end']:
                image_processing.imaging(item['x_coordinate'], item['y_coordinate'], item['width'], item['height'],
                                         image_path, item['screen_area'])
                hand = image_processing.searchCards(str(item['screen_area']), deck, 4)
                determine_position.saveBlindImage(str(item['screen_area']), image_name, folder_name)
                current_stack.saveStackImage(str(item['screen_area']), image_name, folder_name)
                session_log.checkConditionsBeforeInsert(hand, item['screen_area'], stack_collection)
                logic.getDecision(item['screen_area'])
            elif last_row_action in ['open', 'call', 'check']:
                introduction.actionAfterOpen(item['x_coordinate'], item['y_coordinate'], item['width'], item['height'],
                                         image_path, str(item['screen_area']), last_row_action, image_name, folder_name, deck)
            elif last_row_action == 'cbet':
                postflop.actionAfterCbet(item['x_coordinate'], item['y_coordinate'], item['width'], item['height'],
                                         image_path, str(item['screen_area']), deck)
            elif last_row_action in ['turn_cbet', 'river_cbet']:
                postflop.actionAfterTurnCbet(item['x_coordinate'], item['y_coordinate'], item['width'], item['height'],
                                         image_path, str(item['screen_area']), deck)
            elif last_row_action == 'cc_postflop':
                postflop.actionAfterCCPostflop(str(item['screen_area']), deck, item['x_coordinate'], item['y_coordinate'],
                                               item['width'], item['height'], image_path)
            else:
                hand = session_log.getLastRowFromLogSession(str(item['screen_area']))
                if image_processing.checkCurrentHand(str(item['screen_area']), hand[0]['hand']):
                    logic.getDecision(str(item['screen_area']))
                else:
                    print('else-end')
                    session_log.updateActionLogSession('end', str(item['screen_area']))