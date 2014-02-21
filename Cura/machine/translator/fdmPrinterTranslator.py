__author__ = 'Jaime van Kessel'

from Cura.machine.translator.printer3DTranslator import Printer3DTranslator

class FDMPrinterTranslator(Printer3DTranslator):
	def __init__(self):
		super(FDMPrinterTranslator,self).__init__()