#Name: X/Y/Z Shift
#Info: Shift print operations linearly in X, Y, and/or Z
#Depend: GCode
#Type: postprocess
#Param: xshift(float:0.0) X shift (mm)
#Param: yshift(float:0.0) Y shift (mm)
#Param: zshift(float:0.0) Z shift (mm)

import re

shift = {'X': xshift, 'Y': yshift, 'Z': zshift}
def shiftIt(m):
  axis = m.group(1)
	try:
		return m.group(1) + str(float(m.group(2)) + shift[m.group(1)])
	except:
		return m.group(0)

with open(filename, "r") as f:
	lines = f.readlines()

absolute_pos = True

with open(filename, "w") as f:
	for line in lines:
		line2 = list(line.partition(";"))
		if "G90" in line2[0]:
			absolute_pos = True
		if "G91" in line2[0]:
			absolute_pos = False
		if "G1 " in line2[0] and absolute_pos:
			line2[0] = re.sub("([XYZ])([+-]?[0-9]+\.?[0-9]*)", shiftIt, line2[0])
			# f.write(";Processing G1 move: " + line2[0])
		line = "" + line2[0] + line2[1] + line2[2]
		f.write(line)
