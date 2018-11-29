import error_log
import keyboard
import session_log
import sklansky_chubukov

IMAGES_FOLDER = "images/"


def get_decision(screen_area, db):
    try:
        row = get_action_from_preflop_chart(screen_area, db)
        action = row[0]
        stack = row[1]
        if action == 'push':
            keyboard.press('q')
        elif action == 'fold':
            keyboard.press('f')
        elif action == 'open':
            if int(stack) > 17:
                keyboard.press('r')
            else:
                keyboard.press('o')
        elif action == 'call':
            keyboard.press('c')
        elif action == 'check':
            keyboard.press('h')
        session_log.update_action_log_session(action, str(screen_area), db)
    except Exception as e:
        error_log.error_log('getDecision', str(e))
        print(e)


def hand_converting(hand):
    if hand[1] == hand[3]:
        hand = hand[0] + hand[2] + 's'
    else:
        hand = hand[0] + hand[2] + 'o'
    return hand


def get_action_from_preflop_chart(screen_area, db):
    row = session_log.get_last_row_from_log_session(screen_area, db)
    last_opponent_action = row[0]['last_opponent_action']
    hand = hand_converting(row[0]['hand'])
    stack = int(row[0]['current_stack'])
    position = row[0]['current_position']
    is_headsup = row[0]['is_headsup']
    if 0 < stack <= 6:
        return sklansky_chubukov.get_action(hand, stack, last_opponent_action, position, db)
    elif stack == 0:
        data = ['push']
        data.append(stack)
        return data
    if last_opponent_action is None:
        last_opponent_action = ' is null'
    else:
        last_opponent_action = " = '" + last_opponent_action + '\''
    data = db.query("select trim(action) as action from preflop_chart "
                    "where hand = '" + hand + '\'' + " and position = '" + position + '\'' +
                    " and is_headsup = '" + str(is_headsup) + '\'' + " and opponent_last_action" +
                    last_opponent_action + " and stack = " + str(stack))
    if len(data) == 0:
        return sklansky_chubukov.get_action(hand, stack, last_opponent_action, position, db)
    data = [data[0]['action']]
    data.append(stack)
    return data
