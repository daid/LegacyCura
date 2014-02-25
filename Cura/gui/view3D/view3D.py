__author__ = 'Jaime van Kessel'
from OpenGL.GL import *
from OpenGL.GLU import *
from Cura.machine.machine import Machine
from Cura.scene.scene import Scene
from Cura.gui.view3D.renderer import Renderer
from Cura.gui.view3D.machineRenderer import MachineRenderer
from Cura.gui.util.openglHelpers import *

import numpy

class View3D(object):
	'''
	view3D is a view panel that has an associated scene which are drawn by the renderers of the view.
	'''
	def __init__(self):
		self._scene = None #A view 3D has a scene responsible for data storage of what is in the 3D world.
		self._renderer_list = [] #The view holds a set of renderers, such as machine renderer or object renderer.
		self._machine = None # Reference to the machine
		self._panel = None # Reference to the wxPython OpenGL panel
		#self._zoom = numpy.array([self._machine.getSettingValueByNameFloat('machine_width'),self._machine.getSettingValueByNameFloat('machine_height'),self._machine.getSettingValueByNameFloat('machine_depth')]) * 3
		self._yaw = 10
		self._pitch = 60
		self._zoom = 600

		self._min_yaw = None
		self._max_yaw = None
		self._min_pitch = 10
		self._max_pitch = 170
		self._min_zoom = 1.0
		self._max_zoom = None
		self._object_shader = None
		machineRenderer = MachineRenderer()
		self._viewport = None
		self._model_matrix = None
		self._proj_matrix = None
		self._view_target = numpy.array([0,0,0], numpy.float32)
		self.addRenderer(machineRenderer)

	def queueRefresh(self):
		self._panel.queueRefresh()

	def setYaw(self,yaw):
		if self._min_yaw is None or self._min_yaw < yaw:
			if self._max_yaw is None or self._max_yaw > yaw:
				self._yaw = yaw
			else:
				self._yaw = self._max_yaw
		else:
			self._yaw = self._min_yaw
		self.queueRefresh()

	def getYaw(self):
		return self._yaw

	def getPitch(self):
		return self._pitch

	def setPitch(self, pitch):
		if self._min_pitch is None or self._min_pitch < pitch:
			if self._max_pitch is None or self._max_pitch > pitch:
				self._pitch = pitch
			else:
				self._pitch = self._max_pitch
		else:
			self._pitch = self._min_pitch
		self.queueRefresh()

	def getZoom(self):
		return self._zoom

	def setZoom(self, zoom):
		if self._min_zoom is None or self._min_zoom < zoom:
			if self._max_zoom is None or self._max_zoom > zoom:
				self._zoom = zoom
			else:
				self._zoom = self._max_zoom
		else:
			self._zoom = self._min_zoom
		self.queueRefresh()

	def render(self): #todo: Unsure about name.
		self._init3DView()
		self._viewport = glGetIntegerv(GL_VIEWPORT)
		self._model_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
		self._proj_matrix = glGetDoublev(GL_PROJECTION_MATRIX)

		for renderer in self._renderer_list:
			renderer.render() #call all render functions

	def addRenderer(self, renderer):
		if isinstance(renderer,Renderer):
			self._renderer_list.append(renderer);

	def setScene(self,scene):
		assert(issubclass(type(scene), Scene))
		self._scene = scene
		for render in self._renderer_list:
			render.setScene(scene)

	def getScene(self):
		return self._scene

	def getViewTarget(self):
		return self._view_target

	def setMachine(self,machine):
		if isinstance(machine,Machine):
			self._machine = machine
			self._max_zoom = numpy.max(machine.getSize()) * 3
			for renderer in self._renderer_list:
				renderer.setMachine(machine)

	def getMachine(self):
		return self._machine

	def setPanel(self, panel):
		"""
			Set the reference to the wxPython GLPanel that is used to draw this view.
		"""
		self._panel = panel

	def getMouseRay(self, x, y):
		if self._viewport is None:
			return numpy.array([0,0,0],numpy.float32), numpy.array([0,0,1],numpy.float32)
		p0 = unproject(x, self._viewport[1] + self._viewport[3] - y, 0, self._model_matrix, self._proj_matrix, self._viewport)
		p1 = unproject(x, self._viewport[1] + self._viewport[3] - y, 1, self._model_matrix, self._proj_matrix, self._viewport)
		p0 -= self._view_target
		p1 -= self._view_target
		return p0, p1

	def _init3DView(self):
		'''
		Setup the basics of the 3D view
		'''
		view_port_width = self._panel.GetSize().GetWidth()
		view_port_height = self._panel.GetSize().GetHeight()

		glViewport(0, 0, view_port_width, view_port_height)
		glLoadIdentity()

		glLightfv(GL_LIGHT0, GL_POSITION, [0.2, 0.2, 1.0, 0.0])

		glDisable(GL_RESCALE_NORMAL)
		glDisable(GL_LIGHTING)
		glDisable(GL_LIGHT0)
		glEnable(GL_DEPTH_TEST)
		glDisable(GL_CULL_FACE)
		glDisable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

		glClearColor(0.8, 0.8, 0.8, 1.0)
		glClearStencil(0)
		glClearDepth(1.0)

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		aspect = float(view_port_width) / float(view_port_height)
		machine_size = numpy.array([1000,0,0])
		if self._machine is not None:
			machine_size = numpy.array([self._machine.getSettingValueByNameFloat('machine_width'),self._machine.getSettingValueByNameFloat('machine_height'),self._machine.getSettingValueByNameFloat('machine_depth')])

		gluPerspective(45.0, aspect, 1.0, numpy.max(machine_size) * 4)

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)

		glTranslate(0,0,-self._zoom)
		glRotate(-self._pitch, 1,0,0)
		glRotate(self._yaw, 0,0,1)
		glTranslate(-self._view_target[0],-self._view_target[1],-self._view_target[2])
