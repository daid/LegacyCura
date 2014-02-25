__author__ = 'Jaime van Kessel'

from Cura.machine.setting import Setting
import string
import numpy

def _(n):
	return n

class Machine(object):
	'''
	Machine is an low level object that holds settings. These settings are shared by all types of machines.
	'''

	def __init__(self):
		self._setting_list = [] #Create a list with which to fill with settings.

		#todo; Settings are currently addeded for completeness sake but often have the wrong type
		self.addSetting(Setting('machine_width', 200, float, 'basic',    _('Basic')).setRange(0.0001))
		self.addSetting(Setting('machine_height', 200, float, 'basic',    _('Basic')).setRange(0.0001))
		self.addSetting(Setting('machine_depth', 200, float, 'basic',    _('Basic')).setRange(0.0001))
		self.addSetting(Setting('name','Machine', string, 'basic',    _('Basic')))
		self.addSetting(Setting('icon', '', string, 'basic',    _('Basic')))
		self.addSetting(Setting('display_model', '', string, 'basic',    _('Basic')))

		self._machine_shape = numpy.zeros((0, 2), numpy.float32) #Polygon that forms the 'box' around the machine

	def addSetting(self, setting):
		settingRef = self.getSettingByName(setting.getName())
		if settingRef is None: #Setting doesn't exist yet
			self._setting_list.append(setting)
		else:
			pass #TODO; add handling if setting already exists. (replace setting?)

	def getShape(self):
		return self._machine_shape

	def getSize(self):
		return numpy.array([self.getSettingValueByNameFloat('machine_width'),self.getSettingValueByNameFloat('machine_height'),self.getSettingValueByNameFloat('machine_depth')])

	def getSettingByName(self, name):
		'''
		Get first setting in the list by name
		'''
		return self._findFirstMatch(setting for setting in self._setting_list if setting.getName() == name)

	def setSettingValueByName(self, name, value):
		self.getSettingByName(name).setValue(value)

	def getSettingValueByName(self, name):
		return self.getSettingByName(name).getValue()

	def getSettingValueByNameFloat(self, name):
		try:
			setting = self.getSettingValueByName(name).replace(',', '.')
			return float(eval(setting, {}, {}))
		except:
			return 0.0

	def _findFirstMatch(self,iterable, default = None): #TODO; Might need to move this to util.
		'''
		Function that returns first object from an iteratable.
		'''
		for item in iterable:
			return item
		return default