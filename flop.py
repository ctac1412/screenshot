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
        opponent_reaction = image_processing.searchLastOpponentAction(screen_area)
        if not isinstance(opponent_reaction, str):
            opponent_reaction = opponent_reaction['alias']
        session_log.updateHandAfterFlop(screen_area, hand)
        hand_value = checkPair(hand, screen_area)
        if hand_value != True:
            hand_value = checkFlushDraw(hand, screen_area, hand_value)
        if hand_value != True:
            checkStraightDraw(hand, screen_area, hand_value)
        hand_value = session_log.getHandValue(screen_area)
        # if top_pair <= T
        if hand_value == 'weak_top_pair':
            keyboard.press('q')
            session_log.updateActionLogSession('push', str(screen_area))
            return
        elif action == 'open' and int(stack) > 12:
            if image_processing.checkIsCbetAvailable(str(screen_area)):
                if hand_value in ('top_pair', 'two_pairs', 'set', 'flush', 'straight', 'full_house') or hand_value.find('.') != -1:
                    keyboard.press('v')
                    session_log.updateActionLogSession('cbet', str(screen_area))
                    return
                elif hand_value in ('trash', 'bottom_pair', 'gutshot') and is_headsup == 0:
                    keyboard.press('h')
                    session_log.updateActionLogSession('cc_postflop', str(screen_area))
                    return
                else:
                    keyboard.press('b')
                    session_log.updateActionLogSession('cbet', str(screen_area))
                    return
            else:
                if hand_value in('top_pair', 'two_pairs', 'set', 'flush', 'straight', 'full_house') or hand_value.find('.') != -1:
                    keyboard.press('q')
                    session_log.updateActionLogSession('push', str(screen_area))
                    return
                elif int(stack) <= 10 and (hand_value in('middle_pair', 'straight_draw', 'flush_draw', 'low_two_pairs', 'second_pair')
                                           or hand_value.find('.') != -1):
                    keyboard.press('q')
                    session_log.updateActionLogSession('push', str(screen_area))
                    return
                elif hand_value != 'trash':
                    keyboard.press('f')
                    session_log.updateActionLogSession('fold', str(screen_area))
                    return
                elif opponent_reaction in ('1', '2'):
                    keyboard.press('c')
                    session_log.updateActionLogSession('cc_postflop', str(screen_area))
                else:
                    keyboard.press('f')
                    session_log.updateActionLogSession('fold', str(screen_area))
        # if action <> open
        else:
            if image_processing.checkIsCbetAvailable(str(screen_area)):
                if is_headsup == 0 and (hand_value in('top_pair', 'two_pairs', 'set', 'flush', 'straight', 'full_house')
                                        or hand_value.find('.') != -1):
                    keyboard.press('v')
                    session_log.updateActionLogSession('cbet', str(screen_area))
                    return
                elif is_headsup == 1 and (hand_value.find('.') != -1 or
                        hand_value in('top_pair', 'two_pairs', 'set', 'flush', 'straight', 'low_two_pairs', 'full_house')):
                    keyboard.press('v')
                    session_log.updateActionLogSession('cbet', str(screen_area))
                    return
                elif is_headsup == 1 and hand_value in('middle_pair', 'straight_draw', 'flush_draw', 'second_pair'):
                    keyboard.press('b')
                    session_log.updateActionLogSession('cbet', str(screen_area))
                    return
                else:
                    keyboard.press('h')
                    session_log.updateActionLogSession('cc_postflop', str(screen_area))
                    return True
            # if action <> open and cbet unavailable
            else:
                if hand_value == 'trash':
                    keyboard.press('f')
                    session_log.updateActionLogSession('fold', str(screen_area))
                    return
                elif is_headsup == 0 and (hand_value in('top_pair', 'two_pairs', 'set', 'flush', 'straight', 'full_house')
                                          or hand_value.find('.') != -1):
                    keyboard.press('q')
                    session_log.updateActionLogSession('push', str(screen_area))
                    return
                elif is_headsup == 1 and (hand_value.find('.') != -1 or
                        hand_value in('top_pair', 'two_pairs', 'set', 'flush', 'straight', 'full_house')):
                    keyboard.press('q')
                    session_log.updateActionLogSession('push', str(screen_area))
                elif int(stack) <= 10 and (hand_value in('middle_pair', 'straight_draw', 'flush_draw', 'low_two_pairs', 'second_pair')
                                           or hand_value.find('.') != -1):
                    keyboard.press('q')
                    session_log.updateActionLogSession('push', str(screen_area))
                    return
                elif opponent_reaction in ('1', '2') and hand_value != 'gutshot':
                    keyboard.press('c')
                    session_log.updateActionLogSession('cc_postflop', str(screen_area))
                else:
                    keyboard.press('f')
                    session_log.updateActionLogSession('fold', str(screen_area))
    except Exception as e:
        error_log.errorLog('makeFlopDecision' + action, str(e))
        print(e)

