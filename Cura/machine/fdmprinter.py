__author__ = 'Jaime van Kessel'

from Cura.machine import printer3D
from Cura.machine.nozzle import Nozzle

class FDMPrinter(printer3D.Printer3D):
	'''
	Class that holds settings for any kind of FDMPrinter
	'''
	def __init__(self):
		self._nozzles = []

		self.addNozzle(Nozzle(0.4,260,2,85))
		pass

	def addNozzle(self, nozzle):
		self._nozzles.append(nozzle)

	def getNozzle(self,index = 0):
		if len(self._nozzles) > index:
			return self._nozzles[len(self._nozzles)]
		return self._nozzles[index]