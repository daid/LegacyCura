# coding=utf-8

import os
import sys
import time
import socket
import threading
import subprocess
import platform
import getpass
import re

import wx

from Cura.util import profile
from Cura.util import lpr


class LPRHandler(object):
	def __init__(self, callbackObject):
		self.callbackObject = callbackObject

		self._filename = None

		self._alive = True

		self.thread = threading.Thread(target=self._monitor)
		self.thread.daemon = True
		self.thread.start()

	def _monitor(self):
		host = profile.getPreference("lpr_host")
		queue = profile.getPreference("lpr_queue")
		user = getpass.getuser()

		start = " Status: LP filter msg - '"
		status = "Connecting"

		while self._alive:
			try:
				lp = lpr.LPR(host, user=user)
				lp.connect()

				if self._filename is not None:
					stream = open(self._filename, "r")

					lp.send_stream(queue, user, stream,
						os.path.basename(self._filename))

					self._filename = None

				if self._alive:
					self.callbackObject.mcConnected(True)

				lines = lp.command_send_queue_state_long(queue).split("\n")

				for line in lines:
					if line.startswith(start):
						status = line[len(start):-17]

				if self._alive:
					self.callbackObject.mcMessage(status)

				lp.close()

			except (socket.herror, socket.gaierror):
				if self._alive:
					self.callbackObject.mcConnected(False)
					self.callbackObject.mcMessage("unknown host")
			except (socket.error, socket.timeout, lpr.LPRError):
				if self._alive:
					self.callbackObject.mcConnected(False)
					self.callbackObject.mcMessage("connection error")

			for i in range(100):
				if self._alive and self._filename is None:
					time.sleep(0.1)

	def printGCode(self, filename):
		self._filename = filename

	def close(self):
		self._alive = False


def printFile(filename):
	printWindowHandle = printWindow(filename)
	printWindowHandle.Show(True)
	printWindowHandle.Raise()


class printWindow(wx.Frame):
	"Main user interface window"

	def __init__(self, filename):
		super(printWindow, self).__init__(None, -1, title='Printing')
		self.filename = filename
		self.connected = False
		self.server_status = ""

		self.SetSizer(wx.BoxSizer())
		self.panel = wx.Panel(self)
		self.GetSizer().Add(self.panel, 1, flag=wx.EXPAND)
		self.sizer = wx.GridBagSizer(2, 2)
		self.panel.SetSizer(self.sizer)

		sb = wx.StaticBox(self.panel, label="Status")
		boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)

		self.statsText = wx.StaticText(self.panel, -1,
			"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\n\n")
		boxsizer.Add(self.statsText, flag=wx.LEFT, border=5)

		self.sizer.Add(boxsizer, pos=(0, 0), span=(7, 6), flag=wx.EXPAND)

		self.printButton = wx.Button(self.panel, -1, 'Print')
		#self.cancelButton = wx.Button(self.panel, -1, 'Cancel print')
		self.progress = wx.Gauge(self.panel, -1)
		self.progress.SetRange(100)

		self.sizer.Add(self.printButton, pos=(1, 6), flag=wx.EXPAND)
		#self.sizer.Add(self.cancelButton, pos=(2, 6), flag=wx.EXPAND)
		self.sizer.Add(self.progress, pos=(7, 0), span=(1, 7), flag=wx.EXPAND)

		self.sizer.AddGrowableRow(6)
		self.sizer.AddGrowableCol(3)

		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.printButton.Bind(wx.EVT_BUTTON, self.OnPrint)
		#self.cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)

		self.Layout()
		self.Fit()
		self.Centre()

		self.statsText.SetMinSize(self.statsText.GetSize())

		self.UpdateButtonStates()
		self.UpdateProgress()

		self.SetTitle('Printing: %s' % (filename))

		self.lprCom = LPRHandler(self)

	def UpdateButtonStates(self):
		self.printButton.Enable(self.connected)

	def UpdateProgress(self):
		status = ""
		if self.filename is None:
			status += "Connecting\n"
		else:
			status += "Server status: %s\n" % self.server_status

		self.statsText.SetLabel(status.strip())

	def OnPrint(self, e):
		self.printButton.Enable(False)
		self.lprCom.printGCode(self.filename)

	def OnCancel(self, e):
		pass

	def OnClose(self, e):
                self.lprCom.close()
		self.Destroy()

	def mcMessage(self, message):
		self.server_status = message
		wx.CallAfter(self.UpdateProgress)

	def mcConnected(self, connected):
		self.connected = connected
		wx.CallAfter(self.UpdateButtonStates)
