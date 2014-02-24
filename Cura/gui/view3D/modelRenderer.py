__author__ = 'Jaime van Kessel'
from Cura.gui.view3D.renderer import Renderer

class ModelRenderer(Renderer):
	def __int__(self):
		super(ModelRenderer,self).__init__()
		self._model_list = []

	def addModel(self, model):
		self._model_list.append(model)

	def render(self):
		for model in self._model_list:
			self._renderObject(model)