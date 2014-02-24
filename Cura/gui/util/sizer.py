__copyright__ = "Copyright (C) 2013 David Braam - Released under terms of the AGPLv3 License"

import wx

class RelativeSizer(wx.PySizer):
	"""
	The RelativeSizer can position controls relative to other controls.
	This is used in the main window layout where there are multiple panels floating on the interface.
	"""
	def __init__(self):
		super(RelativeSizer, self).__init__()

	def CalcMin(self):
		width, height = 10, 10
		for item in self.GetChildren():
			pass
		return wx.Size(width, height)

	def RecalcSizes(self):
		# find the space allotted to this sizer
		pos = self.GetPosition()
		size = self.GetSize()
		for item in self.GetChildren():
			# Recalculate (if necessary) the position and size of
			# each item and then call item.SetDimension to do the
			# actual positioning and sizing of the items within the
			# space alloted to this sizer.
			#...
			#item.SetDimension(itemPos, itemSize)
			refControl, position, spacing = item.GetUserData()
			itemSize = item.GetSize()
			if refControl is None:
				x = size.GetWidth() / 2 - itemSize.GetWidth() / 2
				y = size.GetHeight() / 2 - itemSize.GetHeight() / 2
			else:
				x = refControl.GetPosition()[0] + refControl.GetSize().GetWidth() / 2 - itemSize.GetWidth() / 2
				y = refControl.GetPosition()[1] + refControl.GetSize().GetHeight() / 2 - itemSize.GetHeight() / 2
			if position == wx.EXPAND:
				#Expand over the whole area.
				x, y = 0, 0
				itemSize = size
			if position & wx.LEFT:
				if refControl is None:
					x = spacing[0]
				else:
					x = refControl.GetPosition()[0] + refControl.GetSize().GetWidth() + spacing[0]
			elif position & wx.RIGHT:
				if refControl is None:
					x = size.GetWidth() - itemSize.GetWidth() - spacing[0]
				else:
					x = refControl.GetPosition()[0] - itemSize.GetWidth() - spacing[0]
			if position & wx.TOP:
				if refControl is None:
					y = spacing
				else:
					y = refControl.GetPosition()[1] + refControl.GetSize().GetHeight() + spacing[1]
			elif position & wx.BOTTOM:
				if refControl is None:
					y = size.GetHeight() - itemSize.GetHeight() - spacing[1]
				else:
					y = refControl.GetPosition()[1] - itemSize.GetHeight() - spacing[1]
			item.SetDimension((x, y), itemSize)

	def Add(self, control, refControl = None, position = wx.CENTER, spacing = (0, 0)):
		sizerItem = super(RelativeSizer, self).Add(control)
		if type(spacing) is not tuple:
			spacing = (spacing, spacing)
		sizerItem.SetUserData((refControl, position, spacing))
