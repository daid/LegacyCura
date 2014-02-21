__author__ = 'Jaime van Kessel'

class Nozzle(object):
	'''
	Representation of a single (fdm) nozzle
	'''
	def __init__(self, diameter, max_temp, fillament_size):
		self._diameter = diameter
		self._max_temp = max_temp
		self._fillament_size = fillament_size

	def getDiameter(self):
		return self._diameter

	def getMaxTemp(self):
		return self._max_temp

	def getFillamentSize(self):
		return self._fillament_size
