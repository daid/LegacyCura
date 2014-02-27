__author__ = 'Jaime van Kessel'

from Cura.gui.tools.tool import Tool
import numpy
class MouseTool(Tool):
	def __init__(self):
		super(MouseTool,self).__init__()
		self._mouse_state = ''

	def onMouseDown(self, e):
		self._mouse_x = e.GetX()
		self._mouse_y = e.GetY()

		if e.ButtonDClick():
			self._mouse_state = 'doubleClick'
		else:
			if self._mouse_state == 'dragObject' and self._scene.getSelectedObject() is not None:
				pass
		if self._view is not None:
			p0, p1 = self._view.getMouseRay(self._mouse_x,self._mouse_y)
			p0 -= self.getObjectCenterPos() - self._view.getViewTarget()
			p1 -= self.getObjectCenterPos() - self._view.getViewTarget()


		#p0, p1 = self.getMouseRay(self._mouseX, self._mouseY)
		#p0 -= self.getObjectCenterPos() - self._viewTarget
		#p1 -= self.getObjectCenterPos() - self._viewTarget
	def onMouseUp(self, e):
		if e.LeftIsDown() or e.MiddleIsDown() or e.RightIsDown(): #Ignore events if some other buttons are still pressed
			return

	def onMouseMotion(self, e):
		p0, p1 = self._view.getMouseRay(self._mouse_x,self._mouse_y)
		if e.Dragging() and self._mouse_state is not None:
			if not e.LeftIsDown() and e.RightIsDown():
				self._mouse_state = 'drag'
				self._view.setYaw(self._view.getYaw() + e.GetX() - self._mouse_x)
				self._view.setPitch(self._view.getPitch() - (e.GetY() - self._mouse_y))

		#update mouse positions again
		self._mouse_x = e.GetX()
		self._mouse_y = e.GetY()

	def onMouseWheel(self,e):
		delta = float(e.GetWheelRotation()) / float(e.GetWheelDelta())
		delta = max(min(delta,4),-4)
		zoom = self._view.getZoom()
		zoom *= 1.0 - delta / 10.0
		self._view.setZoom(zoom)

	def getObjectCenterPos(self): #TODO: Not quite sure what function of this is, copied from old sceneView.
		selected_object = self._scene.getSelectedObject()
		if selected_object is None:
			return [0.0, 0.0, 0.0]
		pos = selected_object.getPosition()
		size = selected_object.getSize()
		return [pos[0], pos[1], size[2]/2]