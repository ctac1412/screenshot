import flop
import session_log
import image_processing
# hand = '5h4h4c6h7s'
# # print(flop.checkPair('3h6s3c3h3s'))
#
# if flop.checkPair(hand) or flop.checkStraightDraw(hand) or flop.checkFlushDraw(hand):
#     print(1)

# row = session_log.getLastRowFromLogSession('3')
print(session_log.getLastRowFromLogSession('3')[0]['current_stack'])