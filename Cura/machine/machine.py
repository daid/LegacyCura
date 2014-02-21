__author__ = 'Jaime van Kessel'

from Cura.machine.setting import Setting
def _(n):
	return n

class Machine(object):
	'''
	Machine is an low level object that holds settings. These settings are shared by all types of machines.
	'''

	def __init__(self):
		self._setting_list = [] #Create a list with which to fill with settings.


		self.addSetting(Setting('machine_width', 10, float, 'basic',    _('Basic')).setRange(0.0001).setLabel(_(""), _("")))

	def addSetting(self, setting):
		self._setting_list.append(setting)

	def getSettingByName(self, name):
		'''
		Get first setting in the list by name
		'''
		return self._findFirstMatch(setting for setting in self._setting_list if setting.getName() == name)

	def setSettingValueByName(self, name, value):
		self.getSettingByName(name).setValue(value)

	def getSettingValueByName(self, name):
		return self.getSettingByName(name).getValue()

	def _findFirstMatch(self,iterable, default = None):
		'''
		Util function that returns first object from an iteratable.
		Might need to move this to util.
		'''
		for item in iterable:
			return item
		return default