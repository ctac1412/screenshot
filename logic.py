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

images_folder = "images/"


def getDecision(hand, current_stack, current_position, screen_area, action):
    try:
        folder_name = images_folder + str(datetime.datetime.now().date())
        hand = handConverting(hand)
        stack_value = sklansky_chubukov.getValidStackValueToPush(hand)
        stack_difference = int(current_stack) - int(stack_value)
        if int(current_stack) <= int(stack_value):
            action = 'push'
            keyboard.press('q')
        elif current_position == 'button' and stack_difference in range(1,15) and int(current_stack) >= 15 and action != 'open':
            action = 'open'
            keyboard.press('o')
        # elif current_position == 'small_blind' and stack_difference in range(1,15) and int(current_stack) >= 15:
        #     if introduction.searchLimpValue(str(screen_area)) == True:
        # action = 'call'
        #         keyboard.press(action)
        #
        #         session_log.updateActionLogSession(action, str(screen_area))
        #         return
        else:
            action = 'fold'
            keyboard.press('f')
            session_log.updateActionLogSession(action, str(screen_area))
            return
        if checkBeforeUpdateAction(screen_area, folder_name) == 1:
            session_log.updateActionLogSession(action, str(screen_area))
            if action == 'open':
                session_log.updateCurrentStackLogSession(str(screen_area))
    except Exception as e:
        error_log.errorLog('getScreenData', str(e))
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
        last_stack = session_log.getLastHandFromLogSession(screen_area)[0]['current_stack']
        cur_stack.saveStackImage(screen_area, image_name, folder_name)
        if cur_stack.searchConctreteStack(screen_area, last_stack) == False:
            return 1
    except Exception as e:
        error_log.errorLog('checkBeforeUpdateAction', str(e))
        print(e)
