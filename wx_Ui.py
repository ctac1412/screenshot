# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Mar 13 2019)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx_form_UI
import win32con
import test
import time
import postgresql
import screen
import image_processing
import db_query
import datetime
 # first line below is necessary only in wxPython 2.8.11.0 since default 
# API in this wxPython is pubsub version 1 (expect later versions 
# of wxPython to use the kwargs API by default)
from wx.lib.pubsub import setupkwargs
from threading import Thread
# regular pubsub import
from wx.lib.pubsub import pub

#######################################################################
class TestThread(Thread):
    """Test Worker Thread Class."""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.start()    # start the thread
 
    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        screen.start()
        wx.CallAfter(lambda: pub.sendMessage('screen.end', msg="Thread finished!"))

class Calculator ( wx_form_UI.Calculator ):
    
    def __init__(self, parent):
        super(Calculator, self).__init__(parent)
        
        self.regHotKey()
        self.Bind(wx.EVT_HOTKEY, self.handleHotKeyF1, id=100)
        self.Bind(wx.EVT_HOTKEY, self.handleHotKeyF2, id=200)
        
        self.wait = 1

        self.is_slot_1.SetValue(self.get_curren_value(1)) # Устанавливаем значение переменной
        self.is_slot_2.SetValue(self.get_curren_value(2))
        self.is_slot_3.SetValue(self.get_curren_value(3))
        self.is_slot_4.SetValue(self.get_curren_value(4))
        
        image_processing.check_is_folder_exist()

        pub.subscribe(self._screen_message_getter, 'screen.end')

    def _screen_message_getter(self, msg):
        # no longer need to access data through message.data.
        self.stateLabel.SetLabel(("Last itteration on: %s" % datetime.datetime.now()))
        if not self.wait:
            self.on_buttonStart(None)

    # def updateDisplay(self, msg):
    #     """
    #     Receives data from thread and updates the display
    #     """
    #     print(msg)
    #     t = msg
    #     if isinstance(t, int):
    #         label_msg =  ("Time since thread started: %s seconds" % t)
    #     else:
    #         label_msg = ("Time since thread started: %s seconds" % t)
    #     self.stateLabel.SetLabel(label_msg)

    def get_curren_value(self, screen_area):
        db = postgresql.open(db_query.connection_string())
        data = db.query("select active from screen_coordinates where screen_area = " + str(screen_area))
        return data[0]['active']

    def update_current_stack_log_session(self, screen_area):
        if len(screen_area) > 0:
            for item in screen_area:
                db = postgresql.open(db_query.connection_string())
                db.query(
                    "UPDATE screen_coordinates SET active = CASE active WHEN 0 THEN 1 WHEN 1 THEN 0 ELSE active END "
                    "where screen_area = " + str(item))

    def truncate_screenshot_table(self):
        db = postgresql.open(db_query.connection_string())
        db.query("truncate screenshots restart identity")


    def on_buttonStart( self, event ):
        self.wait = 0
        TestThread()

    def on_buttonStop( self, event ):
        self.wait = 1

    def on_buttonUpdate( self, event ):
        event.Skip()

    def on_buttonTruncate( self, event ):
        event.Skip()

    def resetShot( self, event ):
        image_path = u"C:\\Users\\Stas\\Desktop\\github\\screenshot\\images\\2019-03-17\\1\\test.png"
        hwnd = test.get_active_window()
        workspace_area = test.registarte_coordinate_and_size(228, 232, 60, 39)
        test.make_relative_screen(hwnd,image_path,workspace_area)
        # self.LastShot = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        self.LastShot.Bitmap  = wx.Bitmap( u"C:\\Users\\Stas\\Desktop\\github\\screenshot\\images\\2019-03-17\\1\\test.png", wx.BITMAP_TYPE_ANY )

    def regHotKey(self):
        """
        This function registers the hotkey Alt+F1 with id=100
        """
        self.RegisterHotKey(
            100, #a unique ID for this hotkey
            win32con.MOD_ALT, #the modifier key
            win32con.VK_F1) #the key to watch for
        self.RegisterHotKey(
            200, #a unique ID for this hotkey
            win32con.MOD_ALT, #the modifier key
            win32con.VK_F2) #the key to watch for

    def handleHotKeyF1(self, evt):
        """
        Prints a simple message when a hotkey event is received.
        """
        print("alt + F1")
        self.resetShot(None)

    def handleHotKeyF2(self, evt):
        """
        Prints a simple message when a hotkey event is received.
        """
        self.wait = 1
        print("alt + F2")

app = wx.App(False)
frame = Calculator(None)
frame.Show()
app.MainLoop()