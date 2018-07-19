import postgresql

#Создание новой записи в таблицу session_log
def insertIntoLogSession(screen_area,hand):
    db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
    data = db.prepare("insert into session_log(screen_area,hand) values($1,$2)")
    data(screen_area,hand)

#Получение значение поля action последней записи для текущей области экрана
def getLastRowActionFromLogSession(screen_area):
    db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
    data = db.query("select trim(action) as action from session_log where screen_area = " + screen_area + " order by id desc limit 1")
    return data

#Обновление значения поля action последней записи для текущей области экрана
def updateActionLogSession(action, screen_area):
    db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
    data = db.query("UPDATE session_log SET action=yourvalue FROM "
                    "(SELECT id, '" + action + "' AS yourvalue FROM session_log where screen_area = " + screen_area + " ORDER BY id desc limit 1) AS t1 "
                    "WHERE session_log.id=t1.id ")

#Получаем руку последней записи для текущей области экрана
def getLastHandFromLogSession(screen_area):
    db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
    data = db.query("select trim(hand) as hand from session_log where screen_area = " + screen_area + " order by id desc limit 1")
    return data