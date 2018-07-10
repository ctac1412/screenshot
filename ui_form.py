from tkinter import *
import screen

root = Tk()
root.title("Tk dropdown example")
root.geometry('200x200')

# Add a grid
mainframe = Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))




# Create a Tkinter variable
tkvar = StringVar(root)

# Dictionary with options
choices = {1,2,3,4}
tkvar.set('1')  # set the default option
Button(root, text = 'Start', command=lambda:screen.start(),width=10).grid(row = 1, column = 1)
#Button(root, text = 'Stop').grid(row = 1, column = 2)
#popupMenu = OptionMenu(mainframe, tkvar, *choices)
#popupMenu.grid(row = 1, column = 1)



# on change dropdown value
def change_dropdown(*args):
    print(tkvar.get())


# link function to change dropdown
tkvar.trace('w', change_dropdown)

root.mainloop()