def checkStraightDraw(hand, screen_area, hand_value):
    if len(hand) == 10:
        hand = hand[0] + hand[2] + hand[4] + hand[6] + hand[8]
    elif len(hand) == 8:
        hand = hand[0] + hand[2] + hand[4] + hand[6]
    elif len(hand) == 12:
        hand = hand[0] + hand[2] + hand[4] + hand[6] + hand[8] + hand[10]
    elif len(hand) == 14:
        hand = hand[0] + hand[2] + hand[4] + hand[6] + hand[8] + hand[10] + hand[12]
    else:
        return hand_value
    collection = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    low_straight = [0, 1, 2, 3, 12]
    arr = []
    for val in hand:
        arr.append(collection.index(val))
    arr = list(set(arr))
    arr = sorted(arr)
    arr_length = len(arr)
    if arr_length == 5:
        first = arr[:-1]
        second = arr[1:]
        if list(range(min(arr), max(arr) + 1)) == arr or set(low_straight).issubset(arr):
            hand_value = 'straight'
        elif first == list(range(min(first), max(first) + 1)) or second == list(range(min(second), max(second) + 1)):
            if hand_value != 'trash':
                hand_value = hand_value + '.straight_draw'
            else:
                hand_value = 'straight_draw'
    elif arr_length == 6:
        first = arr[:-1]
        second = arr[1:]
        third = arr[:-2]
        fourth = arr[1:-1]
        fifth = arr[2:]
        if list(range(min(arr), max(arr) + 1)) == arr or set(low_straight).issubset(arr):
            hand_value = 'straight'
        elif first == list(range(min(first), max(first) + 1)) or second == list(range(min(second), max(second) + 1)):
            hand_value = 'straight'
        elif third == list(range(min(third), max(third) + 1)):
            if hand_value != 'trash':
                hand_value = hand_value + '.straight_draw'
            else:
                hand_value = 'straight_draw'
        elif fourth == list(range(min(fourth), max(fourth) + 1)):
            if hand_value != 'trash':
                hand_value = hand_value + '.straight_draw'
            else:
                hand_value = 'straight_draw'
        elif fifth == list(range(min(fifth), max(fifth) + 1)):
            if hand_value != 'trash':
                hand_value = hand_value + '.straight_draw'
            else:
                hand_value = 'straight_draw'
    elif arr_length == 4:
        if arr == list(range(min(arr), max(arr) + 1)):
            if hand_value != 'trash':
                hand_value = hand_value + '.straight_draw'
            else:
                hand_value = 'straight_draw'
    elif arr_length == 7:
        first = arr[:-2]
        second = arr[1:-1]
        third = arr[2:]
        if first == list(range(min(first), max(first) + 1)) or second == list(range(min(second), max(second) + 1)) or \
                third == list(range(min(third), max(third) + 1)) or set(low_straight).issubset(arr):
            hand_value = 'straight'
    if hand_value not in ('straight', 'straight_draw') and hand_value.find('.') == -1:
        hand_value = checkGutShot(hand, hand_value)
    session_log.updateHandValue(screen_area, hand_value)

def checkFlushDraw(hand, screen_area, hand_value):
    if len(hand) == 10:
        hand = hand[1] + hand[3] + hand[5] + hand[7] + hand[9]
    elif len(hand) == 8:
        hand = hand[1] + hand[3] + hand[5] + hand[7]
    elif len(hand) == 12:
        hand = hand[1] + hand[3] + hand[5] + hand[7] + hand[9] + hand[11]
    elif len(hand) == 14:
        hand = hand[1] + hand[3] + hand[5] + hand[7] + hand[9] + hand[11] + hand[13]
    else:
        return hand_value
    suit_count = len(set(hand))
    if suit_count == 1:
        hand_value = 'flush'
        session_log.updateHandValue(screen_area, hand_value)
        return True
    elif suit_count <= 3:
        counter = {}
        for item in hand:
            counter[item] = counter.get(item, 0) + 1
        doubles = {element: count for element, count in counter.items() if count > 3}
        if doubles and list(doubles.values())[0] >= 5:
            hand_value = 'flush'
            session_log.updateHandValue(screen_area, hand_value)
            return True
        elif len(doubles) > 0 and list(doubles)[0] in (hand[0], hand[1]):
            if hand_value != 'trash':
                hand_value = hand_value + '.flush_draw'
                session_log.updateHandValue(screen_area, hand_value)
                return True
            else:
                hand_value = 'flush_draw'
            return hand_value
    else:
        return hand_value
    return hand_value

