import image_processing

position = 'small_blind'
headsup = 0
if position == 'big_blind' or position == 'small_blind' and headsup == 0:
    last_opponnet_action = image_processing.searchLastOpponentAction('3')
    print(last_opponnet_action)
    if not isinstance(last_opponnet_action, str):
        last_opponnet_action = last_opponnet_action['opponent_action']
    print(last_opponnet_action)