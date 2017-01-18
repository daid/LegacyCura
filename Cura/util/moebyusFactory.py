__copyright__ = "Released under terms of the AGPLv3 License"

import wx
from Cura.util import profile

def setCuraSettings() :
	profile.putPreference('startMode'						, 'Normal')
	profile.putPreference('filament_cost_kg'				, '18')
	profile.putPreference('filament_physical_density'		, '1050')
	profile.putPreference('printing_window'					, 'Pronterface UI')

def setCommonSettings() :
#Default machine settings
	profile.putMachineSetting('gcode_flavor'  				, 'RepRap (Marlin/Sprinter)')
	profile.putMachineSetting('extruder_head_size_min_x'	, '0')
	profile.putMachineSetting('extruder_head_size_min_y'	, '0')
	profile.putMachineSetting('extruder_head_size_max_x'	, '0')
	profile.putMachineSetting('extruder_head_size_max_y'	, '0')
	profile.putMachineSetting('extruder_head_size_height'	, '0')
	profile.putMachineSetting('extruder_offset_x1'		 	, '0')
	profile.putMachineSetting('extruder_offset_y1'			, '0')
	profile.putMachineSetting('has_heated_bed'				, 'True')
	profile.putMachineSetting('machine_center_is_zero'		, 'False')
	profile.putMachineSetting('machine_shape'				, 'Square')	
	profile.putMachineSetting('serial_baud_auto'			, '115200')	
	

#Default print settings
	profile.putProfileSetting('retraction_hop'    			, '0.1')
	profile.putProfileSetting('retraction_dual_amount'		, '22')
	profile.putProfileSetting('cool_min_layer_time'			, '10')
	profile.putProfileSetting('print_speed'       			, '60')
	profile.putProfileSetting('travel_speed'      			, '100')
	profile.putProfileSetting('bottom_layer_speed'			, '40')
	profile.putProfileSetting('solidarea_speed'   			, '40')
	profile.putProfileSetting('inset0_speed'      			, '40')
	profile.putProfileSetting('fill_density'	  			, '25')
	profile.putProfileSetting('print_temperature' 			, '190')
	profile.putProfileSetting('print_bed_temperature'		, '60')	

#Raft & support
	profile.putProfileSetting('support_angle' 			, '50')
	profile.putProfileSetting('support_fill_rate' 		, '18')
	profile.putProfileSetting('support_xy_distance' 	, '1')
	profile.putProfileSetting('support_z_distance' 		, '0.18')
	profile.putProfileSetting('raft_margin' 			, '6')
	profile.putProfileSetting('raft_line_spacing' 		, '3.0')
	profile.putProfileSetting('raft_base_thickness' 	, '0.3')
	profile.putProfileSetting('raft_interface_thickness', '0.2')
	profile.putProfileSetting('raft_airgap_all' 		, '0.0')
	profile.putProfileSetting('raft_airgap' 			, '0.25')
	profile.putProfileSetting('raft_surface_layers' 	, '2')
	profile.putProfileSetting('raft_surface_thickness' 	, '0.2')
						
def setAlterations() :
	profile.setAlterationFile('start.gcode', """;Sliced at: {day} {date} {time}
;Basic settings: Layer height: {layer_height} Walls: {wall_thickness} Fill: {fill_density}
;Print time: {print_time}
;Filament used: {filament_amount}m {filament_weight}g
;Filament cost: {filament_cost}
;M190 S{print_bed_temperature} ;Uncomment to add your own bed temperature line
;M109 S{print_temperature} ;Uncomment to add your own temperature line
G21                     ;metric values
G90                     ;absolute positioning
M82                     ;set extruder to absolute mode
M107                    ;start with the fan off
G28
G29                     ;Run the auto bed leveling
G1 X0 Y0 Z5.0 F{travel_speed} 
G92 E0                  ;zero the extruded length
G1 F300 E25             ;extrude
G92 E0                  ;zero the extruded length again
G0 Z0.5 Y20 F1000
G0 Y50
G1 F{travel_speed}
;Put printing message on LCD screen
M117 Materializando...
""")

	profile.setAlterationFile('end.gcode', """;Sliced at: {day} {date} {time}
;End GCode
M104 S0                    ;extruder heater off
M140 S0                    ;heated bed heater off (if you have it)
G91                        ;relative positioning
G1 E-2.5 F300              ;retract the filament a bit before lifting the nozzle, to release some of the pressure
G1 Z+2 E-3 F{travel_speed} ;move Z up a bit and retract filament even more
G28 XY                     ;move X/Y to min endstops, so the head is out of the way
M84                        ;steppers off
G90                        ;absolute positioning
M117 Terminado!
;{profile_string}
""")

