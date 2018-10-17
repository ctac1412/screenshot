import postgresql
import db_conf
import session_log
import introduction
import image_processing

def insertHandAfterFlop(screen_area, hand):
    db = postgresql.open(db_conf.connectionString())
    db.query("insert into postflop_hand(hand, screen_area)"
             "select '" + hand + "'," + screen_area)

def checkIsTurn(screen_area, image_name, folder_name, flop_deck):
    element_area = introduction.saveElement(screen_area, 'turn_area')
    if image_processing.searchElement(element_area, ['turn'], 'green_board/') is False:
        turn = image_processing.searchCards(screen_area, image_processing.getCards(), 2)
        session_log.updateHandAfterTurn(screen_area, turn)
        # last_row = session_log.getLastRowFromLogSession(str(screen_area))
        # hand = last_row[0][0]
        # stack = last_row[0][1]
        # action = last_row[0][3]
        # is_headsup = last_row[0][4]
        # flop.makeFlopDecision(str(screen_area), hand, image_name, folder_name, stack, action, is_headsup, flop_deck)
        # return True