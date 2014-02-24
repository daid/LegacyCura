__author__ = 'Jaime van Kessel'

class View3D(object):
	def __init__(self):
		self._scene = None #A view 3D has a scene responsible for data storage of what is in the 3D world.
		self._renderer_list = [] #The view holds a set of renderers, such as machine renderer or object renderer.
		self._machine = None # Reference to the machine

	def render(self): #todo: Unsure about name.
		for renderer in self._renderer_list:
			renderer.render() #call all render functions

	def addRenderer(self, renderer):
		self._renderer_list.append(renderer);

	def setScene(self,scene):
		self._scene(scene)

	def getScene(self):
		return self._scene

	def setMachine(self,machine):
		self._machine = machine

	def getMachine(self):
		return self._machine
