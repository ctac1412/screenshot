import time
import flop
import session_log

# hand = 'Qs6hJcAdKh'
last_row = session_log.getLastRowFromLogSession(str(2))
hand = last_row[0][0]
stack = last_row[0][1]
action = last_row[0][3]

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap

# timing(flop.makeFlopDecision('2', hand, 'test','test',stack,action))
# print(hand)
flop.makeFlopDecision('1', hand, 'test','test',stack,action)