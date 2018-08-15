import postgresql
import error_log
import db_conf
import current_stack
import determine_position

#Создание новой записи в таблицу session_log
def insertIntoLogSession(screen_area, hand, current_position='0', current_stack='0'):
    try:
        db = postgresql.open(db_conf.connectionString())
        data = db.prepare("insert into session_log(screen_area,hand,current_position,current_stack) values($1,$2,$3,$4)")
        data(screen_area, hand, current_position, current_stack)
    except Exception as e:
        error_log.errorLog('insertIntoLogSession',e)

#Получение значение поля action последней записи для текущей области экрана
def getLastRowActionFromLogSession(screen_area):
    try:
        db = postgresql.open(db_conf.connectionString())
        data = db.query("select trim(action) as action from session_log where screen_area = " + screen_area + " order by id desc limit 1")
        return data[0]['action']
    except Exception as e:
        error_log.errorLog('getLastRowActionFromLogSession',e)

#Обновление значения поля action последней записи для текущей области экрана
def updateActionLogSession(action, screen_area):
    try:
        db = postgresql.open(db_conf.connectionString())
        db.query("UPDATE session_log SET action=yourvalue FROM "
                        "(SELECT id, '" + action + "' AS yourvalue FROM session_log where screen_area = " + screen_area + " ORDER BY id desc limit 1) AS t1 "
                                                                                                                          "WHERE session_log.id=t1.id ")
    except Exception as e:
        error_log.errorLog('updateActionLogSession',e)

#Обновление значения поля current_stack
def updateCurrentStackLogSession(screen_area):
    db = postgresql.open(db_conf.connectionString())
    db.query("UPDATE session_log SET current_stack=yourvalue FROM "
                        "(SELECT id, current_stack - 3 AS yourvalue FROM session_log where screen_area = " + screen_area + " ORDER BY id desc limit 1) AS t1 "
                                                                                                                          "WHERE session_log.id=t1.id ")

#Получаем руку последней записи для текущей области экрана
def getLastHandFromLogSession(screen_area):
    try:
        db = postgresql.open(db_conf.connectionString())
        data = db.query(
            "select trim(hand) as hand,trim(current_stack) as current_stack,trim(current_position) as current_position from session_log where screen_area = " + screen_area + " order by id desc limit 1")
        return data
    except Exception as e:
        error_log.errorLog('getLastHandFromLogSession',e)


def checkConditionsBeforeInsert(hand, screen_area):
    # session = getLastHandFromLogSession(str(screen_area))
    # if hand != '' and hand != session[0]['hand'] and session[0]['current_stack'] != current_stack.searchCurrentStack(str(screen_area)):
    if hand != '':
        insertIntoLogSession(screen_area,hand,str(determine_position.seacrhBlindChips(screen_area)),str(current_stack.searchCurrentStack(str(screen_area))))
        session = getLastHandFromLogSession(str(screen_area))
        return session
    else:
        return False