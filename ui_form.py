import threading, tkinter, time
import screen
import image_processing
# from tkinter import *
import postgresql
import db_conf

class Window(tkinter.Tk, threading.Thread):
    images_folder = "images/"

    def getCurrenValue(self,screen_area):
        self.screen_area = screen_area
        db = postgresql.open(db_conf.connectionString())
        data = db.query("select active from screen_coordinates where screen_area = " + str(screen_area))
        return data[0]['active']

    def __init__(self):
        print(self.getCurrenValue(3))
        tkinter.Tk.__init__(self)
        threading.Thread.__init__(self)
        self.wait = 1
        self.setDaemon(True)
        self.start()
        self.geometry('150x150')
        self.title('Calculator')
        self.columnconfigure(1, pad=5)

        # first = IntVar()
        # first.set(self.getCurrenValue(1))
        # second = IntVar()
        # second.set(self.getCurrenValue(2))
        # third = IntVar()
        # third.set(self.getCurrenValue(3))
        # fourth = IntVar()
        # fourth.set(self.getCurrenValue(4))

        tkinter.Button(text="start", command=self.Start,width=10).grid(row = 1, column = 1)
        tkinter.Button(text="stop", command=self.Stop).grid(row = 1, column = 2)
        tkinter.Button(text='Exit', command=lambda: self.destroy()).grid(row=2, column=1)
        # tkinter.Checkbutton(text="1", variable=1, onvalue=1, offvalue=0).grid(row=3, column=1)
        # tkinter.Checkbutton(text="2", variable=second, onvalue=1, offvalue=0).grid(row=3, column=2)
        # tkinter.Checkbutton(text="3", variable=third, onvalue=1, offvalue=0).grid(row=4, column=1)
        # tkinter.Checkbutton(text="4", variable=fourth, onvalue=1, offvalue=0).grid(row=4, column=2)
        self.bind("<Key>", self.keydown)

        def destroy():
            self.wait = -1
            time.sleep(1)
            self.destroy()
        self.protocol("WM_DELETE_WINDOW", destroy)

    def keydown(self,e):
        if e.char == 'x':
            self.destroy()
    def Stop(self): self.wait = 1
    def Start(self): self.wait = 0
    def run(self):
        print('thread.start')
        while self.wait >= 0:
            if self.wait: time.sleep(self.wait)
            else:
                self._target = self.work
                self._args = ()
                self._kwargs = {}
                super().run()
        print('thread.stop')

    def work(self):
        image_processing.checkIsFolderExist()
        while not self.wait:
            screen.start()
        print('выход')

if __name__ == '__main__':
    Window().mainloop()

def keydown(e):
    print('down', e.char)



