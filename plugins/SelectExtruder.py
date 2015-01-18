#Name: Select Extruder 15.01
#Info: Adjusts the used extruder for a single material print
#Help: SelectExtruder
#Depend: GCode
#Type: postprocess
#Param: ExtruderNo(int:0) Extruder to be used (0: 1st ex., 1: 2nd ex.)

## Written by Stefan Heule, Dim3nsioneer@gmx.ch
## This script is licensed under the Creative Commons - Attribution - Share Alike - Non Commercial (CC BY-SA-NC) 3.0 terms

version = '15.01'

import re
import wx
import time

try:
	#MacOS release currently lacks some wx components, like the Publisher.
	from wx.lib.pubsub import Publisher
except:
	Publisher = None

def getValue(line, key, default = None):
	if not key in line or (';' in line and line.find(key) > line.find(';')):
		return default
	subPart = line[line.find(key) + 1:]
	m = re.search('^[0-9]+\.?[0-9]*', subPart)
	if m == None:
		return default
	try:
		return float(m.group(0))
	except:
		return default

if Publisher is not None:
	wx.CallAfter(Publisher().sendMessage, "pluginupdate", "OpenPluginProgressWindow;SelectExtruder;Select Extruder plugin is executed for extruder no. " + str(ExtruderNo))

with open(filename, "r") as f: #r for read
	lines = f.readlines()

lastpercentage = 0
i = 0
l = len(lines)

with open(filename, "w") as f: #w for write
	for line in lines: #Steps through the entire Gcode
		if int(i*100/l) > lastpercentage and Publisher is not None: #progressbar
			lastpercentage = int(i*100/l)
			wx.CallAfter(Publisher().sendMessage, "pluginupdate", "Progress;" + str(lastpercentage))
		if "M109" in line: #look for M109 command (heat up and wait)
			print 'found M109'
			temperature = getValue(line,'S',0)
			f.write("M109 T%d S%f\n" % (int(ExtruderNo),float(temperature)))
			f.write("T%d\n" % int(ExtruderNo))
		elif "M104" in line: #look for M104 command (temperature change)
			temperature = getValue(line,'S',0)
			f.write("M104 T%d S%f\n" % (int(ExtruderNo), float(temperature)))
			f.write("T%d\n" % int(ExtruderNo))
		elif ("T0" in line or "T1" in line) and "M200" not in line: #look for single T command (extruder change)
			f.write("T%d\n" % int(ExtruderNo))
		else:
			f.write(line)

if Publisher is not None:
		wx.CallAfter(Publisher().sendMessage, "pluginupdate", "Progress;100")
		time.sleep(1)
		wx.CallAfter(Publisher().sendMessage, "pluginupdate", "ClosePluginProgressWindow")