def setAlterationsMelta() :
	profile.setAlterationFile('start.gcode', """;Sliced at: {day} {date} {time}
;Basic settings: Layer height: {layer_height} Walls: {wall_thickness} Fill: {fill_density}
;Print time: {print_time}
;Filament used: {filament_amount}m {filament_weight}g
;Filament cost: {filament_cost}
;M190 S{print_bed_temperature} ;Uncomment to add your own bed temperature line
;M109 S{print_temperature} ;Uncomment to add your own temperature line
G21                     ;metric values
G90                     ;absolute positioning
M82                     ;set extruder to absolute mode
M107                    ;start with the fan off
G28   
G29                     ;Run the auto bed leveling
G1 Z50 F{travel_speed} ;move the platform down 5mm
G1 X65
G92 E0                  ;zero the extruded length
G1 F200 E20             ;extrude 3mm of feed stock
G92 E0                  ;zero the extruded length again
G0 Z0.5 X60
G1 F{travel_speed}
;Put printing message on LCD screen
M117 Materializando...
""")		

def setAlterationsMeltaXXL() :
	profile.setAlterationFile('start.gcode', """;Sliced at: {day} {date} {time}
;Basic settings: Layer height: {layer_height} Walls: {wall_thickness} Fill: {fill_density}
;Print time: {print_time}
;Filament used: {filament_amount}m {filament_weight}g
;Filament cost: {filament_cost}
;M190 S{print_bed_temperature} ;Uncomment to add your own bed temperature line
;M109 S{print_temperature} ;Uncomment to add your own temperature line
G21                     ;metric values
G90                     ;absolute positioning
M82                     ;set extruder to absolute mode
M107                    ;start with the fan off
G28   
G29                     ;Run the auto bed leveling
G1 Z50 F{travel_speed} ;move the platform down 5mm
G1 X180
G92 E0                  ;zero the extruded length
G1 F200 E20             ;extrude 3mm of feed stock
G92 E0                  ;zero the extruded length again
G0 Z0.5 X175
G1 F{travel_speed}
;Put printing message on LCD screen
M117 Materializando...
""")

def setAlterationsM3() :
	profile.setAlterationFile('start.gcode', """;Sliced at: {day} {date} {time}
;Basic settings: Layer height: {layer_height} Walls: {wall_thickness} Fill: {fill_density}
;Print time: {print_time}
;Filament used: {filament_amount}m {filament_weight}g
;Filament cost: {filament_cost}
;M190 S{print_bed_temperature} ;Uncomment to add your own bed temperature line
;M109 S{print_temperature} ;Uncomment to add your own temperature line
G21                     ;metric values
G90                     ;absolute positioning
M82                     ;set extruder to absolute mode
M107                    ;start with the fan off
G28   
G29                     ;Run the auto bed leveling
G1 Z5.0 F{travel_speed} ;move the platform down 5mm
G92 E0                  ;zero the extruded length
G1 F200 E25             ;extrude 3mm of feed stock
G92 E0                  ;zero the extruded length again
G0 Z0.5 Y50 E40
G1 F{travel_speed}
;Put printing message on LCD screen
M117 Materializando...
""")

