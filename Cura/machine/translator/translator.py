__author__ = 'Jaime van Kessel'

class Translator(object):
	'''
	The translator class forms the interface between Cura and the engine. The translator communicates with
	a socket, which in place sends the data to the engine.
	Some machines might need to send (or recieve) different kinds of data. This is the base class, with inherited
	classes for such cases.
	'''
	def __init__(self):
		pass
