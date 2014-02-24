__author__ = 'Jaime van Kessel'
from OpenGL.GL import *
from Cura.gui.util import previewTools
from Cura.gui.util import openglHelpers
from Cura.util import meshLoader

from Cura.scene.scene import Scene
from Cura.machine.machine import Machine

class Renderer(object):
	'''
	Abstract renderer class
	'''
	def __init__(self):
		self._machine = None #Reference to machine
		self._scene = None #Reference to the scene

	def render(self):
		pass

	def setScene(self,scene):
		assert(issubclass(type(scene), Scene))
		self._scene = scene

	def _renderObject(self, obj):
		glPushMatrix()

		glTranslate(obj.getPosition()[0], obj.getPosition()[1], obj.getSize()[2] / 2)

		#if self.tempMatrix is not None and obj == self._selectedObj:
		#	glMultMatrixf(openglHelpers.convert3x3MatrixTo4x4(self.tempMatrix))

		#offset = obj.getDrawOffset()
		#glTranslate(-offset[0], -offset[1], -offset[2] - obj.getSize()[2] / 2)

		glMultMatrixf(openglHelpers.convert3x3MatrixTo4x4(obj.getMatrix()))

		n = 0
		for m in obj._meshList:

			if m.vbo is None:
				m.vbo = openglHelpers.GLVBO(GL_TRIANGLES, m.vertexes, m.normal)
			#if brightness != 0:
			#	glColor4fv(map(lambda idx: idx * brightness, self._objColors[n]))
			#	n += 1
			m.vbo.render()
		glPopMatrix()

	def setMachine(self,machine):
		if isinstance(machine,Machine):
			self._machine = machine