__author__ = 'Jaime van Kessel'

from Cura.gui.tools.tool import Tool

class MouseTool(Tool):
	def __init__(self):
		super(MouseTool,self).__init__()
		self._mouseX = 0
		self._mouseY = 0
		self._mouseState = ''

	def onMouseUp(self, e):
		self._mouseX = e.GetX()
		self._mouseY = e.GetY()

		if e.ButtonDClick():
			self._mouseState = 'doubleClick'
		else:
			if self._mouseState == 'dragObject' and self._scene.getSelectedObject() is not None:
				pass
		if self._view is not None:
			p0, p1 = self._view.getMouseRay(self._mouseX,self._mouseY)
			print p0
			print p1
		#p0, p1 = self.getMouseRay(self._mouseX, self._mouseY)
		#p0 -= self.getObjectCenterPos() - self._viewTarget
		#p1 -= self.getObjectCenterPos() - self._viewTarget