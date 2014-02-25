"""
The meshLoader module contains a universal interface for loading 3D files.
Depending on the file extension the proper meshLoader is called to load the file.
"""
__copyright__ = "Copyright (C) 2013 David Braam - Released under terms of the AGPLv3 License"

import os

from Cura.util.meshLoaders import stl
from Cura.util.meshLoaders import obj
from Cura.util.meshLoaders import dae
from Cura.util.meshLoaders import amf

def loadSupportedExtensions():
	""" return a list of supported file extensions for loading. """
	return ['.stl', '.obj', '.dae', '.amf']

def saveSupportedExtensions():
	""" return a list of supported file extensions for saving. """
	return ['.amf', '.stl']

def loadPrintableObject(filename):
	"""
	loadPrintableObject loads 1 or more printableObjects from a file.
	STL files are a single printableObject with a single mesh, these are most common.
	OBJ files usually contain a single mesh, but they can contain multiple meshes
	AMF can contain whole scenes of objects with each object having multiple meshes.
	DAE files are a mess, but they can contain scenes of objects as well as grouped meshes
	"""
	ext = os.path.splitext(filename)[1].lower()
	if ext == '.stl':
		return stl.loadScene(filename)
	if ext == '.obj':
		return obj.loadScene(filename)
	if ext == '.dae':
		return dae.loadScene(filename)
	if ext == '.amf':
		return amf.loadScene(filename)
	print 'Error: Unknown model extension: %s' % (ext)
	return []

def loadMesh(filename):
	'''
	Loads mesh from file. Only the first found mesh is returned.
	'''
	ext = os.path.splitext(filename)[1].lower()
	if ext == '.stl':
		return stl.loadMesh(filename)
	if ext == '.obj':
		return obj.loadMesh(filename)
	if ext == '.dae':
		return dae.loadMesh(filename)
	if ext == '.amf':
		return amf.loadMesh(filename)
	print 'Error: Unknown model extension: %s' % (ext)
	return []

def saveMeshes(filename, objects):
	"""
	Save a list of objects into the file given by the filename. Use the filename extension to find out the file format.
	"""
	ext = os.path.splitext(filename)[1].lower()
	if ext == '.stl':
		stl.saveScene(filename, objects)
		return
	if ext == '.amf':
		amf.saveScene(filename, objects)
		return
	print 'Error: Unknown model extension: %s' % (ext)
