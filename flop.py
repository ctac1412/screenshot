def makeFlopDecision(hand):
    checkPair(hand)
    checkFlushDraw(hand)
    checkStraightDraw(hand)
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
    hand = hand[0] + hand[2] + hand[4] + hand[6] + hand[8]
    counter = {}

    for item in hand:
        counter[item] = counter.get(item, 0) + 1

    doubles = {element: count for element, count in counter.items() if count > 1}
    if len(doubles) > 0:
        return True