def getDecision(hand):
    if pocketBroadway(hand) == 1 or pocketPair(hand) == 1 or anyAce(hand) == 1:
        return 1
    else:
        return 0


def pocketBroadway(hand):
    val = ''
    broadway = ['A', 'K', 'Q', 'J', 'T']
    for value in hand:
        if value.isupper():
            val += value
    try:
        if val[0] in broadway and val[1] in broadway:
            return 1
        else:
            return 0
    except:
        return 0

def pocketPair(hand):
    val = ''
    for c in hand:
        if c.isupper() or c.isdigit():
            val += c
    if val[0] == val[1]:
        return 1
    else:
        return 0

def anyAce(hand):
    val = ''
    for c in hand:
        if c.isupper() or c.isdigit():
            val += c
    if val[0] == 'A' or val[1] == 'A':
        return 1
    else:
        return 0