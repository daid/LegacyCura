__copyright__ = "Copyright (C) 2013 David Braam - Released under terms of the AGPLv3 License"

import wx

class RelativePositionSizer(wx.PySizer):
	"""
	The RelativeSizer can position controls relative to other controls.
	This is used in the main window layout where there are multiple panels floating on the interface.
	"""
	def __init__(self):
		super(RelativePositionSizer, self).__init__()

	def CalcMin(self):
		width, height = 10, 10
		for item in self.GetChildren():
			pass
		return wx.Size(width, height)

	def RecalcSizes(self):
		# find the space allotted to this sizer
		pos = self.GetPosition()
		size = self.GetSize()
		windowScreenPosition = self.GetContainingWindow().ClientToScreenXY(0, 0)
		for item in self.GetChildren():
			position, refControl, refPosition, spacing = item.GetUserData()
			itemSize = item.GetSize()

			if position == wx.EXPAND:
				#Expand over the whole area.
				x, y = 0, 0
				itemSize = size
			else:
				if refControl is None:
					#Set the position relative to the container
					x = size.GetWidth() / 2 - itemSize.GetWidth() / 2
					y = size.GetHeight() / 2 - itemSize.GetHeight() / 2
					if refPosition & wx.LEFT:
						x = 0
					elif refPosition & wx.RIGHT:
						x = size.GetWidth()
					if refPosition & wx.TOP:
						y = 0
					elif refPosition & wx.BOTTOM:
						y = size.GetHeight()
				else:
					#Set the position relative to another control
					x = refControl.GetPosition()[0] + refControl.GetSize().GetWidth() / 2
					y = refControl.GetPosition()[1] + refControl.GetSize().GetHeight() / 2

					if refPosition & wx.LEFT:
						x = refControl.GetPosition()[0]
					elif refPosition & wx.RIGHT:
						x = refControl.GetPosition()[0] + refControl.GetSize().GetWidth()
					if refPosition & wx.TOP:
						y = refControl.GetPosition()[1]
					elif refPosition & wx.BOTTOM:
						y = refControl.GetPosition()[1] + refControl.GetSize().GetHeight()

				if position & wx.LEFT:
					x += spacing[0]
				elif position & wx.RIGHT:
					x += -itemSize.GetWidth() - spacing[0]
				if position & wx.TOP:
					y += spacing[1]
				elif position & wx.BOTTOM:
					y += -itemSize.GetHeight() - spacing[1]

			if isinstance(item.GetWindow(), wx.Dialog) or isinstance(item.GetWindow(), wx.Frame) or isinstance(item.GetWindow(), wx.PopupWindow):
				if not isinstance(item.GetWindow(), wx.MDIChildFrame):
					x += windowScreenPosition[0]
					y += windowScreenPosition[1]
			item.SetDimension((x, y), itemSize)

	def Add(self, control, position = 0, refControl = None, refPosition = 0, spacing = (0, 0)):
		sizerItem = super(RelativePositionSizer, self).Add(control)
		if type(spacing) is not tuple:
			spacing = (spacing, spacing)
		if refControl is None and refPosition == 0:
			refPosition = position
		sizerItem.SetUserData((position, refControl, refPosition, spacing))
