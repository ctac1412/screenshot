import image_processing
import postgresql
import db_conf
import keyboard
import session_log
import error_log

def makeFlopDecision(screen_area, hand, image_name, folder_name):
    saveFlopImage(str(screen_area), image_name, folder_name)
    flop_area = getFlopArea(str(screen_area))
    flop_card = image_processing.searchCards(str(flop_area), image_processing.getCards(), 6, 4)
    if len(flop_card) == 6:
        hand = hand + flop_card
        if checkPair(hand) or checkFlushDraw(hand) or checkStraightDraw(hand):
            keyboard.press('q')
            session_log.updateActionLogSession('push', str(screen_area))
            return
        elif session_log.getLastRowActionFromLogSession(str(screen_area)) == 'open':
            stack = session_log.getLastRowFromLogSession(screen_area)[0]['current_stack']
            if image_processing.checkIsCbetAvailable(str(screen_area)) and int(stack) > 12:
                keyboard.press('o')
                session_log.updateActionLogSession('cbet', str(screen_area))
            return
        else:
            keyboard.press('f')
            session_log.updateActionLogSession('fold', str(screen_area))
    else:
        session_log.updateActionLogSession('end', str(screen_area))

def checkStraightDraw(hand):
    hand = hand[0] + hand[2] + hand[4] + hand[6] + hand[8]
    collection = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    arr = []

    for val in hand:
        arr.append(collection.index(val))
    arr = list(set(arr))
    arr = sorted(arr)

    try:
        if len(arr) > 4 and int(arr[-1]) - int(arr[1]) == 3 or int(arr[3]) - int(arr[0]) == 3:
            print(arr)
            return True
        elif int(arr[3]) - int(arr[0]) == 3:
            return True
    except Exception as e:
        error_log.errorLog('checkStraightDraw', str(e))
        print(e)
        return False

def checkFlushDraw(hand):
    hand = hand[1] + hand[3] + hand[5] + hand[7] + hand[9]
    counter = {}

    for item in hand:
        counter[item] = counter.get(item, 0) + 1

    doubles = {element: count for element, count in counter.items() if count > 3}
    if len(doubles) > 0:
        return True

def checkPair(hand):
    flop = [hand[4], hand[6], hand[8]]
    ranks = [str(n) for n in range(2, 10)] + list('TJQKA')
    ts = []
    for item in flop:
        ts.append(ranks.index(item))
    hand = hand[0] + hand[2] + hand[4] + hand[6] + hand[8]
    counter = {}

    for item in hand:
        counter[item] = counter.get(item, 0) + 1
    doubles = {element: count for element, count in counter.items() if count > 1}
    if len(doubles) > 0:
        double_element = list(doubles.keys())[0]
        if double_element in [hand[0], hand[1]] and ranks.index(double_element) != min(ts) or \
                list(doubles.values())[0] > 2 and double_element in [hand[0], hand[1]]:
            return True
    return False

#Получаем номер области экрана, на которой нужно искать элемент для текущего стола
def getFlopArea(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select flop_area from screen_coordinates where screen_area = " + screen_area + " and active = 1")
    return data[0]['flop_area']

def saveFlopImage(screen_area,image_name,folder_name):
    for value in getFlopData(str(getFlopArea(str(screen_area)))):
        image_path = folder_name + "/" + str(getFlopArea(str(screen_area))) + "/" + image_name + ".png"
        # Делаем скрин указанной области экрана
        image_processing.imaging(value['x_coordinate'], value['y_coordinate'], value['width'], value['height'], image_path, value['screen_area'])

def getFlopData(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select x_coordinate,y_coordinate,width,height,screen_area from screen_coordinates "
                    "where screen_area = "  + screen_area)
    return data