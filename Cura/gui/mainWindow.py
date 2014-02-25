__copyright__ = "Copyright (C) 2013 David Braam - Released under terms of the AGPLv3 License"

import wx
import wx.lib.buttons
import sys

from Cura.gui.util import dropTarget
from Cura.gui.util import glPanel
from Cura.gui.util.sizer import RelativePositionSizer
from Cura.util import profile
from Cura.util import version

from Cura.gui.view3D import printerView3D
from Cura.scene import printer3DScene
from Cura.machine.fdmprinter import FDMPrinter

# On windows we can place wxPanels on top of the GLPanel, but on Mac this does not work, as the GLPanel is drawn on top of it.
# On Linux the panel is placed on top, but we need to refresh the panels on top so they show after drawing the GLPanel. The Cura.gui.util.glPanel handles this.
# On Mac we place wx.Dialog on top of the GLPanel, which works. However these get separate focus which causes the title bar to grey out on windows.
if sys.platform.startswith('darwin'):
	class floatingPanel(wx.Dialog):
		def __init__(self, parent):
			super(floatingPanel, self).__init__(parent, style=wx.FRAME_FLOAT_ON_PARENT|wx.BORDER_NONE)
else:
	class floatingPanel(wx.Panel):
		def __init__(self, parent):
			super(floatingPanel, self).__init__(parent)


class mainWindow(wx.Frame):
	def __init__(self):
		super(mainWindow, self).__init__(None, title='Cura - ' + version.getVersion())

		wx.EVT_CLOSE(self, self.onClose)
		wx.EVT_MOVE(self, self.onMove)

		# allow dropping any file, restrict later
		self.SetDropTarget(dropTarget.FileDropTarget(self.OnDropFiles))

		# TODO: wxWidgets 2.9.4 has a bug when NSView does not register for dragged types when wx drop target is set. It was fixed in 2.9.5
		if sys.platform.startswith('darwin'):
			try:
				import objc
				nswindow = objc.objc_object(c_void_p=self.MacGetTopLevelWindowRef())
				view = nswindow.contentView()
				view.registerForDraggedTypes_([u'NSFilenamesPboardType'])
			except:
				pass

		#Main 3D panel
		self._gl_panel = glPanel.GLPanel(self)
		self._view_pos_panel = floatingPanel(self._gl_panel)
		self._view_pos_panel.Show()
		self._view_pos_panel.SetSize((165, 40))

		self._view_pos_panel.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
		tmp = wx.lib.buttons.GenToggleButton(self._view_pos_panel, -1, '3D', style=wx.BORDER_NONE)
		self._view_pos_panel.GetSizer().Add(tmp, 1, wx.EXPAND)
		self._view_pos_panel.GetSizer().AddSpacer(5)
		tmp = wx.lib.buttons.GenToggleButton(self._view_pos_panel, -1, 'Right', style=wx.BORDER_NONE)
		self._view_pos_panel.GetSizer().Add(tmp, 1, wx.EXPAND)
		tmp = wx.lib.buttons.GenToggleButton(self._view_pos_panel, -1, 'Front', style=wx.BORDER_NONE)
		self._view_pos_panel.GetSizer().Add(tmp, 1, wx.EXPAND)
		tmp = wx.lib.buttons.GenToggleButton(self._view_pos_panel, -1, 'Top', style=wx.BORDER_NONE)
		tmp.Bind(wx.EVT_BUTTON, self.onTest)
		self._view_pos_panel.GetSizer().Add(tmp, 1, wx.EXPAND)
		self._view_pos_panel.Layout()

		#Create a machine
		debugMachine = FDMPrinter()
		#Setup a view and scene for testing.
		self._scene = printer3DScene.Printer3DScene()
		self._view = printerView3D.PrinterView3D()
		self._view.setScene(self._scene)
		self._gl_panel.setView(self._view)
		self._view.setMachine(debugMachine)

		# Main window sizer
		sizer = RelativePositionSizer()
		self.SetSizer(sizer)
		sizer.Add(self._gl_panel, wx.EXPAND)
		sizer.Add(self._view_pos_panel, wx.BOTTOM | wx.LEFT, spacing=(20, 12))
		sizer.Layout()

		# Set default window size & position
		self.SetSize((wx.Display().GetClientArea().GetWidth()/2,wx.Display().GetClientArea().GetHeight()/2))
		self.SetMinSize((800, 600))
		self.Centre()

		# Restore the window position, size & state from the preferences file
		try:
			if profile.getPreference('window_maximized') == 'True':
				# Maximize as next event, this solves a layouting problem on windows, where the first size given to the sizer is wrong.
				wx.CallAfter(self.Maximize, True)
			else:
				posx = int(profile.getPreference('window_pos_x'))
				posy = int(profile.getPreference('window_pos_y'))
				width = int(profile.getPreference('window_width'))
				height = int(profile.getPreference('window_height'))
				if posx > 0 or posy > 0:
					self.SetPosition((posx,posy))
				if width > 0 and height > 0:
					self.SetSize((width,height))
		except:
			# Maximize as next event, this solves a layouting problem on windows, where the first size given to the sizer is wrong.
			wx.CallAfter(self.Maximize, True)

		#Check if the window is somewhere on a display, else put it at the center.
		if wx.Display.GetFromPoint(self.GetPosition()) < 0:
			self.Centre()
		if wx.Display.GetFromPoint((self.GetPositionTuple()[0] + self.GetSizeTuple()[1], self.GetPositionTuple()[1] + self.GetSizeTuple()[1])) < 0:
			self.Centre()
		if wx.Display.GetFromPoint(self.GetPosition()) < 0:
			self.SetSize((800,600))
			self.Centre()

	def OnDropFiles(self, files):
		#TODO: Files droped on window, load them.
		pass

	def onMove(self, e):
		self.Layout()

	def onClose(self, e):
		profile.saveProfile(profile.getDefaultProfilePath(), True)

		# Save the window position, size & state from the preferences file
		profile.putPreference('window_maximized', self.IsMaximized())
		if not self.IsMaximized() and not self.IsIconized():
			(posx, posy) = self.GetPosition()
			profile.putPreference('window_pos_x', posx)
			profile.putPreference('window_pos_y', posy)
			(width, height) = self.GetSize()
			profile.putPreference('window_width', width)
			profile.putPreference('window_height', height)

		print "Closing down"
		self.Destroy()

	def onTest(self, e):
		print "Test!"