def checkPair(hand, screen_area):
    hand_value = 'trash'
    if len(hand) == 10:
        flop = [hand[4], hand[6], hand[8]]
        hand = hand[0] + hand[2] + hand[4] + hand[6] + hand[8]
    elif len(hand) == 8:
        flop = [hand[4], hand[6]]
        hand = hand[0] + hand[2] + hand[4] + hand[6]
    elif len(hand) == 12:
        flop = [hand[4], hand[6], hand[8], hand[10]]
        hand = hand[0] + hand[2] + hand[4] + hand[6] + hand[8] + hand[10]
    elif len(hand) == 14:
        flop = [hand[4], hand[6], hand[8], hand[10], hand[12]]
        hand = hand[0] + hand[2] + hand[4] + hand[6] + hand[8] + hand[10] + hand[12]
    else:
        return hand_value
    ranks = [str(n) for n in range(2, 10)] + list('TJQKA')
    ts = []
    for item in flop:
        ts.append(ranks.index(item))
    counter = {}
    for item in hand:
        counter[item] = counter.get(item, 0) + 1
    doubles = {element: count for element, count in counter.items() if count > 1}
    if len(doubles) == 1:
        double_element = list(doubles.keys())[0]
        index_double_element = ranks.index(double_element)
        if list(doubles.values())[0] > 2 and double_element in (hand[0], hand[1]):
            hand_value = 'set'
        elif double_element in (hand[0], hand[1]) and index_double_element >= max(ts):
            if index_double_element <= 8:
                hand_value = 'weak_top_pair'
            else:
                hand_value = 'top_pair'
        elif double_element in (hand[0], hand[1]) and ranks.index(double_element) == min(ts):
            hand_value = 'bottom_pair'
        elif double_element in (hand[0], hand[1]):
            set(ts)
            ts.remove(max(ts))
            if index_double_element >= max(ts):
                hand_value = 'second_pair'
            else:
                hand_value = 'middle_pair'
    elif len(doubles) == 2:
        maximum = max(doubles, key=doubles.get)
        double_element = list(doubles.keys())[0]
        if double_element in (hand[0], hand[1]) and ranks.index(double_element) >= max(ts):
            hand_value = 'two_pairs'
        elif sorted(list(doubles.keys())) == sorted([hand[0], hand[1]]):
            hand_value = 'two_pairs'
        elif doubles[maximum] >= 3:
            hand_value = 'full_house'
        elif double_element in (hand[0], hand[1]):
            hand_value = 'low_two_pairs'
    elif len(doubles) == 3:
        if hand[0] in list(doubles.keys()) and hand[1] in list(doubles.keys()):
            hand_value = 'two_pairs'
        else:
            hand_value = 'low_two_pairs'
    if hand_value in ('top_pair', 'set', 'two_pairs', 'weak_top_pair'):
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
                    "where screen_area = " + screen_area)
    return data

def checkGutShot(hand, hand_value):
    collection = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    arr = []
    for val in hand:
        arr.append(collection.index(val))
    arr = list(set(arr))
    arr = sorted(arr)
    low_straight = [0, 1, 2, 3, 12]
    count = 0
    for item in arr:
        if item in low_straight:
            count += 1
    if len(arr) == 5 and (arr[-2:][0] - arr[0] == 4 or arr[-1:][0] - arr[1] == 4):
        if hand_value != 'trash':
            hand_value = hand_value + '.gutshot'
        else:
            hand_value = 'gutshot'
    elif len(arr) == 6 and (arr[-3:][0] - arr[0] == 4 or arr[-2:][0] - arr[1] == 4 or arr[-1:][0] - arr[2] == 4):
        if hand_value != 'trash':
            hand_value = hand_value + '.gutshot'
        else:
            hand_value = 'gutshot'
    elif len(arr) == 4 and arr[-1:][0] - arr[0] == 4:
        if hand_value != 'trash':
            hand_value = hand_value + '.gutshot'
        else:
            hand_value = 'gutshot'
    elif count == 4:
        if hand_value != 'trash':
            hand_value = hand_value + '.gutshot'
        else:
            hand_value = 'gutshot'
    return hand_value
