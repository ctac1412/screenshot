from tkinter import *
import postgresql
import db_conf

def change():
    screen_area_list = []
    if first.get() != getCurrenValue(1):
        screen_area_list.append(1)
    if second.get() != getCurrenValue(2):
        screen_area_list.append(2)
    if third.get() != getCurrenValue(3):
        screen_area_list.append(3)
    if fourth.get() != getCurrenValue(4):
        screen_area_list.append(4)

    return screen_area_list



def updateCurrentStackLogSession(screen_area):
    print(screen_area)
    if len(screen_area) > 0:
        for item in screen_area:
            db = postgresql.open(db_conf.connectionString())
            db.query("UPDATE screen_coordinates SET active = CASE active WHEN 0 THEN 1 WHEN 1 THEN 0 ELSE active END "
                     "where screen_area = " + str(item))

def getCurrenValue(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select active from screen_coordinates where screen_area = " + str(screen_area))
    return data[0]['active']


root = Tk()

first = IntVar()
first.set(getCurrenValue(1))
second = IntVar()
second.set(getCurrenValue(2))
third = IntVar()
third.set(getCurrenValue(3))
fourth = IntVar()
fourth.set(getCurrenValue(4))
button = Button(text="Изменить", command=lambda:updateCurrentStackLogSession(change()))
button.pack()


c1 = Checkbutton(text="1", variable=first, onvalue=1, offvalue=0)
c1.pack(anchor=W)
c2 = Checkbutton(text="2", variable=second, onvalue=1, offvalue=0)
c2.pack(anchor=W)
c3 = Checkbutton(text="3", variable=third, onvalue=1, offvalue=0)
c3.pack(anchor=W)
c4 = Checkbutton(text="4", variable=fourth, onvalue=1, offvalue=0)
c4.pack(anchor=W)

root.mainloop()