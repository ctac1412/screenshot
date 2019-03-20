
import os
import time
import datetime
import math
import postgresql
import image_processing
import session_log
import mouse
import introduction
import bar as metka
import postflop
import db_query
import image_processing
import win32gui, win32con

IMAGES_FOLDER = "images/"
FOLDER_NAME = IMAGES_FOLDER + str(datetime.datetime.now().date())
DB = postgresql.open(db_query.connection_string())
SCREEN_DATA = db_query.get_screen_data(DB)
DECK = db_query.get_cards(DB)
STACK_COLLECTION = db_query.get_stack_images(DB)

screen_area = SCREEN_DATA[0]
# image_path = os.path.join(r'C:\Users\Stas\Desktop\github\screenshot\cards', 'ace_clubs.png')
image_path = os.path.join(r'C:\Users\Stas\Desktop\github\screenshot\images\2019-03-17\1', 'test.png')

def get_location_and_size(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    print("Window %s:" % win32gui.GetWindowText(hwnd))
    print("\tLocation: (x:%d, y:%d)" % (x, y))
    print("\t    Size: (w:%d, h:%d)" % (w, h))
    return x, y, w, h

# Location: (135, 0)
#             Size: (517, )


# def get_hwnds(pid):
#     """return a list of window handlers based on it process id"""
#     def callback(hwnd, hwnds):
#         if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
#             _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
#             if found_pid == pid:
#                 hwnds.append(hwnd)
#         return True
#     hwnds = []
#     win32gui.EnumWindows(callback, hwnds)
#     return hwn
# hwnds = get_hwnds()


hwnd = win32gui.GetForegroundWindow()
print(win32gui.GetWindowText(hwnd))
hwnd = win32gui.FindWindow(None, win32gui.GetWindowText(hwnd))

x, y, w, h = get_location_and_size(hwnd)
# 363	244	61	27
x += 363 - x
y += 232 - y
rect = win32gui.GetWindowRect(hwnd)
w = 60
h = 37
# w = 423
# h = 271
print("\tNew RECT")
print("\tLocation: (x:%d, y:%d)" % (x, y))
print("\t    Size: (w:%d, h:%d)" % (w, h))

# image_processing.imaging(x, y, w, h, image_path, None, DB )
# x_coordinate, y_coordinate, width, height, image_path, screen_area, db
hand = image_processing.search_cards(screen_area, DECK, 4, DB)
print(hand)
# import wx
# # import wx
# import win32con #for the VK keycodes
# class ExampleFrame(wx.Frame):
#     def __init__(self, parent):
#         wx.Frame.__init__(self, parent)

#         self.panel = wx.Panel(self)     
#         self.quote = wx.StaticText(self.panel, label="Your quote:")
#         self.result = wx.StaticText(self.panel, label="")
#         self.result.SetForegroundColour(wx.RED)
#         self.button = wx.Button(self.panel, label="Save")
#         self.lblname = wx.StaticText(self.panel, label="Your name:")
#         self.editname = wx.TextCtrl(self.panel, size=(140, -1))

#         # Set sizer for the frame, so we can change frame size to match widgets
#         self.windowSizer = wx.BoxSizer()
#         self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)        

#         # Set sizer for the panel content
#         self.sizer = wx.GridBagSizer(5, 5)
#         self.sizer.Add(self.quote, (0, 0))
#         self.sizer.Add(self.result, (0, 1))
#         self.sizer.Add(self.lblname, (1, 0))
#         self.sizer.Add(self.editname, (1, 1))
#         self.sizer.Add(self.button, (2, 0), (1, 2), flag=wx.EXPAND)

#         # Set simple sizer for a nice border
#         self.border = wx.BoxSizer()
#         self.border.Add(self.sizer, 1, wx.ALL | wx.EXPAND, 5)

#         # Use the sizers
#         self.panel.SetSizerAndFit(self.border)  
#         self.SetSizerAndFit(self.windowSizer)  

#         # Set event handlers
#         self.button.Bind(wx.EVT_BUTTON, self.OnButton)

#         self.regHotKey()
#         self.Bind(wx.EVT_HOTKEY, self.handleHotKey, id=self.hotKeyId)

#     def regHotKey(self):
#         """
#         This function registers the hotkey Alt+F1 with id=100
#         """
#         self.hotKeyId = 100
#         self.RegisterHotKey(
#             self.hotKeyId, #a unique ID for this hotkey
#             win32con.MOD_ALT, #the modifier key
#             win32con.VK_F1) #the key to watch for
#         print ("do hot 2222222222")

#     def handleHotKey(self, evt):
#         """
#         Prints a simple message when a hotkey event is received.
#         """
#         print ("do hot key actions")

#     def OnButton(self, e):
#         self.result.SetLabel(self.editname.GetValue())

# app = wx.App(False)
# frame = ExampleFrame(None)
# frame.Show()
# app.MainLoop()