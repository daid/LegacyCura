__author__ = 'Jaime van Kessel'

import numpy

class Mesh(object):
	"""
	A mesh is a list of 3D triangles build from vertexes. Each triangle has 3 vertexes.

	A "VBO" can be associated with this object, which is used for rendering this object.
	"""
	def __init__(self):
		self.vertexes = None
		self.vertexCount = 0
		self.vbo = None
		self._obj = None

	def setObj(self, obj):
		self._obj = obj


	def _addFace(self, x0, y0, z0, x1, y1, z1, x2, y2, z2):
		n = self.vertexCount
		self.vertexes[n][0] = x0
		self.vertexes[n][1] = y0
		self.vertexes[n][2] = z0
		n += 1
		self.vertexes[n][0] = x1
		self.vertexes[n][1] = y1
		self.vertexes[n][2] = z1
		n += 1
		self.vertexes[n][0] = x2
		self.vertexes[n][1] = y2
		self.vertexes[n][2] = z2
		self.vertexCount += 3

	def _prepareFaceCount(self, faceNumber):
		#Set the amount of faces before loading data in them. This way we can create the numpy arrays before we fill them.
		self.vertexes = numpy.zeros((faceNumber*3, 3), numpy.float32)
		self.normal = numpy.zeros((faceNumber*3, 3), numpy.float32)
		self.vertexCount = 0

	def _calculateNormals(self):
		#Calculate the normals
		tris = self.vertexes.reshape(self.vertexCount / 3, 3, 3)
		normals = numpy.cross( tris[::,1 ] - tris[::,0]  , tris[::,2 ] - tris[::,0] )
		lens = numpy.sqrt( normals[:,0]**2 + normals[:,1]**2 + normals[:,2]**2 )
		normals[:,0] /= lens
		normals[:,1] /= lens
		normals[:,2] /= lens

		n = numpy.zeros((self.vertexCount / 3, 9), numpy.float32)
		n[:,0:3] = normals
		n[:,3:6] = normals
		n[:,6:9] = normals
		self.normal = n.reshape(self.vertexCount, 3)
		self.invNormal = -self.normal

	def _vertexHash(self, idx):
		v = self.vertexes[idx]
		return int(v[0] * 100) | int(v[1] * 100) << 10 | int(v[2] * 100) << 20

	def _idxFromHash(self, map, idx):
		vHash = self._vertexHash(idx)
		for i in map[vHash]:
			if numpy.linalg.norm(self.vertexes[i] - self.vertexes[idx]) < 0.001:
				return i

	def getTransformedVertexes(self, applyOffsets = False):
		if(self._obj is not None):
			if applyOffsets:
				pos = self._obj._position.copy()
				pos.resize((3))
				pos[2] = self._obj.getSize()[2] / 2
				offset = self._obj._drawOffset.copy()
				offset[2] += self._obj.getSize()[2] / 2
				return (numpy.matrix(self.vertexes, copy = False) * numpy.matrix(self._obj._matrix, numpy.float32)).getA() - offset + pos
			return (numpy.matrix(self.vertexes, copy = False) * numpy.matrix(self._obj._matrix, numpy.float32)).getA()