def setAlterationsOne() :
	profile.setAlterationFile('start.gcode', """;Sliced at: {day} {date} {time}
;Basic settings: Layer height: {layer_height} Walls: {wall_thickness} Fill: {fill_density}
;Print time: {print_time}
;Filament used: {filament_amount}m {filament_weight}g
;Filament cost: {filament_cost}
;M190 S{print_bed_temperature} ;Uncomment to add your own bed temperature line
;M109 S{print_temperature} ;Uncomment to add your own temperature line
G21                     ;metric values
G90                     ;absolute positioning
M82                     ;set extruder to absolute mode
M107                    ;start with the fan off
G28   
G29                     ;Run the auto bed leveling
G1 Z5.0 F{travel_speed} ;move the platform down 5mm
G92 E0                  ;zero the extruded length
G1 F200 E15             ;extrude 3mm of feed stock
G0 Z0.5 X10
G0 X120 E30
G92 E0                  ;zero the extruded length again
G1 F{travel_speed}
;Put printing message on LCD screen
M117 Materializando...
""")		

def setAlterationsSirius() :
	profile.setAlterationFile('start2.gcode', """;Sliced at: {day} {date} {time}
;Basic settings: Layer height: {layer_height} Walls: {wall_thickness} Fill: {fill_density}
;Print time: {print_time}
;Filament used: {filament_amount}m {filament_weight}g
;Filament cost: {filament_cost}
;M190 S{print_bed_temperature} ;Uncomment to add your own bed temperature line
;M109 S{print_temperature}  ;Uncomment to add your own temperature line
G21                         ;metric values
G90                         ;absolute positioning
M82                         ;set extruder to absolute mode
M107                        ;start with the fan off
G28   
G29                         ;Run the auto bed leveling

T1
G1 X300 Y0 Z5.0 F{travel_speed} 
G92 E0                  ;zero the extruded length
G1 F200 E20             ;extrude 3mm of feed stock
G92 E0                  ;zero the extruded length again
G0 Z0.5 Y10
G1 F400 E-{retraction_dual_amount}
G0 Y40

T0                          ;Switch to the first extruder
G1 X0 Y0 Z5.0 F{travel_speed} 
G92 E0                  ;zero the extruded length
G1 F200 E20             ;extrude 3mm of feed stock
G92 E0                  ;zero the extruded length again
G0 Z0.5 Y10
G0 Y40

G1 F{travel_speed}
;Put printing message on LCD screen
M117 Materializando...
""")

	profile.setAlterationFile('end2.gcode', """;Sliced at: {day} {date} {time}
;End GCode
M104 T0 S0                 ;extruder heater off
M104 T1 S0                 ;extruder heater off
M140 S0                    ;heated bed heater off (if you have it)
G91                        ;relative positioning
G1 E-2.5 F300              ;retract the filament a bit before lifting the nozzle, to release some of the pressure
G1 Z+2 E-3 F{travel_speed} ;move Z up a bit and retract filament even more
G28 XY                     ;move X/Y to min endstops, so the head is out of the way
M84                        ;steppers off
G90                        ;absolute positioning
M117 Terminado!
;{profile_string}
""")

def setAlterationsSiriusRight() :
	profile.setAlterationFile('start.gcode', """;Sliced at: {day} {date} {time}
;Basic settings: Layer height: {layer_height} Walls: {wall_thickness} Fill: {fill_density}
;Print time: {print_time}
;Filament used: {filament_amount}m {filament_weight}g
;Filament cost: {filament_cost}
;M190 S{print_bed_temperature} ;Uncomment to add your own bed temperature line
;M109 S{print_temperature} ;Uncomment to add your own temperature line
G21                     ;metric values
G90                     ;absolute positioning
M82                     ;set extruder to absolute mode
M107                    ;start with the fan off
G28
G29                     ;Run the auto bed leveling
T1
G1 X300 Y0 Z5.0 F{travel_speed} 
G92 E0                  ;zero the extruded length
G1 F300 E20             ;extrude 3mm of feed stock
G92 E0                  ;zero the extruded length again
G0 Z0.5 Y10
G0 Y40

G1 F{travel_speed}
;Put printing message on LCD screen
M117 Materializando...
""")

	profile.setAlterationFile('end.gcode', """;Sliced at: {day} {date} {time}
;End GCode
M104 S0                    ;extruder heater off
M140 S0                    ;heated bed heater off (if you have it)
G91                        ;relative positioning
G1 E-2.5 F300              ;retract the filament a bit before lifting the nozzle, to release some of the pressure
G1 Z+2 E-3 F{travel_speed} ;move Z up a bit and retract filament even more
G28 XY                     ;move X/Y to min endstops, so the head is out of the way
M84                        ;steppers off
G90                        ;absolute positioning
M117 Terminado!
T0
;{profile_string}
""")
	
