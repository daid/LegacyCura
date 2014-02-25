__author__ = 'Jaime van Kessel'

class Scene(object):
	'''
	Base scene class. Holds all objects (all objects on platform, etc) in the 3D world.
	'''
	def __init__(self):
		self._machine = None #Scene has a reference to the machine
		self._object_list = []

	def getObjects(self):
		return self._object_list

	def getSelectedObject(self): #Todo: Implement
		return None
