import image_processing
import datetime
import math
import time
import session_log
import logic
import postgresql
import db_conf
import keyboard

images_folder = "images/"

def actionAfterOpen(x_coordinate, y_coordinate, width, height, image_path, screen_area, action):
    if action == 'open':
        if checkIsFold(screen_area, x_coordinate, y_coordinate, width, height, image_path): return
    if checkIsFlop(screen_area): return
    if checkIsActionButtons(screen_area): return

def saveElement(screen_area, element_name):
    folder_name = images_folder + str(datetime.datetime.now().date())
    element_area = getElementArea(screen_area, element_name)[element_name]
    for item in getElementData(element_area):
        image_name = str(math.floor(time.time()))
        image_path = folder_name + "/" + str(item['screen_area']) + "/" + image_name + ".png"
        image_processing.imaging(item['x_coordinate'], item['y_coordinate'], item['width'], item['height'], image_path,
                                 item['screen_area'])
    return element_area

def checkIsLimpAvailable(screen_area, element):
    element_area = saveElement(screen_area, 'limp_area')
    if image_processing.searchElement(element_area, element, 'limp/'):
        return True
    return False

#Проверка, есть ли карты на столе
def checkIsFlop(screen_area):
    element_area = saveElement(screen_area, 'green_board_area')
    if image_processing.searchElement(element_area, ['green_board'], 'green_board/') is False:
        print('flop')
        session_log.updateIsFlopLogSession(screen_area)
        return True

#Проверка, есть ли кнопка "Raise To"
def checkIsActionButtons(screen_area):
    row = session_log.getLastRowFromLogSession(screen_area)
    reaction_to_opponent = getReactionToOpponent(row)[0]['reaction_to_opponent']
    last_opponnet_action = image_processing.searchLastOpponentAction(screen_area)
    if not isinstance(last_opponnet_action, str):
        bb_count = last_opponnet_action['alias']
        if reaction_to_opponent == 'fold' and bb_count == '1':
            reaction_to_opponent = 'call'
    if reaction_to_opponent == 'push':
        keyboard.press('q')
    elif reaction_to_opponent == 'call':
        keyboard.press('c')
    else:
        keyboard.press('f')
    session_log.updateActionLogSession(reaction_to_opponent, str(screen_area))



#Проверка, слелали ли противники фолд
def checkIsFold(screen_area, x_coordinate, y_coordinate, width, height, image_path):
    last_hand = session_log.getLastRowFromLogSession(str(screen_area))[0]['hand']
    image_processing.imaging(x_coordinate, y_coordinate, width, height, image_path, str(screen_area))
    cur_hand = image_processing.searchCards(str(screen_area), image_processing.getCards(), 4, 1)
    if last_hand != cur_hand:
        session_log.updateActionLogSession('end', screen_area)
        return True

def getElementArea(screen_area, element):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select " + element + " from screen_coordinates where screen_area = " + str(screen_area) + " and active = 1")
    return data[0]

def getElementData(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select x_coordinate,y_coordinate,width,height,screen_area from screen_coordinates "
                    "where active = 1 and screen_area = " + str(screen_area))
    return data

def getReactionToOpponent(row):
    db = postgresql.open(db_conf.connectionString())
    hand = logic.handConverting(row[0]['hand'])
    stack = logic.convertStack(int(row[0]['current_stack']))
    last_opponent_action = row[0]['last_opponent_action']
    if last_opponent_action is None:
        last_opponent_action = ' is null'
    else:
        last_opponent_action = " = '" + last_opponent_action + '\''
    data = db.query("select trim(reaction_to_opponent) as reaction_to_opponent from preflop_chart "
                    "where hand = '" + hand + '\'' + " and position = '" + row[0]['current_position'] + '\'' +
                    " and is_headsup = '" + str(row[0]['is_headsup']) + '\'' + " and opponent_last_action" +
                    last_opponent_action + ' and stack = ' + str(stack) + " and action = '" + row[0]['action'] + '\'')
    return data


