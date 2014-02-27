__author__ = 'Jaime van Kessel'
from Cura.gui.view3D.view3D import View3D
from Cura.gui.view3D.machineRenderer import MachineRenderer
from Cura.gui.view3D.printableObjectRenderer import PrintableObjectRenderer

class PrinterView3D(View3D):
	def __init__(self):
		super(PrinterView3D,self).__init__()

		#machine_renderer = MachineRenderer()
		#machine_renderer.setMachine(self._machine)
		#self.addRenderer(machine_renderer)
		printable_object_renderer = PrintableObjectRenderer()
		printable_object_renderer.setScene(self._scene)
		self.addRenderer(printable_object_renderer,True)


