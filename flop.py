import image_processing
import postgresql
import db_conf
import keyboard
import session_log
import error_log
import os

def makeFlopDecision(screen_area, hand, image_name, folder_name, stack, action, is_headsup, flop_deck):
    try:
        saveFlopImage(str(screen_area), image_name, folder_name)
        flop_area = getFlopArea(str(screen_area))
        flop_card = image_processing.searchCards(str(flop_area), flop_deck, 6)
        hand = hand + flop_card
        session_log.updateHandAfterFlop(screen_area, hand)
        hand_value = checkPair(hand, screen_area)
        hand_value = checkFlushDraw(hand, screen_area, hand_value)
        checkStraightDraw(hand,screen_area, hand_value)
            # keyboard.press('q')
            # session_log.updateActionLogSession('push', str(screen_area))
            # return
        # elif action == 'open' and int(stack) > 12 and is_headsup == 1:
        #     if image_processing.checkIsCbetAvailable(str(screen_area)):
        #         keyboard.press('o')
        #         session_log.updateActionLogSession('cbet', str(screen_area))
        #         return
        #     else:
        #         keyboard.press('f')
        #         session_log.updateActionLogSession('fold', str(screen_area))
        #         return
        # else:
        #     keyboard.press('f')
        #     session_log.updateActionLogSession('end', str(screen_area))
    except Exception as e:
        error_log.errorLog('makeFlopDecision' + action, str(e))
        print(e)

def checkStraightDraw(hand, screen_area, hand_value):
    if len(hand) == 10:
        hand = hand[0] + hand[2] + hand[4] + hand[6] + hand[8]
    elif len(hand) == 8:
        hand = hand[0] + hand[2] + hand[4] + hand[6]
    else:
        return False
    collection = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    arr = []
    for val in hand:
        arr.append(collection.index(val))
    arr = list(set(arr))
    arr = sorted(arr)
    arr_length = len(arr)
    if arr_length > 4:
        first = arr[:-1]
        second = arr[1:]
        if first == list(range(min(first), max(first) + 1)) or second == list(range(min(second), max(second) + 1)):
            if len(hand_value) > 0:
                hand_value = hand_value +'.staight_draw'
            else:
                hand_value = 'staight_draw'
            session_log.updateHandValue(screen_area, hand_value)
    elif arr_length == 4:
        if arr == list(range(min(arr), max(arr) + 1)):
            return True
        else:
            return False
    else:
        return False

def checkFlushDraw(hand, screen_area, hand_value):
    if len(hand) == 10:
        hand = hand[1] + hand[3] + hand[5] + hand[7] + hand[9]
    elif len(hand) == 8:
        hand = hand[1] + hand[3] + hand[5] + hand[7]
    else:
        return False
    suit_count = len(set(hand))
    if suit_count == 1:
        hand_value = 'flush'
        session_log.updateHandValue(screen_area, hand_value)
        return True
    elif suit_count == 2:
        counter = {}
        for item in hand:
            counter[item] = counter.get(item, 0) + 1
        doubles = {element: count for element, count in counter.items() if count > 3}
        if len(doubles) > 0:
            if len(hand_value) > 0:
                hand_value = hand_value +'.flush_draw'
            else:
                hand_value = 'flush_draw'
            return hand_value
    else:
        return hand_value

def checkPair(hand, screen_area):
    if len(hand) == 10:
        flop = [hand[4], hand[6], hand[8]]
        ranks = [str(n) for n in range(2, 10)] + list('TJQKA')
        ts = []
        for item in flop:
            ts.append(ranks.index(item))
        hand = hand[0] + hand[2] + hand[4] + hand[6] + hand[8]
    elif len(hand) == 8:
        flop = [hand[4], hand[6]]
        ranks = [str(n) for n in range(2, 10)] + list('TJQKA')
        ts = []
        for item in flop:
            ts.append(ranks.index(item))
        hand = hand[0] + hand[2] + hand[4] + hand[6]
    else:
        return False
    counter = {}
    for item in hand:
        counter[item] = counter.get(item, 0) + 1
    doubles = {element: count for element, count in counter.items() if count > 1}
    hand_value = ''
    if len(doubles) == 1:
        double_element = list(doubles.keys())[0]
        if double_element in [hand[0], hand[1]] and ranks.index(double_element) == max(ts):
            hand_value = 'top_pair'
        elif list(doubles.values())[0] > 2 and double_element in [hand[0], hand[1]]:
            hand_value = 'set'
        elif double_element in [hand[0], hand[1]] and ranks.index(double_element) == min(ts):
            hand_value = 'bottom_pair'
        elif double_element in [hand[0], hand[1]]:
            hand_value = 'middle_pair'
        else:
            return False
    elif len(doubles) == 2:
        hand_value = 'two_pairs'
    print(hand_value)
    if hand_value in ['top_pair', 'set', 'two_pairs']:
        session_log.updateHandValue(screen_area, hand_value)
        return True
    return hand_value

def getFlopArea(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select flop_area from screen_coordinates where screen_area = " + screen_area + " and active = 1")
    return data[0]['flop_area']

def saveFlopImage(screen_area,image_name,folder_name):
    for value in getFlopData(str(getFlopArea(str(screen_area)))):
        image_path = os.path.join(folder_name, str(getFlopArea(str(screen_area))), image_name)
        image_processing.imaging(value['x_coordinate'], value['y_coordinate'], value['width'], value['height'], image_path, value['screen_area'])

def getFlopData(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select x_coordinate,y_coordinate,width,height,screen_area from screen_coordinates "
                    "where screen_area = "  + screen_area)
    return data