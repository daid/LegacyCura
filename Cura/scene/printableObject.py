__author__ = 'Jaime van Kessel'

from Cura.scene.displayableObject import DisplayableObject
import time
import math
import os
from Cura.util.mesh import Mesh

import numpy
numpy.seterr(all='ignore')

from Cura.util import polygon

class PrintableObject(DisplayableObject):
	"""
	A printable object is an object that can be printed and is on the build platform.
	It contains 1 or more Meshes. Where more meshes are used for multi-extrusion.

	Each object has a 3x3 transformation matrix to rotate/scale the object.
	This object also keeps track of the 2D boundary polygon used for object collision in the objectScene class.
	"""
	def __init__(self, originFilename):
		super(PrintableObject,self).__init__()
		self._originFilename = originFilename
		if originFilename is None:
			self._name = 'None'
		else:
			self._name = os.path.basename(originFilename)
		if '.' in self._name:
			self._name = os.path.splitext(self._name)[0]
		self._mesh_list = []

		self._boundaryCircleSize = None
		self._drawOffset = None
		self._boundaryHull = None
		self._print_area_extend = numpy.array([[-1,-1],[ 1,-1],[ 1, 1],[-1, 1]], numpy.float32)
		self._head_area_extend = numpy.array([[-1,-1],[ 1,-1],[ 1, 1],[-1, 1]], numpy.float32)
		self._head_min_size = numpy.array([1, 1], numpy.float32)
		self._print_area_hull = None
		self._head_area_hull = None
		self._head_area_min_hull = None

		self._loadAnim = None

	def copy(self):
		ret = PrintableObject(self._originFilename)
		ret._matrix = self._matrix.copy()
		ret._transformedMin = self._transformedMin.copy()
		ret._transformedMax = self._transformedMax.copy()
		ret._transformedSize = self._transformedSize.copy()
		ret._boundaryCircleSize = self._boundaryCircleSize
		ret._boundaryHull = self._boundaryHull.copy()
		ret._printAreaExtend = self._printAreaExtend.copy()
		ret._printAreaHull = self._printAreaHull.copy()
		ret._drawOffset = self._drawOffset.copy()
		for m in self._meshList[:]:
			m2 = ret._addMesh()
			m2.vertexes = m.vertexes
			m2.vertexCount = m.vertexCount
			m2.vbo = m.vbo
			m2.vbo.incRef()
		return ret

	def _addMesh(self):
		m = Mesh()
		m.setObj(self)
		self._mesh_list.append(m)
		return m

	def _postProcessAfterLoad(self):
		for m in self._mesh_list:
			m._calculateNormals()
		self.processMatrix()
		#check if size is in a sensible range
		if numpy.max(self.getSize()) > 10000.0:
			for m in self._mesh_list:
				m.vertexes /= 1000.0
			self.processMatrix()
		if numpy.max(self.getSize()) < 1.0:
			for m in self._mesh_list:
				m.vertexes *= 1000.0
			self.processMatrix()

	def applyMatrix(self, m):
		self._matrix *= m
		self.processMatrix()

	def layFlat(self):
		transformed_vertexes = self._mesh_list[0].getTransformedVertexes()
		minZvertex = transformed_vertexes[transformed_vertexes.argmin(0)[2]]
		dotMin = 1.0
		dotV = None
		for v in transformed_vertexes:
			diff = v - minZvertex
			len = math.sqrt(diff[0] * diff[0] + diff[1] * diff[1] + diff[2] * diff[2])
			if len < 5:
				continue
			dot = (diff[2] / len)
			if dotMin > dot:
				dotMin = dot
				dotV = diff
		if dotV is None:
			return
		rad = -math.atan2(dotV[1], dotV[0])
		self._matrix *= numpy.matrix([[math.cos(rad), math.sin(rad), 0], [-math.sin(rad), math.cos(rad), 0], [0,0,1]], numpy.float64)
		rad = -math.asin(dotMin)
		self._matrix *= numpy.matrix([[math.cos(rad), 0, math.sin(rad)], [0,1,0], [-math.sin(rad), 0, math.cos(rad)]], numpy.float64)


		transformed_vertexes = self._meshList[0].getTransformedVertexes()
		min_z_vertex = transformed_vertexes[transformed_vertexes.argmin(0)[2]]
		dotMin = 1.0
		dotV = None
		for v in transformed_vertexes:
			diff = v - min_z_vertex
			len = math.sqrt(diff[1] * diff[1] + diff[2] * diff[2])
			if len < 5:
				continue
			dot = (diff[2] / len)
			if dotMin > dot:
				dotMin = dot
				dotV = diff
		if dotV is None:
			return
		if dotV[1] < 0:
			rad = math.asin(dotMin)
		else:
			rad = -math.asin(dotMin)
		self.applyMatrix(numpy.matrix([[1,0,0], [0, math.cos(rad), math.sin(rad)], [0, -math.sin(rad), math.cos(rad)]], numpy.float64))

	def processMatrix(self):
		self._transformed_min = numpy.array([999999999999,999999999999,999999999999], numpy.float64)
		self._transformed_max = numpy.array([-999999999999,-999999999999,-999999999999], numpy.float64)
		self._boundary_circle_size = 0

		hull = numpy.zeros((0, 2), numpy.int)
		for m in self._mesh_list:
			transformed_vertexes = m.getTransformedVertexes()
			hull = polygon.convexHull(numpy.concatenate((numpy.rint(transformed_vertexes[:,0:2]).astype(int), hull), 0))
			transformed_min = transformed_vertexes.min(0)
			transformed_max = transformed_vertexes.max(0)
			for n in xrange(0, 3):
				self._transformed_min[n] = min(transformed_min[n], self._transformed_min[n])
				self._transformed_max[n] = max(transformed_max[n], self._transformed_max[n])

			#Calculate the boundary circle
			transformed_size = transformed_max - transformed_min
			center = transformed_min + transformed_size / 2.0
			boundary_circle_size = round(math.sqrt(numpy.max(((transformed_vertexes[::,0] - center[0]) * (transformed_vertexes[::,0] - center[0])) + ((transformed_vertexes[::,1] - center[1]) * (transformed_vertexes[::,1] - center[1])) + ((transformed_vertexes[::,2] - center[2]) * (transformed_vertexes[::,2] - center[2])))), 3)
			self._boundary_circle_size = max(self._boundaryCircleSize, boundary_circle_size)
		self._transformed_size = self._transformed_max - self._transformed_min
		self._draw_offset = (self._transformed_max + self._transformed_min) / 2
		self._draw_offset[2] = self._transformed_min[2]
		self._transformed_max -= self._draw_offset
		self._transformed_min -= self._draw_offset

		self._boundary_hull = polygon.minkowskiHull((hull.astype(numpy.float32) - self._draw_offset[0:2]), numpy.array([[-1,-1],[-1,1],[1,1],[1,-1]],numpy.float32))
		self._print_area_hull = polygon.minkowskiHull(self._boundary_hull, self._print_area_extend)
		self.setHeadArea(self._head_area_extend, self._head_min_size)

	def setPrintAreaExtends(self, poly):
		self._print_area_extend = poly
		self._print_area_hull = polygon.minkowskiHull(self._boundary_hull, self._print_area_extend)

		self.setHeadArea(self._head_area_extend, self._head_min_size)

	def setHeadArea(self, poly, min_size):
		self._head_area_extend = poly
		self._head_min_size = min_size
		self._head_area_hull = polygon.minkowskiHull(self._print_area_hull, self._head_area_extend)
		pMin = numpy.min(self._print_area_hull, 0) - self._head_min_size
		pMax = numpy.max(self._print_area_hull, 0) + self._head_min_size
		square = numpy.array([pMin, [pMin[0], pMax[1]], pMax, [pMax[0], pMin[1]]], numpy.float32)
		self._head_area_min_hull = polygon.clipConvex(self._head_area_hull, square)

	def mirror(self, axis):
		matrix = [[1,0,0], [0, 1, 0], [0, 0, 1]]
		matrix[axis][axis] = -1
		self.applyMatrix(numpy.matrix(matrix, numpy.float64))

	#Split splits an object with multiple meshes into different objects, where each object is a part of the original mesh that has
	# connected faces. This is useful to split up plate STL files.
	def split(self, callback):
		ret = []
		for oriMesh in self._mesh_list:
			ret += oriMesh.split(callback)
		return ret

	def canStoreAsSTL(self):
		return len(self._mesh_list) < 2

	#getVertexIndexList returns an array of vertexes, and an integer array for each mesh in this object.
	# the integer arrays are indexes into the vertex array for each triangle in the model.
	def getVertexIndexList(self):
		vertexMap = {}
		vertexList = []
		meshList = []
		for m in self._mesh_list:
			verts = m.getTransformedVertexes(True)
			meshIdxList = []
			for idx in xrange(0, len(verts)):
				v = verts[idx]
				hashNr = int(v[0] * 100) | int(v[1] * 100) << 10 | int(v[2] * 100) << 20
				vIdx = None
				if hashNr in vertexMap:
					for idx2 in vertexMap[hashNr]:
						if numpy.linalg.norm(v - vertexList[idx2]) < 0.001:
							vIdx = idx2
				if vIdx is None:
					vIdx = len(vertexList)
					vertexMap[hashNr] = [vIdx]
					vertexList.append(v)
				meshIdxList.append(vIdx)
			meshList.append(numpy.array(meshIdxList, numpy.int32))
		return numpy.array(vertexList, numpy.float32), meshList