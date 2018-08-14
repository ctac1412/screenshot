import logic
import sklansky_chubukov

hand = logic.handConverting('9sKs')
print(sklansky_chubukov.getValidStackValueToPush(hand))