__author__ = 'Jaime van Kessel'

from Cura.gui.tools.tool import Tool
import wx

class KeyboardTool(Tool):
	def __init__(self):
		super(KeyboardTool,self).__init__()

	def onKeyChar(self, e):
		key_code = e.GetKeyCode()
		if key_code == wx.WXK_UP:
			print "UP"
		pass