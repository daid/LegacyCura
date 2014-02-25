__author__ = 'Jaime van Kessel'

from Cura.gui.tools.tool import Tool
import wx
import numpy

class KeyboardTool(Tool):
	def __init__(self):
		super(KeyboardTool,self).__init__()

	def onKeyChar(self, e):
		key_code = e.GetKeyCode()
		if key_code == wx.WXK_UP:
			if wx.GetKeyState(wx.WXK_SHIFT):
				zoom = self._view.getZoom()
				zoom /= 1.2
				if zoom < 1:
					zoom = 1
				self._view.setZoom(zoom)
			else:
				self._view.setPitch(self._view.getPitch() - 15)
			self._view.queueRefresh()
		elif key_code == wx.WXK_DOWN:
			if wx.GetKeyState(wx.WXK_SHIFT):
				zoom = self._view.getZoom()
				zoom *= 1.2
				if zoom > numpy.max(self._view.getMachine().getSize()) * 3:
					zoom = numpy.max(self._view.getMachine().getSize()) * 3
				self._view.setZoom(zoom)
			else:
				self._view.setPitch(self._view.getPitch() + 15)
		elif key_code == wx.WXK_LEFT:
			self._view.setYaw(self._view.getYaw() - 15)
		elif key_code == wx.WXK_RIGHT:
			self._view.setYaw(self._view.getYaw() + 15)
		elif key_code == wx.WXK_NUMPAD_ADD or key_code == wx.WXK_ADD or key_code == ord('+') or key_code == ord('='):
			zoom = self._view.getZoom()
			zoom /= 1.2
			if zoom < 1:
				zoom = 1
			self._view.setZoom(zoom)
		elif key_code == wx.WXK_NUMPAD_SUBTRACT or key_code == wx.WXK_SUBTRACT or key_code == ord('-'):
			zoom = self._view.getZoom()
			zoom *= 1.2
			if zoom > numpy.max(self._view.getMachine().getSize()) * 3:
				zoom = numpy.max(self._view.getMachine().getSize()) * 3
			self._view.setZoom(zoom)
		elif key_code == wx.WXK_HOME:
			self._view.setYaw(30)
			self._view.setPitch(60)
		elif key_code == wx.WXK_PAGEUP:
			self._view.setYaw(0)
			self._view.setPitch(0)
		elif key_code == wx.WXK_PAGEDOWN:
			self._view.setYaw(0)
			self._view.setPitch(90)
		elif key_code == wx.WXK_END:
			self._view.setYaw(90)
			self._view.setPitch(90)