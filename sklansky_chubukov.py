import postgresql
import db_conf

def getValidStackValueToPush(hand):
    db = postgresql.open(db_conf.connectionString())
    data = db.query(
        "select stack_value from sklansky_chubukov where hand = " + "'" + hand + "'")
    return data[0]['stack_value']

def getAction(hand, stack, last_opponent_action, position):
    push_stack_value = getValidStackValueToPush(hand)
    if int(stack) <= push_stack_value:
        return 'push'
    elif last_opponent_action == 'limp' and position == 'big_blind':
        return 'check'
    else:
        return 'fold'