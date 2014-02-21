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


		self.addSetting(Setting('layer_height',              0.1, float, 'basic',    _('Quality')).setRange(0.0001).setLabel(_("Layer height (mm)"), _("Layer height in millimeters.\nThis is the most important setting to determine the quality of your print. Normal quality prints are 0.1mm, high quality is 0.06mm. You can go up to 0.25mm with an Ultimaker for very fast prints at low quality.")))

	def addSetting(self, setting):
		self._setting_list.append(setting)