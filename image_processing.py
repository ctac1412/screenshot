import cv2
import numpy as np
import postgresql
import os
import datetime

#Поиск карт игрока на скрине
def searchPlayerHand(screen_area):
    hand = ''
    for value in getCards():
        try:
            img_rgb = cv2.imread(getLastScreen(screen_area), 0)
            template = cv2.imread(str(value['image_path']), 0)

            res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.98
            loc = np.where(res >= threshold)

            if (len(loc[0]) != 0):
                hand += value['alias']

        except Exception as e:
            print(str(value['image_path']))
    return hand

images_folder = "images/"

#Вставка пути к изображению в бд
def insertImagePathIntoDb(image_path,screen_area):
    db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
    insert = db.prepare("insert into screenshots (image_path,screen_area) values($1,$2)")
    insert(image_path,screen_area)

#Получение информации об области экрана, на которой будет делаться скриншот
def getScreenData():
    db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
    data = db.query("select x_coordinate,y_coordinate,width,height,screen_area from screen_coordinates")
    return data

#Проверка на существование папок
def checkIsFolderExist():
    folder_name = images_folder + str(datetime.datetime.now().date())
    if not os.path.exists(str(folder_name)):
        os.makedirs(str(folder_name))
    db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
    data = db.query("select screen_area from screen_coordinates")
    for value in data:
        if not os.path.exists(str(folder_name) + "/" + str(value['screen_area'])):
            os.makedirs(str(folder_name) + "/" + str(value['screen_area']))

#Получение путей к изображениям шаблонов карт
def getCards():
    db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
    data = db.query("select trim(image_path) as image_path,card,suit,trim(alias) as alias from cards")
    return data

#Получение последнего скрина для текущей области экрана
def getLastScreen(screen_area):
    db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
    data = db.query("select trim(image_path)as image_path from screenshots where screen_area = " + screen_area + " order by id desc limit 1")
    return data