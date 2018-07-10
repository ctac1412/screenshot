from PIL import Image, ImageGrab
import time
import datetime
import os


folder_name = datetime.datetime.now().date()
if not os.path.exists(str(folder_name)):
    os.makedirs(str(folder_name))

for iteration in range(2):
    img_name = time.strftime("%H-%M-%S")
    time.sleep(1)
    img2 = ImageGrab.grab(bbox=(100, 0, 200, 300))
    img2.save(str(folder_name) + "/" + str(img_name) + ".bmp", "BMP")