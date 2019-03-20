import threading
import tkinter
import time
import postgresql
import screen
import image_processing
import db_query

class Window(tkinter.Tk, threading.Thread):
    def __init__(self):
        # Инициализируем графический интерфейс
        tkinter.Tk.__init__(self)
        threading.Thread.__init__(self)
        self.wait = 1
        self.setDaemon(True)
        self.start()
        self.geometry('200x120+0+640')
        self.title('Calculator')
        self.columnconfigure(1, pad=5)

        tkinter.Button(text="start", command=self.Start, width=10).grid(row=1, column=1)
        tkinter.Button(text="stop", command=self.stop, width=10).grid(row=1, column=3)
        tkinter.Button(text='Exit', command=lambda: self.destroy()).grid(row=1, column=2)
        tkinter.Button(text='Update', command=lambda: update_current_stack_log_session(change())).grid(row=5, column=1)
        tkinter.Button(text='Truncate', command=lambda: truncate_screenshot_table()).grid(row=5, column=2)

        self.first = tkinter.IntVar()
        tkinter.Checkbutton(text="1", variable=self.first, onvalue=1, offvalue=0).grid(row=3,
                                                                                       column=1)
        self.second = tkinter.IntVar()
        tkinter.Checkbutton(text="2", variable=self.second, onvalue=1, offvalue=0).grid(row=3,
                                                                                        column=2)
        self.third = tkinter.IntVar()
        tkinter.Checkbutton(text="3", variable=self.third, onvalue=1, offvalue=0).grid(row=4,
                                                                                       column=1)
        self.fourth = tkinter.IntVar()
        tkinter.Checkbutton(text="4", variable=self.fourth, onvalue=1, offvalue=0).grid(row=4,
                                                                                        column=2)

        # Потом бизнес-логика

        def get_curren_value(screen_area):
            db = postgresql.open(db_query.connection_string())
            data = db.query("select active from screen_coordinates where screen_area = " + str(screen_area))
            return data[0]['active']

        def update_current_stack_log_session(screen_area):
            if len(screen_area) > 0:
                for item in screen_area:
                    db = postgresql.open(db_query.connection_string())
                    db.query(
                        "UPDATE screen_coordinates SET active = CASE active WHEN 0 THEN 1 WHEN 1 THEN 0 ELSE active END "
                        "where screen_area = " + str(item))

        def truncate_screenshot_table():
            db = postgresql.open(db_query.connection_string())
            db.query("truncate screenshots restart identity")

        self.first.set(get_curren_value(1))  # Устанавливаем значение переменной
        self.second.set(get_curren_value(2))
        self.third.set(get_curren_value(3))
        self.fourth.set(get_curren_value(4))

        def change():
            screen_area_list = []
            if self.first.get() != get_curren_value(1):
                screen_area_list.append(1)
                screen_area_list.append(14)
                screen_area_list.append(20)
            if self.second.get() != get_curren_value(2):
                screen_area_list.append(2)
                screen_area_list.append(13)
                screen_area_list.append(19)
            if self.third.get() != get_curren_value(3):
                screen_area_list.append(3)
                screen_area_list.append(16)
                screen_area_list.append(18)
            if self.fourth.get() != get_curren_value(4):
                screen_area_list.append(4)
                screen_area_list.append(15)
                screen_area_list.append(17)

            return screen_area_list

        self.bind("<Key>", self.keydown)

        def destroy():
            self.wait = -1
            time.sleep(1)
            self.destroy()

        self.protocol("WM_DELETE_WINDOW", destroy)

    def keydown(self, e):
        if e.char == 'x':
            self.destroy()

    def stop(self):
        self.wait = 1

    def Start(self):
        self.wait = 0

    def run(self):
        print('thread.start')
        while self.wait >= 0:
            if self.wait:
                time.sleep(self.wait)
            else:
                self._target = self.work
                self._args = ()
                self._kwargs = {}
                super().run()
        print('thread.stop')

    def work(self):
        image_processing.check_is_folder_exist()
        while not self.wait:
            screen.start()


if __name__ == '__main__':
    print('ds')
    Window().mainloop()
    # import wx
    # app = wx.App()
    # # frame = wx.Frame(None, -1, "Title here")
    # # frame.Show()
    # # app.MainLoop()
    # FrameWithHotKey()

def keydown(e):
    print('down', e.char)
