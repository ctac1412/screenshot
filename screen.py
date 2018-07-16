from PIL import Image, ImageGrab
import time
import datetime
import os
import math
import postgresql

images_folder = "images/"

def start():
    folder_name = images_folder + str(datetime.datetime.now().date())
    time.sleep(2)
    for item in getScreenData():
        image_name = str(math.floor(time.time()))
        image_path = folder_name + "/" + str(item['screen_area']) + "/" + image_name + ".png"
        image = ImageGrab.grab(bbox=(item['x_coordinate'], item['y_coordinate'], item['width'], item['height']))
        image.save(image_path, "PNG")
        insertImagePathIntoDb(image_path, str(item['screen_area']))



def insertImagePathIntoDb(image_path,screen_area):
    db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
    insert = db.prepare("insert into screenshots (image_path,screen_area) values($1,$2)")
    insert(image_path,screen_area)

def getScreenData():
    db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
    data = db.query("select x_coordinate,y_coordinate,width,height,screen_area from screen_coordinates")
    return data

def checkIsFolderExist():
    folder_name = images_folder + str(datetime.datetime.now().date())
    if not os.path.exists(str(folder_name)):
        os.makedirs(str(folder_name))
    db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
    data = db.query("select screen_area from screen_coordinates")
    for value in data:
        if not os.path.exists(str(folder_name) + "/" + str(value['screen_area'])):
            os.makedirs(str(folder_name) + "/" + str(value['screen_area']))

def getCards():
    db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
    data = db.query("select trim(image_path) as image_path,card,suit,trim(alias) as alias from cards")
    return data

def getLastScreen(screen_area):
    db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
    data = db.query("select trim(image_path)as image_path from screenshots where screen_area = " + screen_area + " order by id desc limit 1")
    return data