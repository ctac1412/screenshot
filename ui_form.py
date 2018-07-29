import threading, tkinter, time
import screen
import image_processing

class Window(tkinter.Tk, threading.Thread):
    images_folder = "images/"
    def __init__(self):
        tkinter.Tk.__init__(self)
        threading.Thread.__init__(self)
        self.wait = 1
        self.setDaemon(True)
        self.start()
        self.geometry('150x150')
        self.title('Calculator')
        self.columnconfigure(1, pad=5)

        tkinter.Button(text="start", command=self.Start,width=10).grid(row = 1, column = 1)
        tkinter.Button(text="stop", command=self.Stop).grid(row = 1, column = 2)
        tkinter.Button(text='Exit', command=lambda: self.destroy()).grid(row=2, column=1)
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