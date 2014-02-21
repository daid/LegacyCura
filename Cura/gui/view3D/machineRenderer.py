__author__ = 'Jaime van Kessel'


from Cura.gui.view3D.renderer import Renderer

class MachineRenderer(Renderer):
	'''
	Renderer responsible for rendering the 3D model of the machine
	'''
	def __init__(self):
		super(MachineRenderer,self).__init__()

	def render(self):
		super(MachineRenderer,self).render()
