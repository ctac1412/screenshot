# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Mar 13 2019)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class Calculator
###########################################################################

class Calculator ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 409,323 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.m_scrolledWindow1 = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow1.SetScrollRate( 5, 5 )
		bSizer1.Add( self.m_scrolledWindow1, 0, wx.ALL, 1 )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

		gSizer2 = wx.GridSizer( 0, 2, 0, 0 )

		self.Start = wx.Button( self, wx.ID_ANY, u"Запустить", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.Start, 0, wx.ALL, 5 )

		self.Stop = wx.Button( self, wx.ID_ANY, u"Остановить", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.Stop, 0, wx.ALL, 5 )

		self.Update = wx.Button( self, wx.ID_ANY, u"Update", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.Update, 0, wx.ALL, 5 )

		self.Truncate = wx.Button( self, wx.ID_ANY, u"Truncate", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.Truncate, 0, wx.ALL, 5 )

		self.shootScreen = wx.Button( self, wx.ID_ANY, u"Shoot screen", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.shootScreen, 0, wx.ALL, 5 )


		bSizer11.Add( gSizer2, 0, 0, 1 )

		gSizer6 = wx.GridSizer( 0, 2, 0, 0 )

		self.is_slot_1 = wx.CheckBox( self, wx.ID_ANY, u"Слот 1", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.is_slot_1.SetValue(True)
		gSizer6.Add( self.is_slot_1, 0, wx.ALL, 5 )

		self.is_slot_2 = wx.CheckBox( self, wx.ID_ANY, u"Слот 2", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer6.Add( self.is_slot_2, 0, wx.ALL, 5 )

		self.is_slot_4 = wx.CheckBox( self, wx.ID_ANY, u"Слот 4", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer6.Add( self.is_slot_4, 0, wx.ALL, 5 )

		self.is_slot_3 = wx.CheckBox( self, wx.ID_ANY, u"Слот 3", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer6.Add( self.is_slot_3, 0, wx.ALL, 5 )


		bSizer11.Add( gSizer6, 0, 0, 1 )


		bSizer1.Add( bSizer11, 0, wx.EXPAND, 1 )

		self.stateLabel = wx.StaticText( self, wx.ID_ANY, u"Статус", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stateLabel.Wrap( -1 )

		bSizer1.Add( self.stateLabel, 0, wx.ALL, 5 )

		self.LastShot = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		bSizer1.Add( self.LastShot, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Start.Bind( wx.EVT_BUTTON, self.on_buttonStart )
		self.Stop.Bind( wx.EVT_BUTTON, self.on_buttonStop )
		self.Update.Bind( wx.EVT_BUTTON, self.on_buttonUpdate )
		self.Truncate.Bind( wx.EVT_BUTTON, self.on_buttonTruncate )
		self.shootScreen.Bind( wx.EVT_BUTTON, self.resetShot )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def on_buttonStart( self, event ):
		event.Skip()

	def on_buttonStop( self, event ):
		event.Skip()

	def on_buttonUpdate( self, event ):
		event.Skip()

	def on_buttonTruncate( self, event ):
		event.Skip()

	def resetShot( self, event ):
		event.Skip()


