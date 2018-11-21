import postgresql
import error_log
import db_conf
import keyboard
import session_log
import sklansky_chubukov

IMAGES_FOLDER = "images/"


def get_decision(screen_area):
    try:
        action = get_action_from_preflop_chart(str(screen_area))
        if action == 'push':
            keyboard.press('q')
        elif action == 'fold':
            keyboard.press('f')
        elif action == 'open':
            keyboard.press('r')
        elif action == 'call':
            keyboard.press('c')
        elif action == 'check':
            keyboard.press('h')
        session_log.update_action_log_session(action, str(screen_area))
    except Exception as e:
        error_log.error_log('getDecision', str(e))
        print(e)


def hand_converting(hand):
    if hand[1] == hand[3]:
        hand = hand[0] + hand[2] + 's'
    else:
        hand = hand[0] + hand[2] + 'o'
    return hand


def get_action_from_preflop_chart(screen_area):
    row = session_log.get_last_row_from_log_session(screen_area)
    last_opponent_action = row[0]['last_opponent_action']
    hand = hand_converting(row[0]['hand'])
    stack = int(row[0]['current_stack'])
    position = row[0]['current_position']
    is_headsup = row[0]['is_headsup']
    if 0 < stack <= 6:
        return sklansky_chubukov.get_action(hand, stack, last_opponent_action, position)
    elif stack == 0:
        return 'push'
    if last_opponent_action is None:
        last_opponent_action = ' is null'
    else:
        last_opponent_action = " = '" + last_opponent_action + '\''
    db = postgresql.open(db_conf.connection_string())
    sql = "select trim(action) as action from preflop_chart where hand = $1 " \
          "and position = $2 and is_headsup = $3 and opponent_last_action = $4 and stack = $5"
    data = db.query(sql, hand, position, is_headsup, last_opponent_action, stack)
    if len(data) == 0:
        return sklansky_chubukov.get_action(hand, stack, last_opponent_action, position)
    return data
