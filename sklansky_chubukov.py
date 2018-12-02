import db_query


def get_action(hand, stack, last_opponent_action, position, db):
    push_stack_value = db_query.get_valid_stack_value_to_push(hand, db)
    data = [stack]
    if int(stack) <= push_stack_value:
        data.insert(0, 'push')
        return data
    elif last_opponent_action == 'limp' and position == 'big_blind':
        data.insert(0, 'check')
        return data
    else:
        data.insert(0, 'fold')
        return data
