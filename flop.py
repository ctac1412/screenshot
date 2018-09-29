import image_processing
import postgresql
import db_conf
from PIL import Image, ImageGrab
import keyboard
import session_log

def makeFlopDecision(screen_area, hand, image_name, folder_name):
    saveFlopImage(str(screen_area), image_name, folder_name)
    flop_area = getFlopArea(str(screen_area))
    flop_card = image_processing.searchCards(str(flop_area), image_processing.getCards(), 6, 4)
    if len(flop_card) == 6:
        hand = hand + flop_card
        print(hand)
        if checkPair(hand) or checkFlushDraw(hand) or checkStraightDraw(hand):
            keyboard.press('q')
            session_log.updateActionLogSession('push', str(screen_area))
        elif session_log.getLastRowActionFromLogSession(str(screen_area)) == 'open':
            keyboard.press('o')
            session_log.updateActionLogSession('cbet', str(screen_area))
    else:
        print(hand)
        return False

def checkStraightDraw(hand):
    hand = hand[0] + hand[2] + hand[4] + hand[6] + hand[8]
    collection = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    arr = []

    for val in hand:
        arr.append(collection.index(val))
    arr = sorted(arr)

    if int(arr[4]) - int(arr[1]) == 3 or int(arr[3]) - int(arr[0]) == 3:
        return True

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
        if double_element in [hand[0], hand[1]] and ranks.index(double_element) == max(ts):
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
        image = ImageGrab.grab(bbox=(value['x_coordinate'], value['y_coordinate'], value['width'], value['height']))
        # Сохраняем изображение на жестком диске
        image.save(image_path, "PNG")
        # Сохраняем инфо в бд
        image_processing.insertImagePathIntoDb(image_path, value['screen_area'])

def getFlopData(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select x_coordinate,y_coordinate,width,height,screen_area from screen_coordinates "
                    "where screen_area = "  + screen_area)
    return data