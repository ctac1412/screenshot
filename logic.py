import error_log
import postgresql

def getDecision(hand):
    try:
        if pocketBroadway(hand) == 1 or pocketPair(hand) == 1 or anyAce(hand) == 1:
            return 1
        else:
            return 0
    except Exception as e:
        error_log.errorLog('getDecision',e)


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

def getIterationTimer():
    db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
    data = db.query("select round(extract(epoch from now() - created_at)) as second_left from iteration_timer")
    return data[0]['second_left']

def updateIterationTimer():
    db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
    db.query("UPDATE iteration_timer SET created_at = now()")