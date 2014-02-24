__author__ = 'Jaime van Kessel'
from Cura.gui.view3D.renderer import Renderer

class ModelRenderer(Renderer):
	def __int__(self):
		super(ModelRenderer,self).__init__()

	def render(self):
		#todo: add check if objects are renderable.
		for model in self._scene.getModels():
			self._renderObjects(model)