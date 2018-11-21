import postgresql
import db_conf


def get_valid_stack_value_to_push(hand):
    db = postgresql.open(db_conf.connection_string())
    data = db.query(
        "select stack_value from sklansky_chubukov where hand = " + "'" + hand + "'")
    return data[0]['stack_value']


def get_action(hand, stack, last_opponent_action, position):
    push_stack_value = get_valid_stack_value_to_push(hand)
    if int(stack) <= push_stack_value:
        return 'push'
    elif last_opponent_action == 'limp' and position == 'big_blind':
        return 'check'
    else:
        return 'fold'
