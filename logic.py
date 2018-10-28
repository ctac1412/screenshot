import error_log
import postgresql
import db_conf
import keyboard
import session_log
import sklansky_chubukov

images_folder = "images/"


def getDecision(screen_area):
    try:
        action = getActionFromPreflopChart(str(screen_area))
        if action == 'push':
            keyboard.press('q')
        elif action == 'fold':
            keyboard.press('f')
        elif action == 'open':
            if session_log.getLastRowFromLogSession(str(screen_area))[0]['is_headsup'] == 1:
                keyboard.press('o')
            else:
                keyboard.press('r')
        elif action == 'call':
            keyboard.press('c')
        elif action == 'check':
            keyboard.press('h')
        session_log.updateActionLogSession(action, str(screen_area))
    except Exception as e:
        error_log.errorLog('getDecision', str(e))
        print(e)

def handConverting(hand):
    if hand[1] == hand[3]:
        hand = hand[0] + hand[2] + 's'
    else:
        hand = hand[0] + hand[2] + 'o'
    return hand

def getActionFromPreflopChart(screen_area):
    row = session_log.getLastRowFromLogSession(screen_area)
    last_opponent_action = row[0]['last_opponent_action']
    hand = handConverting(row[0]['hand'])
    stack = int(row[0]['current_stack'])
    position = row[0]['current_position']
    if stack == 6:
        return sklansky_chubukov.getAction(hand, int(row[0]['current_stack']), last_opponent_action, position)
    elif stack == 0:
        return 'push'
    if last_opponent_action is None:
        last_opponent_action = ' is null'
    else:
        last_opponent_action = " = '" + last_opponent_action + '\''
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select trim(action) as action from preflop_chart "
                    "where hand = '" + hand + '\'' + " and position = '" + position + '\'' +
                    " and is_headsup = '" + str(row[0]['is_headsup']) + '\'' + " and opponent_last_action" +
                    last_opponent_action + " and stack = " + str(stack))
    if len(data) == 0:
        return sklansky_chubukov.getAction(hand, int(row[0]['current_stack']), last_opponent_action, position)
    return data[0]['action']

def convertStack(stack):
    if stack >= 22:
        stack = 22
    elif stack in range(17, 22):
        stack = 21
    elif stack in range(13, 17):
        stack = 17
    elif stack in range(10, 13):
        stack = 13
    elif stack in range(7, 10):
        stack = 10
    elif stack in range(1, 7):
        stack = 6
    elif stack == 0:
        stack = 0
    return stack