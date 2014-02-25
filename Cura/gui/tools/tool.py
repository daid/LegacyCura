__author__ = 'Jaime van Kessel'

class Tool(object):
	'''
	Interface class for all tools. Holds entry points for events.
	Tools are handlers for interaction with a view.
	'''
	def __int__(self):
		self._scene = None #Reference to Scene object
		self._view = None


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

	def setView(self,view):
		self._view = view

	def setScene(self, scene):
		self._scene = scene