import postgresql
import db_conf

def getValidStackValueToPush(hand):
    db = postgresql.open(db_conf.connectionString())
    data = db.query(
        "select stack_value from sklansky_chubukov where hand = " + "'" + hand + "'")
    return data[0]['stack_value']

def getAction(hand, stack):
    push_stack_value = getValidStackValueToPush(hand)
    if int(stack) <= push_stack_value:
        return 'push'
    else:
        return 'fold'