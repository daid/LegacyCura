__copyright__ = "Copyright (C) 2013 David Braam - Released under terms of the AGPLv3 License"

import wx
import ConfigParser as configparser
import os.path

from Cura.util import profile
from Cura.util import resources

class simpleModePanel(wx.Panel):
	"Main user interface window for Quickprint mode"
	def __init__(self, parent, callback):
		super(simpleModePanel, self).__init__(parent)

		self._callback = callback

		self._print_profile_options = []
		self._print_material_options = []
		self._print_nozzle_options = []

		nozzle_options = []
		printTypePanel = wx.Panel(self)
		for filename in resources.getSimpleModeProfiles(profile.getMachineSetting('machine_type')):
			cp = configparser.ConfigParser()
			cp.read(filename)
			base_filename = os.path.splitext(os.path.basename(filename))[0]
			name = base_filename
			if cp.has_option('info', 'name'):
				name = cp.get('info', 'name')
			nozzle = profile.getProfileSetting('nozzle_size')
			if cp.has_option('profile', 'nozzle_size'):
				nozzle = cp.get('profile', 'nozzle_size')
				if nozzle not in nozzle_options:
					nozzle_options.append(nozzle)
			for button in self._print_profile_options:
				if button.GetLabel() == name:
					button.filename[nozzle] = filename
					nozzle = None

			if nozzle is not None:
				button = wx.RadioButton(printTypePanel, -1, name, style=wx.RB_GROUP if len(self._print_profile_options) == 0 else 0)
				button.base_filename = base_filename
				button.filename = {nozzle: filename}
				self._print_profile_options.append(button)
				if profile.getPreference('simpleModeProfile') == base_filename:
					button.SetValue(True)

		printMaterialPanel = wx.Panel(self)
		for filename in resources.getSimpleModeMaterials():
			cp = configparser.ConfigParser()
			cp.read(filename)
			base_filename = os.path.splitext(os.path.basename(filename))[0]
			name = base_filename
			if cp.has_option('info', 'name'):
				name = cp.get('info', 'name')
			button = wx.RadioButton(printMaterialPanel, -1, name, style=wx.RB_GROUP if len(self._print_material_options) == 0 else 0)
			button.base_filename = base_filename
			button.filename = filename
			self._print_material_options.append(button)
			if profile.getPreference('simpleModeMaterial') == base_filename:
				button.SetValue(True)

		printNozzlePanel = wx.Panel(self)
		for nozzle_size in nozzle_options:
			name = str(nozzle_size) + "mm"
			button = wx.RadioButton(printNozzlePanel, -1, name, style=wx.RB_GROUP if len(self._print_nozzle_options) == 0 else 0)
			button.nozzle_size = nozzle_size
			button.nozzle_name = name
			self._print_nozzle_options.append(button)
			if profile.getPreference('simpleModeNozzle') == name:
				button.SetValue(True)

		if profile.getMachineSetting('gcode_flavor') == 'UltiGCode':
			printMaterialPanel.Show(False)
		if len(nozzle_options) < 1:
			printNozzlePanel.Show(False)

		self.printSupport = wx.CheckBox(self, -1, _("Print support structure"))

		sizer = wx.GridBagSizer()
		self.SetSizer(sizer)

		sb = wx.StaticBox(printTypePanel, label=_("Select a quickprint profile:"))
		boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
		for button in self._print_profile_options:
			boxsizer.Add(button)
		printTypePanel.SetSizer(wx.BoxSizer(wx.VERTICAL))
		printTypePanel.GetSizer().Add(boxsizer, flag=wx.EXPAND)
		sizer.Add(printTypePanel, (0,0), flag=wx.EXPAND)

		sb = wx.StaticBox(printMaterialPanel, label=_("Material:"))
		boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
		for button in self._print_material_options:
			boxsizer.Add(button)
		printMaterialPanel.SetSizer(wx.BoxSizer(wx.VERTICAL))
		printMaterialPanel.GetSizer().Add(boxsizer, flag=wx.EXPAND)
		sizer.Add(printMaterialPanel, (1,0), flag=wx.EXPAND)

		sb = wx.StaticBox(printNozzlePanel, label=_("Nozzle:"))
		boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
		for button in self._print_nozzle_options:
			boxsizer.Add(button)
		printNozzlePanel.SetSizer(wx.BoxSizer(wx.VERTICAL))
		printNozzlePanel.GetSizer().Add(boxsizer, flag=wx.EXPAND)
		sizer.Add(printNozzlePanel, (2,0), flag=wx.EXPAND)

		sb = wx.StaticBox(self, label=_("Other:"))
		boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
		boxsizer.Add(self.printSupport)
		sizer.Add(boxsizer, (3,0), flag=wx.EXPAND)

		for button in self._print_profile_options:
			button.Bind(wx.EVT_RADIOBUTTON, self._update)
		for button in self._print_material_options:
			button.Bind(wx.EVT_RADIOBUTTON, self._update)
		for button in self._print_nozzle_options:
			button.Bind(wx.EVT_RADIOBUTTON, self._update)

		self.printSupport.Bind(wx.EVT_CHECKBOX, self._update)

	def _update(self, e):
		for button in self._print_profile_options:
			if button.GetValue():
				profile.putPreference('simpleModeProfile', button.base_filename)
		for button in self._print_material_options:
			if button.GetValue():
				profile.putPreference('simpleModeMaterial', button.base_filename)
		for button in self._print_nozzle_options:
			if button.GetValue():
				profile.putPreference('simpleModeNozzle', button.nozzle_name)
		self._callback()

	def getSettingOverrides(self):
		settings = {}
		for setting in profile.settingsList:
			if not setting.isProfile():
				continue
			settings[setting.getName()] = setting.getDefault()

		nozzle = profile.getProfileSetting('nozzle_size')
		for button in self._print_nozzle_options:
			if button.GetValue():
				nozzle = button.nozzle_size
		for button in self._print_profile_options:
			if button.GetValue():
				cp = configparser.ConfigParser()
				cp.read(button.filename[nozzle])
				for setting in profile.settingsList:
					if setting.isProfile():
						if cp.has_option('profile', setting.getName()):
							settings[setting.getName()] = cp.get('profile', setting.getName())
		if profile.getMachineSetting('gcode_flavor') != 'UltiGCode':
			for button in self._print_material_options:
				if button.GetValue():
					cp = configparser.ConfigParser()
					cp.read(button.filename)
					for setting in profile.settingsList:
						if setting.isProfile():
							if cp.has_option('profile', setting.getName()):
								settings[setting.getName()] = cp.get('profile', setting.getName())

		if self.printSupport.GetValue():
			settings['support'] = "Exterior Only"
		return settings

	def updateProfileToControls(self):
		pass
