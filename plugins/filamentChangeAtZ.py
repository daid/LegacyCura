#Name: Change filament
#Info: Pause the printer at a certain height and beging filament change procedure.
#Depend: GCode
#Type: postprocess
#Param: pauseLevel(float:5.0) Pause height (mm)
#Param: parkX(float:190) Head park X (mm)
#Param: parkY(float:190) Head park Y (mm)
#Param: parkZ(float:190) Head park Z (mm)
#Param: retractAmount(float:5) Retraction amount (mm)
#Param: retractAmountPost(float:5) Retraction amount After change (mm)

__copyright__ = "Copyright (C) 2013 David Braam , Alejandro Medrano - Released under terms of the AGPLv3 License"
import re

def getValue(line, key, default = None):
	if not key in line or (';' in line and line.find(key) > line.find(';')):
		return default
	subPart = line[line.find(key) + 1:]
	m = re.search('^[0-9]+\.?[0-9]*', subPart)
	if m is None:
		return default
	try:
		return float(m.group(0))
	except:
		return default

with open(filename, "r") as f:
	lines = f.readlines()

z = 0.
x = 0.
y = 0.
pauseState = 0
currentSectionType = 'STARTOFFILE'
with open(filename, "w") as f:
	for line in lines:
		if line.startswith(';'):
			if line.startswith(';TYPE:'):
				currentSectionType = line[6:].strip()
			f.write(line)
			continue
		if getValue(line, 'G', None) == 1 or getValue(line, 'G', None) == 0:
			newZ = getValue(line, 'Z', z)
			x = getValue(line, 'X', x)
			y = getValue(line, 'Y', y)
			if newZ != z and currentSectionType != 'CUSTOM':
				z = newZ
				if z < pauseLevel and pauseState == 0:
					pauseState = 1
				if z >= pauseLevel and pauseState == 1:
					pauseState = 2
					f.write(";TYPE:CUSTOM\n")
					#SEND M600 - Pause for filament change X[pos] Y[pos] Z[relative lift] E[initial retract] L[later retract distance for removal]
					f.write("M600 X%f Y%f Z%f E%f L%f\n" % (parkX, parkY, parkZ, retractAmount, retractAmountPost))
		f.write(line)
