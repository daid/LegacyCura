__author__ = 'Jaime van Kessel'

class Tool(object):
	'''
	Interface class for all tools. Holds entry points for events.
	Tools are handlers for interaction with a view.
	'''
	def __init__(self):
		self._scene = None #Reference to Scene object
		self._view = None
		self._mouse_x = -1
		self._mouse_y = -1

	def onMouseUp(self, e):
		pass

	def onMouseDown(self, e):
		pass

	def onMouseMotion(self, e):
		pass

	def onMouseWheel(self,e):
		pass

	def onKeyChar(self,e):
		pass

	def onMouseWheel(self,e):
		pass

	def getMousePos(self):
		return self._mouse_x, self._mouse_y

	def setView(self,view):
		self._view = view

	def setScene(self, scene):
		self._scene = scene