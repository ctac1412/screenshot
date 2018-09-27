import error_log
import postgresql
import db_conf
import keyboard
import session_log
import sklansky_chubukov
import time
import datetime
import math
import current_stack as cur_stack
import introduction
import image_processing

images_folder = "images/"


def getDecision(hand, current_stack, current_position, screen_area, action):
    try:
        action = getActionFromPreflopChart(screen_area)
        if action == 'push':
            keyboard.press('q')
        elif action == 'fold':
            keyboard.press('f')
        elif action == 'open':
            keyboard.press('o')
        elif action == 'call':
            keyboard.press('c')
        elif action == 'check':
            keyboard.press('h')
        session_log.updateActionLogSession(action, str(screen_area))
    except Exception as e:
        error_log.errorLog('getDecision', str(e))
        print(e)

def getIterationTimer(ui_element):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select round(extract(epoch from now() - created_at)) as seconds_left from iteration_timer where ui_element = '" + ui_element + "'")
    return data[0]['seconds_left']

def updateIterationTimer(ui_element):
    db = postgresql.open(db_conf.connectionString())
    db.query("UPDATE iteration_timer SET created_at = now() where ui_element = '" + ui_element + "'")

def handConverting(hand):
    if hand[1] == hand[3]:
        hand = hand[0] + hand[2] + 's'
    else:
        hand = hand[0] + hand[2] + 'o'
    return hand

def checkBeforeUpdateAction(screen_area, folder_name):
    try:
        image_name = str(math.floor(time.time()))
        last_stack = session_log.getLastRowFromLogSession(screen_area)[0]['current_stack']
        cur_stack.saveStackImage(screen_area, image_name, folder_name)
        if cur_stack.searchConctreteStack(screen_area, last_stack) is False:
            return True
    except Exception as e:
        error_log.errorLog('checkBeforeUpdateAction', str(e))
        print(e)

def getActionFromPreflopChart(screen_area):
    row = session_log.getLastRowFromLogSession(screen_area)
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select trim(action) as action from preflop_chart "
                    "where hand = " + row[0]['hand'] + " and position = " + row[0]['current_position'] +
                    " and opponent_last_action = " + row[0]['last_opponent_action'] + " and is_headsup = " + row[0]['is_headsup'])
    return data[0]['action']
