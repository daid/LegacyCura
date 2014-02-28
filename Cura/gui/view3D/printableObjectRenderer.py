__author__ = 'Jaime van Kessel'
from Cura.gui.view3D.renderer import Renderer
from OpenGL.GL import *
class PrintableObjectRenderer(Renderer):
	def __int__(self):
		super(PrintableObjectRenderer,self).__init__()

	def render(self):
		super(PrintableObjectRenderer,self).render()
		#todo: add check if objects are renderable.
		self._object_shader.bind()
		for model in self._scene.getObjects():
			if model[0].isSelected():
				glColor4f(1,0.7,0,1)
			else:
				glColor4f(1,0.7,0.8,0.5)
			self._renderObject(model[0])
		self._object_shader.unbind()