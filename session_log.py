import postgresql
import error_log
import db_conf
import current_stack
import determine_position
import headsup
import image_processing

def insertIntoLogSession(screen_area, hand, current_position='0', current_stack='0', action='', is_headsup=0, last_opponent_action=None):
    try:
        db = postgresql.open(db_conf.connectionString())
        data = db.prepare("insert into session_log(screen_area,hand,current_position,current_stack,action,is_headsup,last_opponent_action) "
                          "values($1,$2,$3,$4,$5,$6,$7)")
        data(screen_area, hand, current_position, current_stack, action, int(is_headsup), last_opponent_action)
    except Exception as e:
        error_log.errorLog('insertIntoLogSession',str(e))
        print(e)

def getLastRowActionFromLogSession(screen_area):
    try:
        db = postgresql.open(db_conf.connectionString())
        data = db.query("select trim(action) as action from session_log where screen_area = " + screen_area + " order by id desc limit 1")
        return data[0]['action']
    except Exception as e:
        error_log.errorLog('getLastRowActionFromLogSession', str(e))
        print(e)

def updateActionLogSession(action, screen_area):
    try:
        db = postgresql.open(db_conf.connectionString())
        db.query("UPDATE session_log SET action=yourvalue FROM "
                        "(SELECT id, '" + action + "' AS yourvalue FROM session_log where screen_area = " + screen_area + " ORDER BY id desc limit 1) AS t1 "
                                                                                                                          "WHERE session_log.id=t1.id ")
    except Exception as e:
        error_log.errorLog('updateActionLogSession' + action, str(e))
        print(e)

def getLastIsFlopLogSession(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query(
        "select is_flop from session_log where screen_area = " + screen_area + " order by id desc limit 1")
    return data[0]['is_flop']

def updateIsFlopLogSession(screen_area):
    db = postgresql.open(db_conf.connectionString())
    db.query("UPDATE session_log SET is_flop = 1 FROM "
             "(SELECT id FROM session_log where screen_area = " + screen_area + "ORDER BY id desc limit 1) AS t1 WHERE session_log.id=t1.id")

def updateCurrentStackLogSession(screen_area):
    try:
        db = postgresql.open(db_conf.connectionString())
        db.query("UPDATE session_log SET current_stack=yourvalue FROM "
                 "(SELECT id, int2(current_stack) - 3 AS yourvalue FROM session_log where screen_area = " + screen_area + " ORDER BY id desc limit 1) AS t1 "
                                                                                                                          "WHERE session_log.id=t1.id ")
    except Exception as e:
        error_log.errorLog('updateCurrentStackLogSession', str(e))
        print(e)

def getLastRowFromLogSession(screen_area):
    try:
        db = postgresql.open(db_conf.connectionString())
        data = db.query(
            "select trim(hand) as hand,trim(current_stack) as current_stack,trim(current_position) as current_position, trim(action) as action,"
            "is_headsup, trim(last_opponent_action) as last_opponent_action"
            " from session_log where screen_area = " + str(screen_area) + " order by id desc limit 1")
        return data
    except Exception as e:
        error_log.errorLog('getLastHandFromLogSession', str(e))
        print(e)

def checkConditionsBeforeInsert(hand, screen_area):
    try:
        session = getLastRowFromLogSession(str(screen_area))
        if hand != '' and hand != session[0]['hand']:
            position = str(determine_position.seacrhBlindChips(screen_area))
            opponent_data = headsup.searchOpponentCard(str(screen_area))
            is_headsup = opponent_data[0]
            stack = str(current_stack.searchCurrentStack(str(screen_area)))
            print(stack)
            opponent_data.pop(0)
            print(opponent_data)
            opponent_actual_stack = max(opponent_data)
            if int(opponent_actual_stack) < int(stack):
                stack = opponent_actual_stack
            print(stack)
            if position == 'big_blind' or position == 'small_blind' and is_headsup == 0:
                last_opponnet_action = image_processing.searchLastOpponentAction(screen_area)
                if not isinstance(last_opponnet_action, str):
                    last_opponnet_action = last_opponnet_action['opponent_action']
            else:
                last_opponnet_action = None
            insertIntoLogSession(screen_area, hand, position, str(stack), is_headsup=is_headsup, last_opponent_action=last_opponnet_action)
            session = [hand, stack, position, '', is_headsup]
            return session
        else:
            return False
    except Exception as e:
        error_log.errorLog('checkConditionsBeforeInsert', str(e))
        print(e)