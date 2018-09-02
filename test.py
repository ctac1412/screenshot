import postgresql
import db_conf
import cv2
import numpy as np
import error_log
import btn_open
import mouse
# btn_open.checkIsActionButtons('1')

def test():
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select trim(image_path) as image_path from stack where stack_value = 50")
    print(len(data))
test()