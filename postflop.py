import session_log
import introduction
import image_processing
import keyboard
import flop

def checkIsTurn(screen_area, deck):
    last_row = session_log.getLastRowFromLogSession(str(screen_area))
    hand = last_row[0][0]
    is_headsup = last_row[0][4]
    element_area = introduction.saveElement(screen_area, 'turn_area')
    if image_processing.searchElement(element_area, ['turn'], 'green_board/') is False:
        turn = image_processing.searchCards(element_area, deck, 2)
        session_log.updateHandAfterTurn(screen_area, turn)
        if turnAction(screen_area, is_headsup, hand):
            return True


def turnAction(screen_area, is_headsup, hand):
    hand_value = flop.checkPair(hand, screen_area)
    if hand_value != True:
        hand_value = flop.checkFlushDraw(hand, screen_area, hand_value)
    if hand_value != True:
        flop.checkStraightDraw(hand, screen_area, hand_value)
    hand_value = session_log.getHandValue(screen_area)
    if is_headsup == 0 and hand_value in ['top_pair', 'two_pairs', 'set', 'flush', 'straight'] or hand_value.find('.') != -1:
        keyboard.press('q')
        session_log.updateActionLogSession('push', str(screen_area))
        return True
    elif is_headsup == 1 and hand_value.find('.') != -1 or \
            hand_value in ['top_pair', 'two_pairs', 'set', 'flush', 'straight', 'middle_pair', 'straight_draw', 'flush_draw']:
        keyboard.press('q')
        session_log.updateActionLogSession('push', str(screen_area))
        return True
    elif image_processing.checkIsCbetAvailable(str(screen_area)):
        keyboard.press('h')
        session_log.updateActionLogSession('cc_postflop', str(screen_area))
        return True
    elif not isinstance (image_processing.searchLastOpponentAction(screen_area), str):
        keyboard.press('c')
        session_log.updateActionLogSession('cc_postflop', str(screen_area))
        return True
    else:
        keyboard.press('f')
        session_log.updateActionLogSession('fold', str(screen_area))
        return True


def actionAfterCbet(x_coordinate, y_coordinate, width, height, image_path, screen_area, deck):
    if introduction.checkIsFold(screen_area, x_coordinate, y_coordinate, width, height, image_path): return
    if checkIsTurn(screen_area, deck): return
    if checkIsRaiseCbet(screen_area): return

def checkIsRiver(screen_area, deck):
    last_row = session_log.getLastRowFromLogSession(str(screen_area))
    hand = last_row[0][0]
    element_area = introduction.saveElement(screen_area, 'river_area')
    if image_processing.searchElement(element_area, ['river'], 'green_board/') is False:
        turn = image_processing.searchCards(element_area, deck, 2)
        session_log.updateHandAfterTurn(screen_area, turn)
        if riverAction(screen_area, hand):
            return True

def riverAction(screen_area, hand):
    hand_value = flop.checkPair(hand, screen_area)
    opponent_reaction = image_processing.searchLastOpponentAction(screen_area)
    if not isinstance(opponent_reaction, str):
        opponent_reaction = opponent_reaction['alias']
    if hand_value != True:
        hand_value = flop.checkFlushDraw(hand, screen_area, hand_value)
    if hand_value != True:
        flop.checkStraightDraw(hand, screen_area, hand_value)
    hand_value = session_log.getHandValue(screen_area)
    if hand_value in['trash']:
        keyboard.press('f')
        session_log.updateActionLogSession('fold', str(screen_area))
        return True
    elif hand_value in ['top_pair', 'two_pairs', 'set', 'flush', 'straight']:
        keyboard.press('q')
        session_log.updateActionLogSession('push', str(screen_area))
        return True
    elif opponent_reaction in ['1', '2', '3'] and hand_value in['middle_pair']:
        keyboard.press('c')
        session_log.updateActionLogSession('end', str(screen_area))
        return True
    else:
        keyboard.press('f')
        session_log.updateActionLogSession('fold', str(screen_area))
        return True

def checkIsRaiseCbet(screen_area):
    hand_value = session_log.getHandValue(screen_area)
    opponent_reaction = image_processing.searchLastOpponentAction(screen_area)
    if not isinstance(opponent_reaction, str):
        opponent_reaction = opponent_reaction['alias']
    if opponent_reaction in ['push'] and hand_value.find('.') != -1 or \
            hand_value in ['top_pair', 'two_pairs', 'set', 'flush', 'straight']:
        keyboard.press('q')
        session_log.updateActionLogSession('push', str(screen_area))
        return True
    elif opponent_reaction in ['1', '2', '3'] and hand_value in ['middle_pair', 'straight_draw', 'flush_draw']:
        keyboard.press('c')
        session_log.updateActionLogSession('cc_postflop', str(screen_area))
        return True
    else:
        keyboard.press('f')
        session_log.updateActionLogSession('fold', str(screen_area))
        return True

def actionAfterCCPostflop(screen_area, deck):
    if checkIsRiver(screen_area, deck): return
    if checkIsTurn(screen_area, deck): return
    if getOpponentFlopReaction(screen_area): return

def getOpponentFlopReaction(screen_area):
    opponent_reaction = image_processing.searchLastOpponentAction(screen_area)
    if not isinstance(opponent_reaction, str):
        opponent_reaction = opponent_reaction['alias']
    if opponent_reaction in ['1', '2']:
        keyboard.press('c')
        session_log.updateActionLogSession('cc_postflop', str(screen_area))
        return True
    else:
        keyboard.press('f')
        session_log.updateActionLogSession('fold', str(screen_area))
        return True
