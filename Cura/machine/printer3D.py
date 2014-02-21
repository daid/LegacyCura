__author__ = 'Jaime van Kessel'

from Cura.machine import machine
from Cura.machine.setting import Setting

class Printer3D(machine.Machine):
	'''
	Class that holds settings for any kind of 3D printers
	'''
	def __init__(self):
		self.addSetting(Setting('build_area', 0, int)) #Todo: build area needs to be a 2d poly with height
		self.addSetting(Setting('layer_height',0.2,float))
		