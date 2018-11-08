import session_log
import introduction
import image_processing
import keyboard
import flop
import current_stack

def checkIsTurn(screen_area, deck):
    element_area = introduction.saveElement(screen_area, 'turn_area')
    if image_processing.searchElement(element_area, ['turn'], 'green_board/') is False:
        if len(session_log.getActualHand(screen_area)) == 10:
            turn = image_processing.searchCards(element_area, deck, 2)
            session_log.updateHandAfterTurn(screen_area, turn)
        last_row = session_log.getLastRowFromLogSession(str(screen_area))
        hand = last_row[0][0]
        stack = last_row[0][1]
        if turnAction(screen_area, hand, stack):
            return True
    return False

def turnAction(screen_area, hand, stack):
    opponent_reaction = image_processing.searchLastOpponentAction(screen_area)
    if not isinstance(opponent_reaction, str):
        opponent_reaction = opponent_reaction['alias']
    hand_value = flop.checkPair(hand, screen_area)
    if hand_value != True:
        hand_value = flop.checkFlushDraw(hand, screen_area, hand_value)
    if hand_value != True:
        flop.checkStraightDraw(hand, screen_area, hand_value)
    hand_value = session_log.getHandValue(screen_area)
    if hand_value in ['top_pair', 'two_pairs', 'set', 'flush', 'straight'] and image_processing.checkIsCbetAvailable(str(screen_area)):
        action = current_stack.compareBankAndAvailableStack(screen_area, image_processing.getStackImages())
        if action == 'turn_cbet':
            keyboard.press('v')
            session_log.updateActionLogSession('turn_cbet', str(screen_area))
            return True
        else:
            keyboard.press('q')
            session_log.updateActionLogSession('push', str(screen_area))
            return True
    if hand_value in ['top_pair', 'two_pairs', 'set', 'flush', 'straight'] or hand_value.find('.') != -1:
        keyboard.press('q')
        session_log.updateActionLogSession('push', str(screen_area))
        return True
    elif int(stack) <= 10 and hand_value in ['middle_pair', 'straight_draw', 'flush_draw', 'low_two_pairs']:
        keyboard.press('q')
        session_log.updateActionLogSession('push', str(screen_area))
    elif image_processing.checkIsCbetAvailable(str(screen_area)):
        keyboard.press('h')
        session_log.updateActionLogSession('cc_postflop', str(screen_area))
        return True
    elif opponent_reaction in ['1', '2'] and hand_value != 'trash':
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

def actionAfterTurnCbet(x_coordinate, y_coordinate, width, height, image_path, screen_area, deck):
    if introduction.checkIsFold(screen_area, x_coordinate, y_coordinate, width, height, image_path): return
    if checkIsRiver(screen_area, deck): return
    if checkIsRaiseCbet(screen_area): return

def checkIsRiver(screen_area, deck):
    element_area = introduction.saveElement(screen_area, 'river_area')
    if image_processing.searchElement(element_area, ['river'], 'green_board/') is False:
        if len(session_log.getActualHand(screen_area)) == 12:
            river = image_processing.searchCards(element_area, deck, 2)
            session_log.updateHandAfterTurn(screen_area, river)
        last_row = session_log.getLastRowFromLogSession(str(screen_area))
        hand = last_row[0][0]
        stack = last_row[0][1]
        action = last_row[0][3]
        if riverAction(screen_area, hand, stack, action):
            return True
    return False

def riverAction(screen_area, hand, stack, action):
    if action == 'turn_cbet':
        keyboard.press('q')
        session_log.updateActionLogSession('push', str(screen_area))
        return True
    opponent_reaction = image_processing.searchLastOpponentAction(screen_area)
    if not isinstance(opponent_reaction, str):
        opponent_reaction = opponent_reaction['alias']
    hand_value = flop.checkPair(hand, screen_area)
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
    elif opponent_reaction in ['1', '2'] and (hand_value in['middle_pair', 'low_two_pairs'] or hand_value.find('middle_pair.') != -1):
        keyboard.press('c')
        session_log.updateActionLogSession('cc_postflop', str(screen_area))
        return True
    elif int(stack) <= 10 and hand_value in['middle_pair', 'low_two_pairs']:
        keyboard.press('q')
        session_log.updateActionLogSession('push', str(screen_area))
    elif hand_value in['middle_pair', 'low_two_pairs'] and image_processing.checkIsCbetAvailable(str(screen_area)):
        keyboard.press('h')
        session_log.updateActionLogSession('cc_postflop', str(screen_area))
        return True
    else:
        keyboard.press('f')
        session_log.updateActionLogSession('fold', str(screen_area))
        return True

def checkIsRaiseCbet(screen_area):
    hand_value = session_log.getHandValue(screen_area)
    opponent_reaction = image_processing.searchLastOpponentAction(screen_area)
    stack = session_log.getLastRowFromLogSession(screen_area)[0]['current_stack']
    if not isinstance(opponent_reaction, str):
        opponent_reaction = opponent_reaction['alias']
    if hand_value.find('.') != -1 or hand_value in ['top_pair', 'two_pairs', 'set', 'flush', 'straight']:
        keyboard.press('q')
        session_log.updateActionLogSession('push', str(screen_area))
        return True
    elif int(stack) <= 10 and hand_value in ['middle_pair', 'straight_draw', 'flush_draw', 'low_two_pairs']:
        keyboard.press('q')
        session_log.updateActionLogSession('push', str(screen_area))
        return True
    elif opponent_reaction in ['1', '2'] and hand_value in ['middle_pair', 'straight_draw', 'flush_draw', 'low_two_pairs']:
        keyboard.press('c')
        session_log.updateActionLogSession('cc_postflop', str(screen_area))
        return True
    else:
        keyboard.press('f')
        session_log.updateActionLogSession('fold', str(screen_area))
        return True

def actionAfterCCPostflop(screen_area, deck, x_coordinate, y_coordinate, width, height, image_path):
    if checkIsRiver(screen_area, deck): return
    if checkIsTurn(screen_area, deck): return
    if introduction.checkIsFold(screen_area, x_coordinate, y_coordinate, width, height, image_path): return
    if getOpponentFlopReaction(screen_area): return

def getOpponentFlopReaction(screen_area):
    hand_value = session_log.getHandValue(screen_area)
    if hand_value is None:
        return False
    opponent_reaction = image_processing.searchLastOpponentAction(screen_area)
    if not isinstance(opponent_reaction, str):
        opponent_reaction = opponent_reaction['alias']
    if opponent_reaction in ['1', '2'] and hand_value != 'trash':
        keyboard.press('c')
        session_log.updateActionLogSession('cc_postflop', str(screen_area))
        return True
    else:
        keyboard.press('f')
        session_log.updateActionLogSession('fold', str(screen_area))
        return True