def setAlterationsSiriusDuplicator() :
	profile.setAlterationFile('start.gcode', """;Sliced at: {day} {date} {time}
;Basic settings: Layer height: {layer_height} Walls: {wall_thickness} Fill: {fill_density}
;Print time: {print_time}
;Filament used: {filament_amount}m {filament_weight}g
;Filament cost: {filament_cost}
;M190 S{print_bed_temperature} ;Uncomment to add your own bed temperature line
;M109 S{print_temperature} ;Uncomment to add your own temperature line
G21                     ;metric values
G90                     ;absolute positioning
M82                     ;set extruder to absolute mode
M107                    ;start with the fan off
M605 S2
G28
G29                     ;Run the auto bed leveling
G1 Z5.0 F{travel_speed} ;move the platform down 5mm
G92 E0                  ;zero the extruded length
G1 F200 E20             ;extrude 3mm of feed stock
G92 E0                  ;zero the extruded length again
G0 Z0.5 Y5
G1 F{travel_speed}
;Put printing message on LCD screen
M117 Materializando...
""")

	profile.setAlterationFile('end.gcode', """;Sliced at: {day} {date} {time}
;End GCode
M104 S0                    ;extruder heater off
M140 S0                    ;heated bed heater off (if you have it)
G91                        ;relative positioning
G1 E-2.5 F300              ;retract the filament a bit before lifting the nozzle, to release some of the pressure
G1 Z+2 E-3 F{travel_speed} ;move Z up a bit and retract filament even more
G28 XY                     ;move X/Y to min endstops, so the head is out of the way
M605 S1
M84                        ;steppers off
G90                        ;absolute positioning
M117 Terminado!
;{profile_string}
""")

