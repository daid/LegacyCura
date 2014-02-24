__author__ = 'Jaime van Kessel'

class EngineConnection(object):
	'''
	Interface for connection with engine. This is the lowest level of communication.
	The connection classes only handle the sending of data.
	The translator class handle the conversion from models to send-able data.
	'''
	def __int__(self):
		pass

	def connectWithEngine(self):
		pass
