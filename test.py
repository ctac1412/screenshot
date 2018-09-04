import postgresql
import db_conf
import cv2
import numpy as np
import error_log
import introduction
import mouse
import current_stack
# btn_open.checkIsActionButtons('1')

def test():
    stack = str(current_stack.searchCurrentStack(str(3)))
    print(stack)
test()