def setMachineProperties(machineType = "PrusaI3MM", filamentSize = 3 , nozzleSize = 0.4) :
	_printer_info = [
		("Moebyus One"				, 150, 150, 150, "MoebyusOne"),
		("Prusa i3 MM"				, 200, 200, 190, "PrusaI3MM" ),
		("Prusa i3 MM Large"		, 200, 300, 190, "PrusaI3MM-L"),
		("Steel MM"					, 200, 200, 200, "SteelMM"),
		("Steel MM Large"			, 310, 200, 260, "SteelMM-L"),
		("Steel MM Marco Sirius"	, 310, 200, 260, "SteelMM-Sirius"),
		("Melta Kossel"				, 160, 160, 300, "Melta"),
		("Melta XL"					, 400, 400, 600, "MeltaXL"),
		("[SIRIUS] Normal & Dual"	, 300, 200, 200, "Sirius1"),
		("[SIRIUS] Right Extruder"	, 300, 200, 200, "Sirius1-right"),		
		("[SIRIUS] Duplicator"		, 150, 200, 200, "Sirius1-duplication"),
		("[SIRIUS] Normal & Dual"	, 310, 200, 260, "Sirius11"),
		("[SIRIUS] Right Extruder"	, 310, 200, 260, "Sirius11-right"),
		("[SIRIUS] Duplicator"		, 150, 200, 260, "Sirius11-duplication"),
		("Moebyus M3"				, 1000,1000,1000, "M3") ]

	profile.putMachineSetting('machine_type'  		, machineType)
	profile.putProfileSetting('nozzle_size' 		, nozzleSize)
	profile.putPreference	 ('simpleModeNozzle' 	, nozzleSize)
	
	profile.putProfileSetting('filament_diameter'	, filamentSize)
	profile.putProfileSetting('retraction_speed' 	, 60)
	profile.putProfileSetting('retraction_amount'	, 3.5)


	profile.putMachineSetting('machine_width' , 199)
	profile.putMachineSetting('machine_depth' , 199)
	profile.putMachineSetting('machine_height', 199)
	
	for machineInfo in _printer_info :
		if machineInfo[4] == machineType:
			profile.putMachineSetting('machine_name'  , machineInfo[0])
			profile.putMachineSetting('machine_width' , machineInfo[1])
			profile.putMachineSetting('machine_depth' , machineInfo[2])
			profile.putMachineSetting('machine_height', machineInfo[3])

	profile.putProfileSetting('layer_height'			, float(nozzleSize) / 2)
	profile.putProfileSetting('bottom_thickness'		, float(nozzleSize) / 2)
	profile.putProfileSetting('wall_thickness'			, float(nozzleSize) * 2)
	profile.putProfileSetting('solid_layer_thickness'	, float(profile.getProfileSettingFloat('layer_height')) * 4)
	profile.putProfileSetting('raft_base_linewidth' 	, float(nozzleSize) * 2 )
	profile.putProfileSetting('raft_interface_linewidth', float(nozzleSize) * 1.25)
	profile.putProfileSetting('raft_surface_linewidth' 	, float(nozzleSize) * 1.1 )
		
	setAlterations()
	if machineType == 'Melta':
		profile.putMachineSetting('has_heated_bed', 'False')
		profile.putMachineSetting('machine_center_is_zero', 'True')	
		profile.putMachineSetting('machine_shape', 'Circular')
		setAlterationsMelta()
	elif machineType == 'MeltaXL':
		profile.putMachineSetting('has_heated_bed', 'True')
		profile.putMachineSetting('machine_center_is_zero', 'True')	
		profile.putMachineSetting('machine_shape', 'Circular')
		setAlterationsMeltaXXL()
	elif machineType == 'M3':
		profile.putMachineSetting('has_heated_bed', 'False')
		profile.putMachineSetting('machine_center_is_zero', 'False')	
		profile.putMachineSetting('machine_shape', 'Square')		
		setAlterationsM3()
	elif machineType == 'MoebyusOne':
		profile.putMachineSetting('has_heated_bed'				, 'False')
		profile.putMachineSetting('machine_center_is_zero'		, 'False')
		profile.putMachineSetting('machine_shape'				, 'Square')
		profile.putProfileSetting('platform_adhesion'			, 'Raft')
		profile.putPreference	 ('simpleModePlatformAdhesion'	, '2')

		profile.putProfileSetting('fan_full_height'			, '0.5')
		profile.putProfileSetting('fan_speed' 				, '60')
		profile.putProfileSetting('fan_speed_max' 			, '90')
		profile.putProfileSetting('cool_min_feedrate' 		, '10')
		profile.putPreference	 ('startMode'				, 'Simple')
		
		setAlterationsOne()
	elif machineType == 'Sirius1' or machineType == 'Sirius11':
		profile.putMachineSetting('extruder_amount', '2')
		setAlterationsSirius()
	elif machineType == 'Sirius1-right' or machineType == 'Sirius11-right':
		profile.putMachineSetting('extruder_amount', '1')
		setAlterationsSirius()
	elif machineType == 'Sirius1-duplication' or machineType == 'Sirius11-duplication':
		profile.putMachineSetting('extruder_amount', '1')
		setAlterationsSirius()

def genProfileForMachine (machineType = "PrusaI3MM", filamentSize = 3 , nozzleSize = 0.4) :
	print("Gen Profile for:")
	print(machineType)

	if machineType == 'Sirius1' :
		setCommonSettings()
		setMachineProperties('Sirius1-duplication',filamentSize,nozzleSize)
		profile.checkAndUpdateMachineName()
		profile.setActiveMachine(profile.getMachineCount())
		setCommonSettings()
		setMachineProperties('Sirius1-right',filamentSize,nozzleSize)
		profile.checkAndUpdateMachineName()
		profile.setActiveMachine(profile.getMachineCount())
	elif machineType == 'Sirius11':
		setCommonSettings()
		setMachineProperties('Sirius11-duplication',filamentSize,nozzleSize)
		profile.checkAndUpdateMachineName()
		profile.setActiveMachine(profile.getMachineCount())
		setCommonSettings()
		setMachineProperties('Sirius11-right',filamentSize,nozzleSize)
		profile.checkAndUpdateMachineName()
		profile.setActiveMachine(profile.getMachineCount())
		
	setCommonSettings()
	setMachineProperties(machineType,filamentSize,nozzleSize)

	
