__copyright__ = "Released under terms of the AGPLv3 License"


import wx
import wx.wizard


from Cura.gui  import firmwareInstall
from Cura.util import machineCom
from Cura.util import profile
from Cura.util import resources


from Cura.util import moebyusFactory


class MoebyusInfoPage(wx.wizard.WizardPageSimple):
	def __init__(self, parent, title):
		wx.wizard.WizardPageSimple.__init__(self, parent)

		sizer = wx.GridBagSizer(5, 5)
		self.sizer = sizer
		self.SetSizer(sizer)

		title = wx.StaticText(self, -1, title)
		title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
		sizer.Add(title, pos=(0, 0), span=(1, 2), flag=wx.ALIGN_CENTRE | wx.ALL)
		sizer.Add(wx.StaticLine(self, -1), pos=(1, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL)
		sizer.AddGrowableCol(1)

		self.rowNr = 2

	def AddText(self, info):
		text = wx.StaticText(self, -1, info)
		self.GetSizer().Add(text, pos=(self.rowNr, 0), span=(1, 2), flag=wx.LEFT | wx.RIGHT)
		self.rowNr += 1
		return text

	def AddSeperator(self):
		self.GetSizer().Add(wx.StaticLine(self, -1), pos=(self.rowNr, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL)
		self.rowNr += 1

	def AddHiddenSeperator(self):
		self.AddText("")

	def AddInfoBox(self):
		infoBox = InfoBox(self)
		self.GetSizer().Add(infoBox, pos=(self.rowNr, 0), span=(1, 2), flag=wx.LEFT | wx.RIGHT | wx.EXPAND)
		self.rowNr += 1
		return infoBox

	def AddRadioButton(self, label, style=0):
		radio = wx.RadioButton(self, -1, label, style=style)
		self.GetSizer().Add(radio, pos=(self.rowNr, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL)
		self.rowNr += 1
		return radio

	def AddCheckbox(self, label, checked=False):
		check = wx.CheckBox(self, -1)
		text = wx.StaticText(self, -1, label)
		check.SetValue(checked)
		self.GetSizer().Add(text, pos=(self.rowNr, 0), span=(1, 1), flag=wx.LEFT | wx.RIGHT)
		self.GetSizer().Add(check, pos=(self.rowNr, 1), span=(1, 2), flag=wx.ALL)
		self.rowNr += 1
		return check

	def AddButton(self, label):
		button = wx.Button(self, -1, label)
		self.GetSizer().Add(button, pos=(self.rowNr, 0), span=(1, 2), flag=wx.LEFT)
		self.rowNr += 1
		return button

	def AddDualButton(self, label1, label2):
		button1 = wx.Button(self, -1, label1)
		self.GetSizer().Add(button1, pos=(self.rowNr, 0), flag=wx.RIGHT)
		button2 = wx.Button(self, -1, label2)
		self.GetSizer().Add(button2, pos=(self.rowNr, 1))
		self.rowNr += 1
		return button1, button2

	def AddTextCtrl(self, value):
		ret = wx.TextCtrl(self, -1, value)
		self.GetSizer().Add(ret, pos=(self.rowNr, 0), span=(1, 2), flag=wx.LEFT)
		self.rowNr += 1
		return ret

	def AddLabelTextCtrl(self, info, value):
		text = wx.StaticText(self, -1, info)
		ret = wx.TextCtrl(self, -1, value)
		self.GetSizer().Add(text, pos=(self.rowNr, 0), span=(1, 1), flag=wx.LEFT)
		self.GetSizer().Add(ret, pos=(self.rowNr, 1), span=(1, 1), flag=wx.LEFT)
		self.rowNr += 1
		return ret

	def AddTextCtrlButton(self, value, buttonText):
		text = wx.TextCtrl(self, -1, value)
		button = wx.Button(self, -1, buttonText)
		self.GetSizer().Add(text, pos=(self.rowNr, 0), span=(1, 1), flag=wx.LEFT)
		self.GetSizer().Add(button, pos=(self.rowNr, 1), span=(1, 1), flag=wx.LEFT)
		self.rowNr += 1
		return text, button

	def AddBitmap(self, bitmap):
		bitmap = wx.StaticBitmap(self, -1, bitmap)
		self.GetSizer().Add(bitmap, pos=(self.rowNr, 0), span=(1, 2), flag=wx.LEFT | wx.RIGHT)
		self.rowNr += 1
		return bitmap

	def AddCheckmark(self, label, bitmap):
		check = wx.StaticBitmap(self, -1, bitmap)
		text = wx.StaticText(self, -1, label)
		self.GetSizer().Add(text, pos=(self.rowNr, 0), span=(1, 1), flag=wx.LEFT | wx.RIGHT)
		self.GetSizer().Add(check, pos=(self.rowNr, 1), span=(1, 1), flag=wx.ALL)
		self.rowNr += 1
		return check

	def AddCombo(self, label, options):
		combo = wx.ComboBox(self, -1, options[0], choices=options, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		text = wx.StaticText(self, -1, label)
		self.GetSizer().Add(text, pos=(self.rowNr, 0), span=(1, 1), flag=wx.LEFT | wx.RIGHT)
		self.GetSizer().Add(combo, pos=(self.rowNr, 1), span=(1, 1), flag=wx.LEFT | wx.RIGHT)
		self.rowNr += 1
		return combo

	def AllowNext(self):
		return True

	def AllowBack(self):
		return True

	def StoreData(self):
		pass


class MoebyusFactory(wx.Dialog) :
	def __init__(self,parent):
		super(MoebyusFactory, self).__init__(parent=parent, title="Moebyus Machines", size=(250, 100))

	def genProfile(machineType = "PrusaI3MM", filamentSize = '3' , nozzleSize = '0.4') :
		print("Gen profile")


class moebyusFirmwarePage(MoebyusInfoPage) :
	def __init__(self, parent) :
		super(moebyusFirmwarePage, self).__init__(parent, _("Moebyus Firmware"))
		self.options = []
		self.machines = [
						("Prusa I3\t\t\t(200x200x200)"			,"PrusaI3MM"),
						("Prusa MM - L\t\t(200x300x200)"		,"PrusaI3MM-L"),
						("Steel MM\t\t\t(200x200x200)"			,"SteelMM"),
						("Steel MM - L\t\t(300x200x200)"		,"SteelMM-L"),
						("Steel MM Marco Sirius\t(300x200x200)"	,"SteelMM-Sirius"),
						("Melta Kossel\t\t(160x300)"			,"Melta"),
						("[SIRIUS] 1.0\t\t(200x200x200)"		,"Sirius1"),
						("[SIRIUS] 1.1\t\t(200x200x200)"		,"Sirius11")]
		i = 0;
		for machine in self.machines:
			if i == 0:
				item = self.AddRadioButton(machine[0], style=wx.RB_GROUP)
				i+=1;
				item.data = machine[1:]
				self.options.append(item)
				item.Bind(wx.EVT_RADIOBUTTON, self.OnMachineSelect)
			else:
				item = self.AddRadioButton(machine[0])
				item.data = machine[1:]
				self.options.append(item)
				item.Bind(wx.EVT_RADIOBUTTON, self.OnMachineSelect)

	def OnMachineSelect(self, e):
		print("selected")
		
		
class MoebyusSelectModelPage(MoebyusInfoPage):
	def __init__(self, parent) :
		super(MoebyusSelectModelPage, self).__init__(parent, _("Moebyus Machines"))
		self._printer_info = [
			# max Size x, y, z,machine type
			("Moebyus One\t\t\t(150x150x150)"			, "MoebyusOne" 		, "mone.png" ),
			("Prusa i3 MM\t\t\t\t(200x200x200)"			, "PrusaI3MM"  		, "prusai3mm.png" ),
			("Prusa i3 MM Large\t\t(200x300x200)"		, "PrusaI3MM-L"		, "prusai3mml.png" ),
			("Steel MM\t\t\t\t\t(200x200x200)"			, "SteelMM"			, "steelmm.png" ),
			("Steel MM Large\t\t\t(300x200x200)"		, "SteelMM-L"  		, "steelmml.png" ),
			("Steel MM Marco Sirius\t(300x200x200)"		, "SteelMM-Sirius"	, "steelsirius.png" ),
			("Melta Kossel\t\t\t\t(160x300)"			, "Melta"			, "melta.png" ),
			("Melta XL\t\t\t\t\t(400x600)"				, "MeltaXL"			, "meltaxl.png" ),
			("[SIRIUS] 1.0\t\t\t\t(300x200x200)"		, "Sirius1"			, "sirius1.png" ),
			("[SIRIUS] 1.1\t\t\t\t(300x200x250)"		, "Sirius11"		, "sirius11.png" ),
			("Moebyus M3\t\t\t\t(1000x1000x1000)"		, "M3"				, "m3.png") ]
		self.parent = parent
#Seleccion de maquina
		self.AddText(_("Select Model:"))
		self._printers = []
		i = 0;
		for printer in self._printer_info:
			if i == 0:
				item = self.AddRadioButton(printer[0], style=wx.RB_GROUP)
				i+=1;
				item.data = printer[1:]
				self._printers.append(item)
				item.Bind(wx.EVT_RADIOBUTTON, self.OnMachineSelect)
			else:
				item = self.AddRadioButton(printer[0])
				item.data = printer[1:]
				self._printers.append(item)
				item.Bind(wx.EVT_RADIOBUTTON, self.OnMachineSelect)
		
		bitmap = wx.Bitmap(resources.getPathForImage('mone.png'))
		self.previewBitmap = wx.StaticBitmap(self, -1, bitmap)
		self.GetSizer().Add(self.previewBitmap, pos=(1, 3), span=(14, 2), flag=wx.LEFT | wx.RIGHT)
		self.rowNr += 1
		self.AddSeperator()

		filaments = ['1.75','3']
		self.comboFilaments = wx.ComboBox(self, -1, filaments[0], choices=filaments, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		text = wx.StaticText(self, -1, "Filament size")
		self.GetSizer().Add(text,  pos=(self.rowNr, 0), span=(1, 1), flag=wx.LEFT | wx.RIGHT)
		self.GetSizer().Add(self.comboFilaments, pos=(self.rowNr, 1), span=(1, 1), flag=wx.LEFT | wx.RIGHT)

		nozzles = ['0.2','0.3','0.35','0.4','0.5','0.6','0.8','1.0']
		self.comboNozzles = wx.ComboBox(self, -1, nozzles[3], choices=nozzles, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		text = wx.StaticText(self, -1, "Nozzle size")
		self.GetSizer().Add(text,  pos=(self.rowNr, 2), span=(1, 1), flag=wx.LEFT | wx.RIGHT)
		self.GetSizer().Add(self.comboNozzles, pos=(self.rowNr, 3), span=(1, 1), flag=wx.LEFT | wx.RIGHT)
		self.rowNr += 1

		self.AddSeperator()
		text = wx.StaticText(self, -1, 'Options')
		self.GetSizer().Add(text, pos=(self.rowNr, 0), span=(1, 1), flag=wx.ALL)		
		self.rowNr += 1
		self.checkFirmware = wx.CheckBox(self, -1)
		text = wx.StaticText(self, -1, 'Load Firmware')
		self.checkFirmware.SetValue(0)
		self.checkFirmware.Disable()
		self.GetSizer().Add(text,  pos=(self.rowNr, 0), span=(1, 1), flag=wx.LEFT | wx.RIGHT)
		self.GetSizer().Add(self.checkFirmware, pos=(self.rowNr, 1), span=(1, 1), flag=wx.ALL)

		self.checkLevel = wx.CheckBox(self, -1)
		text = wx.StaticText(self, -1, 'Level Bed')
		self.checkLevel.SetValue(0)
		self.checkLevel.Disable()
		self.GetSizer().Add(text,  pos=(self.rowNr, 2), span=(1, 1), flag=wx.LEFT | wx.RIGHT)
		self.GetSizer().Add(self.checkLevel, pos=(self.rowNr, 3), span=(1, 1), flag=wx.ALL)

		self.rowNr += 1


#Configuracion del perfil
	def StoreData(self):
		mType = "PrusaI3MM"
		for selected in self._printers:
			if selected.GetValue():
				print(selected.GetLabel())
				values = selected.data
				mType = values[0];
		moebyusFactory.genProfileForMachine(mType, self.comboFilaments.GetValue(),self.comboNozzles.GetValue())
		profile.checkAndUpdateMachineName()

	def OnMachineSelect(self, e):
		for selected in self._printers:
			if selected.GetValue():
				print(selected.GetLabel())
				values = selected.data
				self.previewBitmap.SetBitmap(wx.Bitmap(resources.getPathForImage(values[1])))
				if values[0] == 'MoebyusOne' :
					self.comboNozzles.Disable()
					self.comboFilaments.Disable()
					self.checkFirmware.Disable()
					self.comboNozzles.SetSelection(3)
					self.comboFilaments.SetSelection(0)
				elif values[0] == 'M3' :
					self.comboNozzles.Enable()
					self.comboFilaments.Disable()
					self.checkFirmware.Disable()
					self.comboNozzles.SetSelection(6)
					self.comboFilaments.SetSelection(0)
				elif values[0] == 'MeltaXL' :
					self.comboNozzles.Enable()
					self.comboFilaments.Disable()
					self.checkFirmware.Disable()
					self.comboNozzles.SetSelection(6)
					self.comboFilaments.SetSelection(0)
				elif values[0] == 'Sirius1' or  values[0] == 'Sirius11' or values[0] == 'SteelMM-Sirius' or values[0] == 'Melta' :
					self.comboNozzles.Enable()
					self.comboFilaments.Enable()
					self.checkFirmware.Enable()
					self.comboNozzles.SetSelection(3)
					self.comboFilaments.SetSelection(0)
				else :
					self.comboNozzles.Enable()
					self.comboFilaments.Enable()
					self.checkFirmware.Enable()
					self.comboNozzles.SetSelection(3)
					self.comboFilaments.SetSelection(1)					


class MoebyusDonePage(MoebyusInfoPage):
	def __init__(self, parent):
		super(MoebyusDonePage, self).__init__(parent, _("Cura is now ready!"))
		self.AddSeperator()
		self.AddText(_("Thanks for installing our software, now you're ready to print"))
		self.AddHiddenSeperator()
		self.AddHiddenSeperator()
		self.AddText(_("You can find the latest version of this software at: "))
		self.AddText(_("https://github.com/moebyus/cura/releases"))
		self.AddHiddenSeperator()		
		self.AddText(_("Also you can find and Download all the files regarding your machine at: "))
		self.AddText(_("https://github.com/moebyus"))
		self.AddHiddenSeperator()
		self.AddHiddenSeperator()
		self.AddText(_("May the Force be with you..."))				
