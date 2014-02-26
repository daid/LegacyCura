__author__ = 'Jaime van Kessel'

from Cura.machine import printer3D
from Cura.machine.nozzle import Nozzle
import numpy

class FDMPrinter(printer3D.Printer3D):
	'''
	Class that holds settings for any kind of FDMPrinter
	'''
	def __init__(self):
		super(FDMPrinter,self).__init__()
		self._nozzles = []

		self.addNozzle(Nozzle(0.4,260,2.85))


		#def getMachineSizePolygons():
		size = self.getSize()
		ret = []
		ret.append(numpy.array([[-size[0]/2,-size[1]/2],[size[0]/2,-size[1]/2],[size[0]/2, size[1]/2], [-size[0]/2, size[1]/2]], numpy.float32))
		self._machine_shape = ret
	def addNozzle(self, nozzle):
		self._nozzles.append(nozzle)

	def getNozzle(self,index = 0):
		if len(self._nozzles) > index:
			return self._nozzles[len(self._nozzles)]
		return self._nozzles[index]