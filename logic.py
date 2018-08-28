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

images_folder = "images/"


def getDecision(hand, current_stack, current_position, screen_area, action):
    try:
        folder_name = images_folder + str(datetime.datetime.now().date())
        hand = handConverting(hand)
        stack_value = sklansky_chubukov.getValidStackValueToPush(hand)
        stack_difference = int(current_stack) - int(stack_value)
        print(stack_difference)
        print(current_position)
        if current_position == 'button' and stack_difference >= 1 and stack_difference <= 25 and action != 'open':
            print('open')
            keyboard.open()
            folder_name = images_folder + str(datetime.datetime.now().date())
            action = 'open'
        elif int(current_stack) <= int(stack_value):
            print('push')
            keyboard.push()
            action = 'push'
        else:
            print('fold')
            keyboard.checkFold()
            action = 'fold'
        if action == 'fold':
            session_log.updateActionLogSession(action, str(screen_area))
        if checkBeforeUpdateAction(screen_area, folder_name) == 1 and action != 'fold':
            session_log.updateActionLogSession(action, str(screen_area))
            if action == 'open':
                session_log.updateCurrentStackLogSession(str(screen_area))
    except Exception as e:
        error_log.errorLog('getScreenData',e)
        print(e)

def pocketBroadway(hand):
    val = ''
    broadway = ['A', 'K', 'Q', 'J', 'T']
    for value in hand:
        if value.isupper():
            val += value
    try:
        if val[0] in broadway and val[1] in broadway:
            return 1
        else:
            return 0
    except:
        return 0

def pocketPair(hand):
    val = ''
    for c in hand:
        if c.isupper() or c.isdigit():
            val += c
    if val[0] == val[1]:
        return 1
    else:
        return 0

def anyAce(hand):
    val = ''
    for c in hand:
        if c.isupper() or c.isdigit():
            val += c
    if val[0] == 'A' or val[1] == 'A':
        return 1
    else:
        return 0

def suitedConnectors(hand):
    arr = ['K', 'Q', 'J', 'T', '9', '8', '7']
    if hand[1] == hand[3]:
        if hand[0] in arr and hand[2] in arr:
            return 1

def getIterationTimer(ui_element):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select round(extract(epoch from now() - created_at)) as seconds_left from iteration_timer where ui_element = '" + ui_element + "'")
    return data[0]['seconds_left']

def updateIterationTimer(ui_element):
    db = postgresql.open(db_conf.connectionString())
    db.query("UPDATE iteration_timer SET created_at = now() where ui_element = '" + ui_element + "'")

def openRange(hand):
    suitedConnectors(hand)
    return 0

def handConverting(hand):
    if hand[1] == hand[3]:
        hand = hand[0] + hand[2] + 's'
    else:
        hand = hand[0] + hand[2] + 'o'
    return hand

def checkBeforeUpdateAction(screen_area, folder_name):
    try:
        image_name = str(math.floor(time.time()))
        last_stack = session_log.getLastHandFromLogSession(screen_area)[0]['current_stack']
        cur_stack.saveStackImage(screen_area, image_name, folder_name)
        curr_stack = cur_stack.searchCurrentStack(screen_area)
        if int(last_stack) != int(curr_stack):
            return 1
    except Exception as e:
        error_log.errorLog('checkBeforeUpdateAction',e)
        print(e)
