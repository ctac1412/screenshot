import flop

hand = '3h6hQc3hAh'
# print(flop.checkPair('3h6s3c3h3s'))

# if flop.checkPair(hand) or flop.checkStraightDraw(hand) or flop.checkFlushDraw(hand):
#     print()
if flop.image_processing.checkIsCbetAvailable(str(3)):
    print(1)
else:print(2)