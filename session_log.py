import postgresql
import error_log
import db_conf

#Создание новой записи в таблицу session_log
def insertIntoLogSession(screen_area, hand, current_position=0, current_stack=0):
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

#Получаем руку последней записи для текущей области экрана
def getLastHandFromLogSession(screen_area):
    try:
        db = postgresql.open(db_conf.connectionString())
        data = db.query(
            "select trim(hand) as hand from session_log where screen_area = " + screen_area + " order by id desc limit 1")
        return data[0]['hand']
    except Exception as e:
        error_log.errorLog('getLastHandFromLogSession',e)