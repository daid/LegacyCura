__author__ = 'Jaime van Kessel'


from Cura.gui.view3D.renderer import Renderer
from OpenGL.GL import *
from Cura.util import meshLoader

class MachineRenderer(Renderer):
	'''
	Renderer responsible for rendering the 3D model of the machine
	'''
	def __init__(self):
		super(MachineRenderer,self).__init__()
		self._machine_width = 0;
		self._machine_height = 0;
		self._machine_depth = 0;
		self._mesh_path = ''
		self._platform_mesh = None

	def render(self):
		super(MachineRenderer,self).render()
		if self._machine is not None:
			#Draw machine
			glEnable(GL_CULL_FACE)
			glEnable(GL_BLEND)
			size = [self._machine_width,self._machine_depth,self._machine_height]
			if(self._platform_mesh is None):
				self._platform_mesh = meshLoader.loadMeshes(self._mesh_path)
			glColor4f(1,1,1,0.5)
			self._renderObject(self._platformMesh)

			#Draw sides
			glDepthMask(False)


