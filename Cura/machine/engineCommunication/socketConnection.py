__author__ = 'Jaime van Kessel'

from Cura.machine.engineCommunication.engineConnection import EngineConnection

class SocketConnection(EngineConnection):
	def __int__(self):
		super(SocketConnection,self).__init__()