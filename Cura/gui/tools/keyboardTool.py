__author__ = 'Jaime van Kessel'

from Cura.gui.tools.tool import Tool

class KeyboardTool(Tool):
	def __init__(self):
		super(KeyboardTool,self).__init__()

	def onKeyChar(self, keychar):
		pass