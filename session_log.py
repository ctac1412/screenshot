import postgresql
import error_log

#Создание новой записи в таблицу session_log
def insertIntoLogSession(screen_area,hand):
    try:
        db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
        data = db.prepare("insert into session_log(screen_area,hand) values($1,$2)")
        data(screen_area, hand)
    except Exception as e:
        error_log.errorLog('insertIntoLogSession',e)

#Получение значение поля action последней записи для текущей области экрана
def getLastRowActionFromLogSession(screen_area):
    try:
        db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
        data = db.query("select trim(action) as action from session_log where screen_area = " + screen_area + " order by id desc limit 1")
        return data
    except Exception as e:
        error_log.errorLog('getLastRowActionFromLogSession',e)

#Обновление значения поля action последней записи для текущей области экрана
def updateActionLogSession(action, screen_area):
    try:
        db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
        data = db.query("UPDATE session_log SET action=yourvalue FROM "
                        "(SELECT id, '" + action + "' AS yourvalue FROM session_log where screen_area = " + screen_area + " ORDER BY id desc limit 1) AS t1 "
                                                                                                                          "WHERE session_log.id=t1.id ")
    except Exception as e:
        error_log.errorLog('updateActionLogSession',e)

#Получаем руку последней записи для текущей области экрана
def getLastHandFromLogSession(screen_area):
    try:
        db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
        data = db.query(
            "select trim(hand) as hand from session_log where screen_area = " + screen_area + " order by id desc limit 1")
        return data
    except Exception as e:
        error_log.errorLog('getLastHandFromLogSession',e)