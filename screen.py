from PIL import Image, ImageGrab
import time
import datetime
import os
import math
import postgresql
import pyautogui

images_folder = "images/"

def start():
    # time.sleep(5)
    # pyautogui.click(100, 150)
    checkIsFolderExist()
    folder_name = images_folder + str(datetime.datetime.now().date())
    for iteration in range(3):
        time.sleep(3)
        for item in getScreenData():
            image_name = str(math.floor(time.time()))
            image_path = folder_name + "/" + str(item['screen_area']) + "/" + image_name + ".png"
            image = ImageGrab.grab(bbox=(item['x_coordinate'], item['y_coordinate'], item['width'], item['height']))
            image.save(image_path, "PNG")
            insertImagePathIntoDb(image_path,str(item['screen_area']))


def insertImagePathIntoDb(image_path,screen_area):
    db = postgresql.open('pq://postgres:postgres@localhost:5432/postgres')
    insert = db.prepare("INSERT INTO screenshots (image_path,screen_area) VALUES ($1,$2)")
    insert(image_path,screen_area)

def getScreenData():
    db = postgresql.open('pq://postgres:postgres@localhost:5432/postgres')
    data = db.query("select x_coordinate,y_coordinate,width,height,screen_area from screen_coordinates")
    return data

def checkIsFolderExist():
    folder_name = images_folder + str(datetime.datetime.now().date())
    if not os.path.exists(str(folder_name)):
        os.makedirs(str(folder_name))
    db = postgresql.open('pq://postgres:postgres@localhost:5432/postgres')
    data = db.query("select screen_area from screen_coordinates")
    for value in data:
        if not os.path.exists(str(folder_name) + "/" + str(value['screen_area'])):
            os.makedirs(str(folder_name) + "/" + str(value['screen_area']))

