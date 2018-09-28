import image_processing
import datetime
import math
import time
import session_log
import current_stack
import logic
import postgresql
import db_conf

images_folder = "images/"

def actionAfterOpen(screen_area, image_name, folder_name, action):
    if action == 'open':
        if checkIsFold(screen_area, image_name, folder_name): return
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
        session_log.updateActionLogSession('flop', screen_area)
        return True

#Проверка, есть ли кнопка "Raise To"
def checkIsActionButtons(screen_area):
    row = session_log.getLastRowFromLogSession(screen_area)
    return getReactionToOpponent(row)
    # if image_processing.searchLastOpponentAction(screen_area) == 'push':
    #     last_opponnet_action = 'push'

#Проверка, слелали ли противники фолд
def checkIsFold(screen_area, image_name, folder_name):
    last_stack = session_log.getLastRowFromLogSession(screen_area)[0]['current_stack']
    current_stack.saveStackImage(screen_area, image_name, folder_name)
    cur_stack = current_stack.searchCurrentStack(screen_area)
    if int(last_stack) != int(cur_stack):
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
    data = db.query("select trim(reaction_to_opponent) as reaction_to_opponent from preflop_chart "
                    "where hand = '" + row[0]['hand'] + '\'' + " and stack = " + row[0]['current_stack'] +
                    " and position = '" + row[0]['current_position'] + '\'' + " and opponent_last_action = '" +
                    row[0]['last_opponent_action'] + '\'' + " and action = '" + row[0]['action'] + '\'' +
                    " and is_headsup = " + row[0]['is_headsup'])
    return data


