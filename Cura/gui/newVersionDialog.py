__copyright__ = "Copyright (C) 2013 David Braam - Released under terms of the AGPLv3 License"

import wx
from Cura.gui import firmwareInstall
from Cura.util import version
from Cura.util import profile

class newVersionDialog(wx.Dialog):
	def __init__(self):
		super(newVersionDialog, self).__init__(None, title="Welcome to the new version!")

		wx.EVT_CLOSE(self, self.OnClose)

		p = wx.Panel(self)
		self.panel = p
		s = wx.BoxSizer()
		self.SetSizer(s)
		s.Add(p, flag=wx.ALL, border=15)
		s = wx.BoxSizer(wx.VERTICAL)
		p.SetSizer(s)

		title = wx.StaticText(p, -1, 'Cura - ' + version.getVersion())
		title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
		s.Add(title, flag=wx.ALIGN_CENTRE|wx.EXPAND|wx.BOTTOM, border=5)
		s.Add(wx.StaticText(p, -1, 'Welcome to the new version of Cura.'))
		s.Add(wx.StaticText(p, -1, '(This dialog is only shown once)'))
		s.Add(wx.StaticLine(p), flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=10)
		s.Add(wx.StaticText(p, -1, 'New in version 15.04.6:'))
		s.Add(wx.StaticText(p, -1, '* Improved material profiles for PLA, ABS and CPE for the Ultimaker 2+ family.'))
		s.Add(wx.StaticText(p, -1, 'New in version 15.04.5:'))
		s.Add(wx.StaticText(p, -1, '* Fixed Ultimaker2 family build volume, which was configured too big by default.'))
		s.Add(wx.StaticText(p, -1, '* Bugfix for nozzle sizes being incorrectly copied when switching from quickprint to full settings.'))
		s.Add(wx.StaticText(p, -1, '* Bugfix for selected platform adhesion type not being remembered in quickprint mode.'))
		s.Add(wx.StaticText(p, -1, '* Bugfix for head size of the Ultimaker2+, which caused the head to bump into prints in one-at-a-time mode.'))

		self.has_machine = {}
		for n in xrange(0, profile.getMachineCount()):
			self.has_machine[profile.getMachineSetting('machine_type', n)] = n
			if profile.getMachineSetting('machine_type', n) == 'ultimaker':
				self.hasUltimaker = n
			if profile.getMachineSetting('machine_type', n) == 'ultimaker2':
				self.hasUltimaker2 = n
		if 'ultimaker' in self.has_machine and False:
			s.Add(wx.StaticLine(p), flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=10)
			s.Add(wx.StaticText(p, -1, 'New firmware for your Ultimaker Original:'))
			s.Add(wx.StaticText(p, -1, '* .'))
			button = wx.Button(p, -1, 'Install now')
			self.Bind(wx.EVT_BUTTON, lambda e: self.OnFirmwareInstall(self.has_machine['ultimaker']), button)
			s.Add(button, flag=wx.TOP, border=5)
		if 'ultimaker2' in self.has_machine and True:
			s.Add(wx.StaticLine(p), flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=10)
			s.Add(wx.StaticText(p, -1, 'New firmware for your Ultimaker 2:'))
			s.Add(wx.StaticText(p, -1, '* Updated error messages, to assist in getting better support'))
			button = wx.Button(p, -1, 'Install now')
			self.Bind(wx.EVT_BUTTON, lambda e: self.OnFirmwareInstall(self.has_machine['ultimaker2']), button)
			s.Add(button, flag=wx.TOP, border=5)
		if 'ultimaker2+' in self.has_machine and True:
			s.Add(wx.StaticLine(p), flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=10)
			s.Add(wx.StaticText(p, -1, 'New firmware for your Ultimaker 2+:'))
			s.Add(wx.StaticText(p, -1, '* Updated error messages, to assist in getting better support'))
			s.Add(wx.StaticText(p, -1, '* Bugfix for the import/export material settings which was not working properly'))
			button = wx.Button(p, -1, 'Install now')
			self.Bind(wx.EVT_BUTTON, lambda e: self.OnFirmwareInstall(self.has_machine['ultimaker2+']), button)
			s.Add(button, flag=wx.TOP, border=5)
		if 'ultimaker2+extended' in self.has_machine and True:
			s.Add(wx.StaticLine(p), flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=10)
			s.Add(wx.StaticText(p, -1, 'New firmware for your Ultimaker2+Extended:'))
			s.Add(wx.StaticText(p, -1, '* Fixed temperature stability.'))
			s.Add(wx.StaticText(p, -1, '* Fixed print starting problems when a material warning was ignored'))
			button = wx.Button(p, -1, 'Install now')
			self.Bind(wx.EVT_BUTTON, lambda e: self.OnFirmwareInstall(self.has_machine['ultimaker2+extended']), button)
			s.Add(button, flag=wx.TOP, border=5)

		s.Add(wx.StaticLine(p), flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=10)
		button = wx.Button(p, -1, 'Ok')
		self.Bind(wx.EVT_BUTTON, self.OnOk, button)
		s.Add(button, flag=wx.TOP|wx.ALIGN_RIGHT, border=5)

		self.Fit()
		self.Centre()

	def OnFirmwareInstall(self, index):
		firmwareInstall.InstallFirmware(machineIndex=index)

	def OnOk(self, e):
		self.Close()

	def OnClose(self, e):
		self.Destroy()
