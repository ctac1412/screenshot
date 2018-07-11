from PIL import Image, ImageGrab
import time
import datetime
import os
import math
import postgresql
# db = postgresql.open('pq://postgres:postgres@localhost:5432/postgres')
# db.execute("CREATE TABLE screenshots (id SERIAL PRIMARY KEY, "
#                "image_path CHAR(64), screen_area CHAR(2), created_at TIMESTAMP DEFAULT NOW())")
def start():
    folder_name = datetime.datetime.now().date()
    if not os.path.exists(str(folder_name)):
        os.makedirs(str(folder_name))

    if not os.path.exists(str(folder_name) + "/1"):
        os.makedirs(str(folder_name) + "/1")

    if not os.path.exists(str(folder_name) + "/2"):
        os.makedirs(str(folder_name) + "/2")

    if not os.path.exists(str(folder_name) + "/3"):
        os.makedirs(str(folder_name) + "/3")

    if not os.path.exists(str(folder_name) + "/4"):
        os.makedirs(str(folder_name) + "/4")

    for iteration in range(3):
        img_name = math.floor(time.time())
        time.sleep(1)
        
        img1 = ImageGrab.grab(bbox=(0, 0, 300, 300))
        img1.save(str(folder_name) + "/1/" + str(img_name) + ".png", "PNG")
        insertImagePathIntoDb(str(folder_name) + "/1/" + str(img_name) + ".png","1")

        img2 = ImageGrab.grab(bbox=(300, 0, 600, 300))
        img2.save(str(folder_name) + "/2/" + str(img_name) + ".png", "PNG")
        insertImagePathIntoDb(str(folder_name) + "/2/" + str(img_name) + ".png","2")

        img3 = ImageGrab.grab(bbox=(0, 300, 300, 600))
        img3.save(str(folder_name) + "/3/" + str(img_name) + ".png", "PNG")
        insertImagePathIntoDb(str(folder_name) + "/3/" + str(img_name) + ".png","3")

        img4 = ImageGrab.grab(bbox=(300, 300, 600, 600))
        img4.save(str(folder_name) + "/4/" + str(img_name) + ".png", "PNG")
        insertImagePathIntoDb(str(folder_name) + "/4/" + str(img_name) + ".png","4")


def insertImagePathIntoDb(image_path,screen_area):
    db = postgresql.open('pq://postgres:postgres@localhost:5432/postgres')
    insert = db.prepare("INSERT INTO screenshots (image_path,screen_area) VALUES ($1,$2)")
    insert(image_path,screen_area)



