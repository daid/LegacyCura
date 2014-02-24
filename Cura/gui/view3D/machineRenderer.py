__author__ = 'Jaime van Kessel'


from Cura.gui.view3D.renderer import Renderer
from OpenGL.GL import *
from Cura.util import meshLoader
from Cura.gui.util import openglHelpers
from Cura.util import resources

class MachineRenderer(Renderer):
	'''
	Renderer responsible for rendering the 3D model of the machine
	'''
	def __init__(self):
		super(MachineRenderer,self).__init__()
		self._machine_width = 0;
		self._machine_height = 0;
		self._machine_depth = 0;
		self._mesh_path = resources.getPathForMesh('ultimaker_platform.stl') #Todo; hardcoded now.
		self._platform_mesh = None
		self._platform_texture = None

	def render(self):
		super(MachineRenderer,self).render()
		if self._machine is not None:
			#Draw machine
			glEnable(GL_CULL_FACE)
			glEnable(GL_BLEND)
			#size = [self._machine_width,self._machine_depth,self._machine_height]
			if(self._platform_mesh is None):
				self._platform_mesh = meshLoader.loadMeshes(self._mesh_path)
			glColor4f(1,1,0,0.5)
			self._object_shader.bind()
			self._renderObject(self._platform_mesh[0])
			self._object_shader.unbind()
			#Draw sides
			glDepthMask(False)
			polys = self._machine.getShape()
			height = self._machine.getSettingValueByName('machine_height')
			glBegin(GL_QUADS)
			for n in xrange(0, len(polys)):

				if n % 2 == 0:
					glColor4ub(5, 171, 231, 96)
				else:
					glColor4ub(5, 171, 231, 64)

				glVertex3f(polys[n][0], polys[n][1], height)
				glVertex3f(polys[n][0], polys[n][1], 0)
				glVertex3f(polys[n-1][0], polys[n-1][1], 0)
				glVertex3f(polys[n-1][0], polys[n-1][1], height)
			glEnd()

			#Draw top of build volume.
			glColor4ub(5, 171, 231, 128)
			glBegin(GL_TRIANGLE_FAN)
			for p in polys[::-1]:
				glVertex3f(p[0], p[1], height)
			glEnd()
			#Draw checkerboard

			if self._platform_texture is None:
				self._platform_texture = openglHelpers.loadGLTexture('checkerboard.png')
				glBindTexture(GL_TEXTURE_2D, self._platform_texture)
				glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
				glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
			glColor4f(1,1,1,0.5)
			glBindTexture(GL_TEXTURE_2D, self._platform_texture)
			glEnable(GL_TEXTURE_2D)
			glBegin(GL_TRIANGLE_FAN)
			for p in polys:
				glTexCoord2f(p[0]/20, p[1]/20)
				glVertex3f(p[0], p[1], 0)
			glEnd()

			#Draw no-go zones (if any)
			glDisable(GL_TEXTURE_2D)
			glColor4ub(127, 127, 127, 200)
			polys = self._machine.getDisallowedZones()
			for poly in polys:
				glBegin(GL_TRIANGLE_FAN)
				for p in poly:
					glTexCoord2f(p[0]/20, p[1]/20)
					glVertex3f(p[0], p[1], 0)
				glEnd()
			glDepthMask(True)
			glDisable(GL_BLEND)
			glDisable(GL_CULL_FACE)
