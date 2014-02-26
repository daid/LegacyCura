__author__ = 'Jaime van Kessel'
import math
import numpy

class DisplayableObject(object):
	#Base class for any object (save platform) in the scene.

	def __init__(self):
		self._position = numpy.array([0.0, 0.0])
		self._matrix = numpy.matrix([[1,0,0],[0,1,0],[0,0,1]], numpy.float64)
		self._transformed_min = None
		self._transformed_max = None
		self._transformed_size = None
		self._origin_filename = None
		self._boundary_circle_size = None
		self._name = None
		self._draw_offset = None


	def getName(self):
		return self._name
	def getOriginFilename(self):
		return self._origin_filename
	def getPosition(self):
		return self._position
	def setPosition(self, new_pos):
		self._position = new_pos
	def getMatrix(self):
		return self._matrix
	def getMaximum(self):
		return self._transformed_max
	def getMinimum(self):
		return self._transformed_min
	def getSize(self):
		return self._transformed_size
	def getDrawOffset(self):
		return self._draw_offset
	def getBoundaryCircle(self):
		return self._boundary_circle_size

	def getScale(self):
		return numpy.array([
			numpy.linalg.norm(self._matrix[::,0].getA().flatten()),
			numpy.linalg.norm(self._matrix[::,1].getA().flatten()),
			numpy.linalg.norm(self._matrix[::,2].getA().flatten())], numpy.float64)

	def setScale(self, scale, axis, uniform):
		currentScale = numpy.linalg.norm(self._matrix[::,axis].getA().flatten())
		scale /= currentScale
		if scale == 0:
			return
		if uniform:
			matrix = [[scale,0,0], [0, scale, 0], [0, 0, scale]]
		else:
			matrix = [[1.0,0,0], [0, 1.0, 0], [0, 0, 1.0]]
			matrix[axis][axis] = scale
		self.applyMatrix(numpy.matrix(matrix, numpy.float64))

	def setSize(self, size, axis, uniform):
		scale = self.getSize()[axis]
		scale = size / scale
		if scale == 0:
			return
		if uniform:
			matrix = [[scale,0,0], [0, scale, 0], [0, 0, scale]]
		else:
			matrix = [[1,0,0], [0, 1, 0], [0, 0, 1]]
			matrix[axis][axis] = scale
		self.applyMatrix(numpy.matrix(matrix, numpy.float64))

	def resetScale(self):
		x = 1/numpy.linalg.norm(self._matrix[::,0].getA().flatten())
		y = 1/numpy.linalg.norm(self._matrix[::,1].getA().flatten())
		z = 1/numpy.linalg.norm(self._matrix[::,2].getA().flatten())
		self.applyMatrix(numpy.matrix([[x,0,0],[0,y,0],[0,0,z]], numpy.float64))

	def resetRotation(self):
		x = numpy.linalg.norm(self._matrix[::,0].getA().flatten())
		y = numpy.linalg.norm(self._matrix[::,1].getA().flatten())
		z = numpy.linalg.norm(self._matrix[::,2].getA().flatten())
		self._matrix = numpy.matrix([[x,0,0],[0,y,0],[0,0,z]], numpy.float64)
		self.processMatrix()

	def scaleUpTo(self, size):
		vMin = self._transformed_min
		vMax = self._transformed_max

		scaleX1 = (size[0] / 2 - self._position[0]) / ((vMax[0] - vMin[0]) / 2)
		scaleY1 = (size[1] / 2 - self._position[1]) / ((vMax[1] - vMin[1]) / 2)
		scaleX2 = (self._position[0] + size[0] / 2) / ((vMax[0] - vMin[0]) / 2)
		scaleY2 = (self._position[1] + size[1] / 2) / ((vMax[1] - vMin[1]) / 2)
		scaleZ = size[2] / (vMax[2] - vMin[2])
		scale = min(scaleX1, scaleY1, scaleX2, scaleY2, scaleZ)
		if scale > 0:
			self.applyMatrix(numpy.matrix([[scale,0,0],[0,scale,0],[0,0,scale]], numpy.float64))