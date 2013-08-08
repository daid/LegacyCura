from __future__ import absolute_import
from __future__ import division
__copyright__ = "Copyright (C) 2013 David Braam - Released under terms of the AGPLv3 License"

import os, traceback, math, re, zlib, base64, time, sys, platform, glob, string, stat, types
import cPickle as pickle
if sys.version_info[0] < 3:
	import ConfigParser
else:
	import configparser as ConfigParser

from Cura.util import resources
from Cura.util import version
from Cura.util import validators

settingsDictionary = {}
settingsList = []
class setting(object):
	def __init__(self, name, default, type, category, subcategory):
		self._name = name
		self._label = name
		self._tooltip = ''
		self._default = unicode(default)
		self._value = self._default
		self._type = type
		self._category = category
		self._subcategory = subcategory
		self._validators = []
		self._conditions = []

		if type is types.FloatType:
			validators.validFloat(self)
		elif type is types.IntType:
			validators.validInt(self)

		global settingsDictionary
		settingsDictionary[name] = self
		global settingsList
		settingsList.append(self)

	def setLabel(self, label, tooltip = ''):
		self._label = label
		self._tooltip = tooltip
		return self

	def setRange(self, minValue = None, maxValue = None):
		if len(self._validators) < 1:
			return
		self._validators[0].minValue = minValue
		self._validators[0].maxValue = maxValue
		return self

	def getLabel(self):
		return self._label

	def getTooltip(self):
		return self._tooltip

	def getCategory(self):
		return self._category

	def getSubCategory(self):
		return self._subcategory

	def isPreference(self):
		return self._category == 'preference'

	def isAlteration(self):
		return self._category == 'alteration'

	def isProfile(self):
		return not self.isAlteration() and not self.isPreference()

	def getName(self):
		return self._name

	def getType(self):
		return self._type

	def getValue(self):
		return self._value

	def getDefault(self):
		return self._default

	def setValue(self, value):
		self._value = unicode(value)

	def validate(self):
		result = validators.SUCCESS
		msgs = []
		for validator in self._validators:
			res, err = validator.validate()
			if res == validators.ERROR:
				result = res
			elif res == validators.WARNING and result != validators.ERROR:
				result = res
			if res != validators.SUCCESS:
				msgs.append(err)
		return result, '\n'.join(msgs)

	def addCondition(self, conditionFunction):
		self._conditions.append(conditionFunction)

	def checkConditions(self):
		for condition in self._conditions:
			if not condition():
				return False
		return True

#########################################################
## Settings
#########################################################
setting('layer_height',              0.1, float, 'basic',    '质量').setRange(0.0001).setLabel('层厚(mm)', '层厚的单位是毫米。\n这是影响打印质量最重要的设定。0.1mm用于普通质量的打印。\n0.05mm用于高质量的打印。0.2mm用于高速低质量的打印。')
setting('wall_thickness',            0.4, float, 'basic',    '质量').setRange(0.0).setLabel('壁厚(mm)', '外壁水平方向上的厚度。\n取决于喷头直径和外壁周长。')
setting('retraction_enable',       False, bool,  'basic',    '质量').setLabel('允许回滚', '在非打印区域时回滚丝料。具体的设定可以在高级打印设置菜单中设置。')
setting('solid_layer_thickness',     0.9, float, 'basic',    '填充').setRange(0).setLabel('底部/顶部厚度 (mm)', '这个设定决定了顶部和底部的厚度，这里的数量是由顶部和底部实心层数来决定的。\n建议该设定和壁厚一起考虑，建议将顶部\底部厚度设置成壁厚的倍数。\n顶部\底部厚度接近于层厚是比较均衡的设定。')
setting('fill_density',               20, float, 'basic',    '填充').setRange(0, 100).setLabel('填充率 (%)', '这个参数决定了模型的填充率，实体的填充率一般使用100％\n（一般用到90％足够了），空心体使用0％。\n20％的填充率对一般的模型通常是足够了。\n这个设定一般不影响外观，但会对模型强度造成影响。')
setting('nozzle_size',               0.4, float, 'advanced', '设备尺寸').setRange(0.1,10).setLabel('喷头直径 (mm)', '喷头直径非常重要，喷头直径是用来计算在打印设定中\n您所选择的填充的线的宽度、外壁线宽以及壁厚。')
setting('print_speed',                60, float, 'basic',    '速度与温度').setRange(1).setLabel('打印速度 (mm/s)', '打印速度的设置如果需要打印质量提高，可以适当降低打印\n速度。调整好的设备可以将速度提高到150mm/s。\n打印速度和很多因素有关，您需要仔细优化调整你的机器并选择一个合适的打印速度。')
setting('print_temperature',         220, int,   'basic',    '速度与温度').setRange(0,340).setLabel('打印温度 (C)', '打印时喷头需要的温度设置为0时由用户自行预热。\nPLA一般采用220℃。\nABS一般设置为230℃或更高。')
setting('print_temperature2',          0, int,   'basic',    '速度与温度').setRange(0,340).setLabel('第2喷头打印温度 (C)', '打印时喷头需要的温度设置为0时由用户自行预热。\nPLA一般采用220℃。\nABS一般设置为230℃或更高。')
setting('print_temperature3',          0, int,   'basic',    '速度与温度').setRange(0,340).setLabel('第3喷头打印温度 (C)', '打印时喷头需要的温度设置为0时由用户自行预热。\nPLA一般采用220℃。\nABS一般设置为230℃或更高。')
setting('print_temperature4',          0, int,   'basic',    '速度与温度').setRange(0,340).setLabel('第4喷头打印温度 (C)', '打印时喷头需要的温度设置为0时由用户自行预热。\nPLA一般采用220℃。\nABS一般设置为230℃或更高。')
setting('print_bed_temperature',      70, int,   'basic',    '速度与温度').setRange(0,340).setLabel('加热板温度 (C)', '加热板温度，设置为0时由用户自行预热')
setting('support',                'None', ['None', 'Touching buildplate', 'Everywhere'], 'basic', '支撑结构').setLabel('支撑类型', '支撑结构的类型\n"Touching buildplate" 是最常用的支撑结构。\nNone表示不打支撑结构 \n“Touching buildplate”支撑类型仅生成需要从底部到接触面的支撑结构。\n例如T型结构选择Touching buildplate。\n“Everywhere”支撑类型将全面生成支撑。\n例如F型结构选择Everywhere。')
setting('platform_adhesion',      'None', ['None', 'Brim', 'Raft'], 'basic', '支撑结构').setLabel('平台粘附类型', '不同的选项来防止模型边角的翘曲。\nBrim边缘在整个模型外围增加一圈薄片，这些薄片可以被很容易剥离。推荐选项。\nraft剥离基层是在实体下的几层松散结构。\n（注意如果选择brim边缘或者raft剥离基层将会禁用裙边。）')
setting('support_dual_extrusion',  False, bool, 'basic', '支撑结构').setLabel('支撑材料（第2喷头）', '在多喷头情况下，采用第2喷头作为支撑材料的打印。')
setting('filament_diameter',        1.75, float, 'basic',    '材料').setRange(1).setLabel('线径 (mm)', '材料线径。\n如果你无法准确测量该值，你可以校准该值，数字越大，挤出越少，数字越小，挤出越多。')
setting('filament_diameter2',          0, float, 'basic',    '材料').setRange(0).setLabel('第2喷头线径 (mm)', '第2喷头使用的材料线径，设为0表示和第1喷头使用相同的线径。')
setting('filament_diameter3',          0, float, 'basic',    '材料').setRange(0).setLabel('第3喷头线径 (mm)', '第3喷头使用的材料线径，设为0表示和第1喷头使用相同的线径。')
setting('filament_diameter4',          0, float, 'basic',    '材料').setRange(0).setLabel('第4喷头线径 (mm)', '第4喷头使用的材料线径，设为0表示和第1喷头使用相同的线径。')
setting('filament_flow',            100., float, 'basic',    '材料').setRange(1,300).setLabel('流量 (%)', '流量补偿, 挤出量是原设定值与该值相乘的结果。')
#setting('retraction_min_travel',     5.0, float, 'advanced', 'Retraction').setRange(0).setLabel('Minimum travel (mm)', 'Minimum amount of travel needed for a retraction to happen at all. To make sure you do not get a lot of retractions in a small area')
setting('retraction_speed',         60.0, float, 'advanced', '回滚').setRange(0.1).setLabel('回滚速度 (mm/s)', '回滚速度是指线材回滚的速度。高速回滚能够使拉丝减轻，但太高速易导致线材磨损。')
setting('retraction_amount',         4.5, float, 'advanced', '回滚').setRange(0).setLabel('回滚距离 (mm)', '线材回滚的距离，设置为0则不回滚，4.5mm的回滚距离效果一般不错')
#setting('retraction_extra',          0.0, float, 'advanced', 'Retraction').setRange(0).setLabel('Extra length on start (mm)', 'Extra extrusion amount when restarting after a retraction, to better "Prime" your extruder after retraction.')
setting('retraction_dual_amount',   16.5, float, 'advanced', '回滚').setRange(0).setLabel('双头切换回滚距离 (mm)', '在多喷头情况下，切换喷头时回滚丝料的距离。\n设为0表示完全不回滚。设为16.5mm一般效果较好。')
setting('bottom_thickness',          0.2, float, 'advanced', '质量').setRange(0).setLabel('初始层高度 (mm)', '底层的厚度，厚一些能和底板粘的更牢。设为0则厚度和其他层相同。')
setting('object_sink',               0.0, float, 'advanced', '质量').setLabel('底部切除距离(mm)', '将模型下沉至平台下部，切除部分模型。\n一般用于模型没有一个较大平面，不利于打印，\n利用此功能可以形成一个较理想的平面，提高打印成功率。')
#setting('enable_skin',             False, bool,  'advanced', 'Quality').setLabel('Duplicate outlines', 'Skin prints the outer lines of the prints twice, each time with half the thickness. This gives the illusion of a higher print quality.')
setting('overlap_dual',              0.2, float, 'advanced', '质量').setLabel('双头重叠量 (mm)', '在双头打印时增加一定量的重叠部分，这对用两种颜色打印的情况有帮助。')
setting('travel_speed',            150.0, float, 'advanced', '速度').setRange(0.1).setLabel('空驶速度 (mm/s)', '非打印时移动速度，一般不建议设置超过250mm/s。超过这个数值可能会失步。')
setting('bottom_layer_speed',         40, float, 'advanced', '速度').setRange(0.1).setLabel('底层打印速度 (mm/s)', '底层打印速度，降低第一层的打印速度可以使打印件更好的和打印平台粘结更好。')
setting('infill_speed',              120, float, 'advanced', '速度').setRange(0.0).setLabel('填充速度 (mm/s)', '打印填充时的速度。如果设成0，则填充速度和打印速度相同。\n填充打印速度增快可以显著的降低打印时间，但是可能会对打印效果产生负面影响。')
setting('cool_min_layer_time',         5, float, 'advanced', '冷却设定').setRange(0).setLabel('层最小打印时间 (sec)', '每层最短时间，每次打印下一层之前留够足够的时间来冷却。\n如果打印的太快，将会降低打印速度延长时间来确保冷却。')
setting('fan_enabled',              True, bool,  'advanced', '冷却设定').setLabel('允许风扇冷却', '允许在打印时用风扇进行冷却。快速打印时风扇是必要的选项。')

setting('skirt_line_count',            3, int,   'expert', '裙边').setRange(0).setLabel('圈数', '裙边是在打印模型前第一层上围绕模型打印的线。\n这是为了喷头预挤出并帮助查看平台是否适合打印。\n设置为0即表示取消裙边。打印小物体时可设置\n更大的值来帮助预挤出。')
setting('skirt_gap',                 3.0, float, 'expert', '裙边').setRange(0).setLabel('间距 (mm)', '裙边与模型第一层的距离。\n这是最小距离，若需要更多裙边，\n则会在此距离上向外扩展打印裙边。')
#setting('max_z_speed',               3.0, float, 'expert',   'Speed').setRange(0.1).setLabel('Max Z speed (mm/s)', 'Speed at which Z moves are done. When you Z axis is properly lubricated you can increase this for less Z blob.')
#setting('retract_on_jumps_only',    True, bool,  'expert',   'Retraction').setLabel('Retract on jumps only', 'Only retract when we are making a move that is over a hole in the model, else retract on every move. This effects print quality in different ways.')
setting('fan_layer',                   1, int,   'expert',   '冷却设定').setRange(0).setLabel('风扇启动层数', '风扇将在设定层启动。第一层的设置值是0。建议可以在第一层关闭风扇以帮助更好地黏在底板上，并在第二层开启风扇。')
setting('fan_speed',                 100, int,   'expert',   '冷却设定').setRange(0,100).setLabel('风扇最小风速 (%)', '当冷却风扇被启动时，这个设定将起作用。开启风扇冷却时，会自动根据温度来调整风速，调整的范围将在最大和最小风速之间自动调节。如果冷却不会降低打印速度，就会启动风扇最小风速。')
setting('fan_speed_max',             100, int,   'expert',   '冷却设定').setRange(0,100).setLabel('风扇最大风速 (%)', '当冷却风扇被启动时，这个设定将起作用。风扇冷却时，会自动根据温度来调整风速，调整的范围将在最大和最小风速之间自动调节。冷却效果可以设定为200%。')
setting('cool_min_feedrate',          10, float, 'expert',   '冷却设定').setRange(0).setLabel('最低速度（ (mm/s)', '最少层花的时间会使打印速度降低很多，这样喷头的材料就会溢出。最小进料速度就会防止这个问题发生。即使是打印速度变慢也不会低于这个最低速度。')
setting('cool_head_lift',          False, bool,  'expert',   '冷却设定').setLabel('抬高打印头冷却', '打印时为确保冷却时间将打印速度降低到最低速度时\n仍不能保证冷却时间时，就抬高打印头，并等一段时间来确保达到打印最少层的时间。')
#setting('extra_base_wall_thickness', 0.0, float, 'expert',   'Accuracy').setRange(0).setLabel('Extra Wall thickness for bottom/top (mm)', 'Additional wall thickness of the bottom and top layers.')
#setting('sequence', 'Loops > Perimeter > Infill', ['Loops > Perimeter > Infill', 'Loops > Infill > Perimeter', 'Infill > Loops > Perimeter', 'Infill > Perimeter > Loops', 'Perimeter > Infill > Loops', 'Perimeter > Loops > Infill'], 'expert', 'Sequence')
#setting('force_first_layer_sequence', True, bool, 'expert', 'Sequence').setLabel('Force first layer sequence', 'This setting forces the order of the first layer to be \'Perimeter > Loops > Infill\'')
#setting('infill_type', 'Line', ['Line', 'Grid Circular', 'Grid Hexagonal', 'Grid Rectangular'], 'expert', 'Infill').setLabel('Infill pattern', 'Pattern of the none-solid infill. Line is default, but grids can provide a strong print.')
setting('solid_top', True, bool, 'expert', '填充').setLabel('顶部实心填充', '在顶部进行实心填充，如果不勾选，将以填充率填充。适用于打印杯或瓶。')
setting('solid_bottom', True, bool, 'expert', '填充').setLabel('底部实心填充', '在底部进行实心填充，如果不勾选，将以填充率填充。适用于打印建筑。')
setting('fill_overlap', 15, int, 'expert', '填充').setRange(0,100).setLabel('重叠填充率 (%)', '内部填充与内外壁的重叠比例。轻微的重叠填充能使结构更坚固。')
setting('support_rate', 60, int, 'expert', '支撑').setRange(0,100).setLabel('材料用量 (%)', '用于支撑的材料用量。较少材料会使支撑更脆弱，也更容易去除。')
#setting('support_distance',  0.5, float, 'expert', 'Support').setRange(0).setLabel('Distance from object (mm)', 'Distance between the support structure and the object. Empty gap in which no support structure is printed.')
#setting('joris', False, bool, 'expert', 'Joris').setLabel('Spiralize the outer contour', '[Joris] is a code name for smoothing out the Z move of the outer edge. This will create a steady Z increase over the whole print. It is intended to be used with a single walled wall thickness to make cups/vases.')
#setting('bridge_speed', 100, int, 'expert', 'Bridge').setRange(0,100).setLabel('Bridge speed (%)', 'Speed at which layers with bridges are printed, compared to normal printing speed.')
setting('brim_line_count', 20, int, 'expert', '边缘').setRange(1,100).setLabel('边缘线数量', '用于打印边缘的线的数量。多的话可以形成更大的边缘使得粘附力更强，但有效打印面积会缩小。')
setting('raft_margin', 5, float, 'expert', '剥离基层').setRange(0).setLabel('额外边缘 (mm)', '如果选择使用剥离基层，则额外边缘将决定在已经有剥离基层的物体外围额外的支撑距离。当你打印需要耗用较多材料而打印件使用的材料不多时，增加边缘数量会使得剥离基层的强度加强。')
setting('raft_line_spacing', 1.0, float, 'expert', '剥离基层').setRange(0).setLabel('行距 (mm)', '这是使用剥离基层时剥离基层打印线的中心线的距离。')
setting('raft_base_thickness', 0.3, float, 'expert', '剥离基层').setRange(0).setLabel('基础层厚度 (mm)', '这是使用剥离基层时所打印出的基础层厚度。')
setting('raft_base_linewidth', 0.7, float, 'expert', '剥离基层').setRange(0).setLabel('基础层线宽 (mm)', '这是使用剥离基层时所打印出的基础层线宽。')
setting('raft_interface_thickness', 0.2, float, 'expert', '剥离基层').setRange(0).setLabel('接触面厚度 (mm)', '这是使用剥离基层时所打印出的接触面厚度。')
setting('raft_interface_linewidth', 0.2, float, 'expert', '剥离基层').setRange(0).setLabel('接触面线宽 (mm)', '这是使用剥离基层时所打印出的接触面线宽。')
#setting('hop_on_move', False, bool, 'expert', 'Hop').setLabel('Enable hop on move', 'When moving from print position to print position, raise the printer head 0.2mm so it does not knock off the print (experimental).')
setting('fix_horrible_union_all_type_a', False, bool, 'expert', '极端修复').setLabel('模型合并 (Type-A)', '这个高级选项是把模型的所有部分结合起来。有时打印会使模型内部腔体消失。\n这个选项可以让你选择是否体现内部腔体。\n您要自行承担选择这个选项的风险。\nA型号基于模型的法向并试图保持内部孔的完整。B型号忽略了内部所有的孔洞，\n以保证模型表面的形状。')
setting('fix_horrible_union_all_type_b', False, bool, 'expert', '极端修复').setLabel('模型合并 (Type-B)', '这个高级选项是把模型的所有部分结合起来。有时打印会使模型内部腔体消失。\n这个选项可以让你选择是否体现内部腔体。\n您要自行承担选择这个选项的风险。\nA型号基于模型的法向并试图保持内部孔的完整。B型号忽略了内部所有的孔洞，\n以保证模型表面的形状。')
setting('fix_horrible_use_open_bits', False, bool, 'expert', '极端修复').setLabel('开放面', '这个高级选项完整地保持了完整模型的开孔处。一般来说Cura会尽量填补小的孔隙，\n并用大孔来去除所有内部细节，但这个选项会保留所有的缝隙并按原有形态进行。\n这个选项通常你不会用到，选中这个选项有可能解决以前不能生成合适路径的模型的问题。\n所有的极端修复的选项都会产生很奇怪的情况，你必须自行承担这个风险。')
setting('fix_horrible_extensive_stitching', False, bool, 'expert', '极端修复').setLabel('封闭间隙', '封闭间隙选项通过构造多边形来帮助封闭和修复开放面、孔洞等。这个算法计算开销很大，会增加很多的生成时间。\n所有的极端修复的选项都会产生很奇怪的情况，你必须自行承担这个风险。')

setting('plugin_config', '', str, 'hidden', 'hidden')
setting('object_center_x', -1, float, 'hidden', 'hidden')
setting('object_center_y', -1, float, 'hidden', 'hidden')

setting('start.gcode', """;Sliced at: {day} {date} {time}
;Basic settings: Layer height: {layer_height} Walls: {wall_thickness} Fill: {fill_density}
;Print time: {print_time}
;Filament used: {filament_amount}m {filament_weight}g
;Filament cost: {filament_cost}
G21        ;metric values
G90        ;absolute positioning
M107       ;start with the fan off

G28 X0 Y0  ;move X/Y to min endstops
G28 Z0     ;move Z to min endstops

G1 Z15.0 F{travel_speed} ;move the platform down 15mm

G92 E0                  ;zero the extruded length
G1 F200 E3              ;extrude 3mm of feed stock
G92 E0                  ;zero the extruded length again
G1 F{travel_speed}
M117 Printing...
""", str, 'alteration', 'alteration')
#######################################################################################
setting('end.gcode', """;End GCode
M104 S0                     ;extruder heater off
M140 S0                     ;heated bed heater off (if you have it)

G91                                    ;relative positioning
G1 E-1 F300                            ;retract the filament a bit before lifting the nozzle, to release some of the pressure
G1 Z+0.5 E-5 X-20 Y-20 F{travel_speed} ;move Z up a bit and retract filament even more
G28 X0 Y0                              ;move X/Y to min endstops, so the head is out of the way

M84                         ;steppers off
G90                         ;absolute positioning
""", str, 'alteration', 'alteration')
#######################################################################################
setting('start2.gcode', """;Sliced at: {day} {date} {time}
;Basic settings: Layer height: {layer_height} Walls: {wall_thickness} Fill: {fill_density}
;Print time: {print_time}
;Filament used: {filament_amount}m {filament_weight}g
;Filament cost: {filament_cost}
G21        ;metric values
G90        ;absolute positioning
M107       ;start with the fan off

G28 X0 Y0  ;move X/Y to min endstops
G28 Z0     ;move Z to min endstops

G1 Z15.0 F{travel_speed} ;move the platform down 15mm

T1
G92 E0                  ;zero the extruded length
G1 F200 E10             ;extrude 10mm of feed stock
G92 E0                  ;zero the extruded length again
G1 F200 E-{retraction_dual_amount}

T0
G92 E0                  ;zero the extruded length
G1 F200 E10              ;extrude 10mm of feed stock
G92 E0                  ;zero the extruded length again
G1 F{travel_speed}
M117 Printing...
""", str, 'alteration', 'alteration')
#######################################################################################
setting('end2.gcode', """;End GCode
M104 T0 S0                     ;extruder heater off
M104 T1 S0                     ;extruder heater off
M140 S0                     ;heated bed heater off (if you have it)

G91                                    ;relative positioning
G1 E-1 F300                            ;retract the filament a bit before lifting the nozzle, to release some of the pressure
G1 Z+0.5 E-5 X-20 Y-20 F{travel_speed} ;move Z up a bit and retract filament even more
G28 X0 Y0                              ;move X/Y to min endstops, so the head is out of the way

M84                         ;steppers off
G90                         ;absolute positioning
""", str, 'alteration', 'alteration')
#######################################################################################
setting('support_start.gcode', '', str, 'alteration', 'alteration')
setting('support_end.gcode', '', str, 'alteration', 'alteration')
setting('cool_start.gcode', '', str, 'alteration', 'alteration')
setting('cool_end.gcode', '', str, 'alteration', 'alteration')
setting('replace.csv', '', str, 'alteration', 'alteration')
#######################################################################################
setting('nextobject.gcode', """;Move to next object on the platform. clear_z is the minimal z height we need to make sure we do not hit any objects.
G92 E0

G91                                    ;relative positioning
G1 E-1 F300                            ;retract the filament a bit before lifting the nozzle, to release some of the pressure
G1 Z+0.5 E-5 F{travel_speed}           ;move Z up a bit and retract filament even more
G90                                    ;absolute positioning

G1 Z{clear_z} F{max_z_speed}
G92 E0
G1 X{object_center_x} Y{object_center_y} F{travel_speed}
G1 F200 E6
G92 E0
""", str, 'alteration', 'alteration')
#######################################################################################
setting('switchExtruder.gcode', """;Switch between the current extruder and the next extruder, when printing with multiple extruders.
G92 E0
G1 E-36 F5000
G92 E0
T{extruder}
G1 X{new_x} Y{new_y} Z{new_z} F{travel_speed}
G1 E36 F5000
G92 E0
""", str, 'alteration', 'alteration')

setting('startMode', 'Simple', ['Simple', 'Normal'], 'preference', 'hidden')
setting('lastFile', os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'resources', 'example', 'UltimakerRobot_support.stl')), str, 'preference', 'hidden')
setting('machine_width', '205', float, 'preference', 'hidden').setLabel('最大打印宽度 (mm)', '打印尺寸，以毫米计。')
setting('machine_depth', '205', float, 'preference', 'hidden').setLabel('最大打印深度 (mm)', '打印尺寸，以毫米计。')
setting('machine_height', '200', float, 'preference', 'hidden').setLabel('最大打印高度 (mm)', '打印尺寸，以毫米计。')
setting('machine_type', 'unknown', str, 'preference', 'hidden')
setting('machine_center_is_zero', 'False', bool, 'preference', 'hidden')
setting('ultimaker_extruder_upgrade', 'False', bool, 'preference', 'hidden')
setting('has_heated_bed', 'False', bool, 'preference', 'hidden').setLabel('加热平台', '如有加热平台，请勾选此项（需要重启）。')
setting('reprap_name', 'RepRap', str, 'preference', 'hidden')
setting('extruder_amount', '1', ['1','2','3','4'], 'preference', 'hidden').setLabel('喷头数', '打印机喷头数量。')
setting('extruder_offset_x1', '-21.6', float, 'preference', 'hidden').setLabel('X轴偏移', '相对于主喷头在X轴方向的偏移。')
setting('extruder_offset_y1', '0.0', float, 'preference', 'hidden').setLabel('Y轴偏移', '相对于主喷头在Y轴方向的偏移。')
setting('extruder_offset_x2', '0.0', float, 'preference', 'hidden').setLabel('X轴偏移', '相对于主喷头在X轴方向的偏移。')
setting('extruder_offset_y2', '0.0', float, 'preference', 'hidden').setLabel('Y轴偏移', '相对于主喷头在Y轴方向的偏移。')
setting('extruder_offset_x3', '0.0', float, 'preference', 'hidden').setLabel('X轴偏移', '相对于主喷头在X轴方向的偏移。')
setting('extruder_offset_y3', '0.0', float, 'preference', 'hidden').setLabel('Y轴偏移', '相对于主喷头在Y轴方向的偏移。')
setting('filament_physical_density', '1240', float, 'preference', 'hidden').setRange(500.0, 3000.0).setLabel('密度 (kg/m3)', '每立方米材料的重量。PLA大约是1250，ABS是1040左右。这个值是用于估测打印材料的重量。')
setting('steps_per_e', '0', float, 'preference', 'hidden').setLabel('E-Steps值', '每毫米丝料挤出步进数，假如设置为0，则该值会被忽略并直接使用你固件中的值。')
setting('serial_port', 'AUTO', str, 'preference', 'hidden').setLabel('串口号', '打印机通信串口号。')
setting('serial_port_auto', '', str, 'preference', 'hidden')
setting('serial_baud', 'AUTO', str, 'preference', 'hidden').setLabel('波特率', '匹配固件设定的波特率，\n通常数值为250000，115200，57600。')
setting('serial_baud_auto', '', int, 'preference', 'hidden')
setting('save_profile', 'False', bool, 'preference', 'hidden').setLabel('Save profile on slice', 'When slicing save the profile as [stl_file]_profile.ini next to the model.')
setting('filament_cost_kg', '0', float, 'preference', 'hidden').setLabel('成本 (price/kg)', '每千克材料的费，用来估计最终打印的花费。')
setting('filament_cost_meter', '0', float, 'preference', 'hidden').setLabel('成本 (price/m)', '每米材料的费，用来估计最终打印的花费。')
setting('auto_detect_sd', 'True', bool, 'preference', 'hidden').setLabel('自动检测SD卡', '自动检测SD卡。如果在一些系统中外置硬盘和u盘被认为是SD卡，可取消该选项。')
setting('check_for_updates', 'True', bool, 'preference', 'hidden').setLabel('检查更新', '在启动时检测到更新的Cura版本。')
setting('submit_slice_information', 'False', bool, 'preference', 'hidden').setLabel('发送使用的统计信息', '发送匿名的使用信息来改善下个Cura版本。')

setting('extruder_head_size_min_x', '75.0', float, 'preference', 'hidden').setLabel('打印头X轴左边距 (mm)', '打印多个物件时，从喷嘴顶端到风扇左边框的距离。\n风扇位于左边的时候，在Ultimaker和DreamMaker上使用的是75mm。')
setting('extruder_head_size_min_y', '18.0', float, 'preference', 'hidden').setLabel('打印头Y轴下边距 (mm)', '打印多个物件时，从喷嘴顶端到打印头到Y轴下边框的距离。\n风扇位于左边的时候，在Ultimaker和DreamMaker上使用的是18mm。')
setting('extruder_head_size_max_x', '18.0', float, 'preference', 'hidden').setLabel('打印头X轴右边距(mm)', '打印多个物件时，从喷嘴顶端到打印头到x轴右边框的距离。\n风扇位于左边的时候，在Ultimaker和DreamMaker上使用的是18mm。')
setting('extruder_head_size_max_y', '35.0', float, 'preference', 'hidden').setLabel('打印头Y轴上边距 (mm)', '打印多个物件时，从喷嘴顶端到打印头到Y轴上边框的距离。\n风扇位于左边的时候，在Ultimaker和DreamMaker上使用的是35mm。')
setting('extruder_head_size_height', '60.0', float, 'preference', 'hidden').setLabel('打印头机架高度 (mm)', '打印头机架光杆高度，若物体超过此高度就不能依次单独打印多个物体。\n在Ultimaker和DreamMaker上使用的是60mm。')

setting('model_colour', '#7AB645', str, 'preference', 'hidden').setLabel('模型颜色')
setting('model_colour2', '#CB3030', str, 'preference', 'hidden').setLabel('模型颜色 (2)')
setting('model_colour3', '#DDD93C', str, 'preference', 'hidden').setLabel('模型颜色 (3)')
setting('model_colour4', '#4550D3', str, 'preference', 'hidden').setLabel('模型颜色 (4)')

setting('window_maximized', 'True', bool, 'preference', 'hidden')
setting('window_pos_x', '-1', float, 'preference', 'hidden')
setting('window_pos_y', '-1', float, 'preference', 'hidden')
setting('window_width', '-1', float, 'preference', 'hidden')
setting('window_height', '-1', float, 'preference', 'hidden')
setting('window_normal_sash', '320', float, 'preference', 'hidden')

validators.warningAbove(settingsDictionary['layer_height'], lambda : (float(getProfileSetting('nozzle_size')) * 80.0 / 100.0), "层厚超过 %.2fmm (80%% 喷头直径) 通常效果较差，不推荐使用")
validators.wallThicknessValidator(settingsDictionary['wall_thickness'])
validators.warningAbove(settingsDictionary['print_speed'], 150.0, "如果您的打印机没有经过仔细优化，强烈建议打印速度不要超过150mm/s")
validators.printSpeedValidator(settingsDictionary['print_speed'])
validators.warningAbove(settingsDictionary['print_temperature'], 260.0, "超过260℃可能会损坏您的打印机，请小心设定!")
validators.warningAbove(settingsDictionary['print_temperature2'], 260.0, "超过260℃可能会损坏您的打印机，请小心设定!")
validators.warningAbove(settingsDictionary['print_temperature3'], 260.0, "超过260℃可能会损坏您的打印机，请小心设定!")
validators.warningAbove(settingsDictionary['print_temperature4'], 260.0, "超过260℃可能会损坏您的打印机，请小心设定!")
validators.warningAbove(settingsDictionary['filament_diameter'], 3.5, "您确定您的丝料直径有那么大吗？普通的材料应该在3mm或者1.75mm左右！")
validators.warningAbove(settingsDictionary['filament_diameter2'], 3.5, "您确定您的丝料直径有那么大吗？普通的材料应该在3mm或者1.75mm左右！")
validators.warningAbove(settingsDictionary['filament_diameter3'], 3.5, "您确定您的丝料直径有那么大吗？普通的材料应该在3mm或者1.75mm左右！")
validators.warningAbove(settingsDictionary['filament_diameter4'], 3.5, "您确定您的丝料直径有那么大吗？普通的材料应该在3mm或者1.75mm左右！")
validators.warningAbove(settingsDictionary['travel_speed'], 300.0, "如果您的打印机没有经过仔细优化，强烈建议打印速度不要超过300mm/s")
validators.warningAbove(settingsDictionary['bottom_thickness'], lambda : (float(getProfileSetting('nozzle_size')) * 3.0 / 4.0), "底层超过 %.2fmm (3/4 喷头直径) 通常效果较差，不推荐使用。")

#Conditions for multiple extruders
settingsDictionary['print_temperature2'].addCondition(lambda : int(getPreference('extruder_amount')) > 1)
settingsDictionary['print_temperature3'].addCondition(lambda : int(getPreference('extruder_amount')) > 2)
settingsDictionary['print_temperature4'].addCondition(lambda : int(getPreference('extruder_amount')) > 3)
settingsDictionary['filament_diameter2'].addCondition(lambda : int(getPreference('extruder_amount')) > 1)
settingsDictionary['filament_diameter3'].addCondition(lambda : int(getPreference('extruder_amount')) > 2)
settingsDictionary['filament_diameter4'].addCondition(lambda : int(getPreference('extruder_amount')) > 3)
settingsDictionary['support_dual_extrusion'].addCondition(lambda : int(getPreference('extruder_amount')) > 1)
settingsDictionary['retraction_dual_amount'].addCondition(lambda : int(getPreference('extruder_amount')) > 1)
#Heated bed
settingsDictionary['print_bed_temperature'].addCondition(lambda : getPreference('has_heated_bed') == 'True')

#########################################################
## Profile and preferences functions
#########################################################

def getSubCategoriesFor(category):
	done = {}
	ret = []
	for s in settingsList:
		if s.getCategory() == category and not s.getSubCategory() in done:
			done[s.getSubCategory()] = True
			ret.append(s.getSubCategory())
	return ret

def getSettingsForCategory(category, subCategory = None):
	ret = []
	for s in settingsList:
		if s.getCategory() == category and (subCategory is None or s.getSubCategory() == subCategory):
			ret.append(s)
	return ret

## Profile functions
def getBasePath():
	if platform.system() == "Windows":
		basePath = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
		#If we have a frozen python install, we need to step out of the library.zip
		if hasattr(sys, 'frozen'):
			basePath = os.path.normpath(os.path.join(basePath, ".."))
	else:
		basePath = os.path.expanduser('~/.cura/%s' % version.getVersion(False))
	if not os.path.isdir(basePath):
		os.makedirs(basePath)
	return basePath

def getAlternativeBasePaths():
	paths = []
	basePath = os.path.normpath(os.path.join(getBasePath(), '..'))
	for subPath in os.listdir(basePath):
		path = os.path.join(basePath, subPath)
		if os.path.isdir(path) and os.path.isfile(os.path.join(path, 'preferences.ini')) and path != getBasePath():
			paths.append(path)
		path = os.path.join(basePath, subPath, 'Cura')
		if os.path.isdir(path) and os.path.isfile(os.path.join(path, 'preferences.ini')) and path != getBasePath():
			paths.append(path)
	return paths

def getDefaultProfilePath():
	return os.path.join(getBasePath(), 'current_profile.ini')

def loadProfile(filename):
	#Read a configuration file as global config
	profileParser = ConfigParser.ConfigParser()
	try:
		profileParser.read(filename)
	except ConfigParser.ParsingError:
		return
	global settingsList
	for set in settingsList:
		if set.isPreference():
			continue
		section = 'profile'
		if set.isAlteration():
			section = 'alterations'
		if profileParser.has_option(section, set.getName()):
			set.setValue(unicode(profileParser.get(section, set.getName()), 'utf-8', 'replace'))

def saveProfile(filename):
	#Save the current profile to an ini file
	profileParser = ConfigParser.ConfigParser()
	profileParser.add_section('profile')
	profileParser.add_section('alterations')
	global settingsList
	for set in settingsList:
		if set.isPreference():
			continue
		if set.isAlteration():
			profileParser.set('alterations', set.getName(), set.getValue().encode('utf-8'))
		else:
			profileParser.set('profile', set.getName(), set.getValue().encode('utf-8'))

	profileParser.write(open(filename, 'w'))

def resetProfile():
	#Read a configuration file as global config
	global settingsList
	for set in settingsList:
		if set.isPreference():
			continue
		set.setValue(set.getDefault())

	if getPreference('machine_type') == 'ultimaker':
		putProfileSetting('nozzle_size', '0.4')
		if getPreference('ultimaker_extruder_upgrade') == 'True':
			putProfileSetting('retraction_enable', 'True')
	else:
		putProfileSetting('nozzle_size', '0.5')

def loadProfileFromString(options):
	options = base64.b64decode(options)
	options = zlib.decompress(options)
	(profileOpts, alt) = options.split('\f', 1)
	global settingsDictionary
	for option in profileOpts.split('\b'):
		if len(option) > 0:
			(key, value) = option.split('=', 1)
			if key in settingsDictionary:
				if settingsDictionary[key].isProfile():
					settingsDictionary[key].setValue(value)
	for option in alt.split('\b'):
		if len(option) > 0:
			(key, value) = option.split('=', 1)
			if key in settingsDictionary:
				if settingsDictionary[key].isAlteration():
					settingsDictionary[key].setValue(value)

def getProfileString():
	p = []
	alt = []
	global settingsList
	for set in settingsList:
		if set.isProfile():
			if set.getName() in tempOverride:
				p.append(set.getName() + "=" + tempOverride[set.getName()])
			else:
				p.append(set.getName() + "=" + set.getValue())
		if set.isAlteration():
			if set.getName() in tempOverride:
				alt.append(set.getName() + "=" + tempOverride[set.getName()])
			else:
				alt.append(set.getName() + "=" + set.getValue())
	ret = '\b'.join(p) + '\f' + '\b'.join(alt)
	ret = base64.b64encode(zlib.compress(ret, 9))
	return ret

def getGlobalPreferencesString():
	p = []
	global settingsList
	for set in settingsList:
		if set.isPreference():
			p.append(set.getName() + "=" + set.getValue())
	ret = '\b'.join(p)
	ret = base64.b64encode(zlib.compress(ret, 9))
	return ret


def getProfileSetting(name):
	if name in tempOverride:
		return tempOverride[name]
	global settingsDictionary
	if name in settingsDictionary and settingsDictionary[name].isProfile():
		return settingsDictionary[name].getValue()
	print 'Error: "%s" not found in profile settings' % (name)
	return ''

def getProfileSettingFloat(name):
	try:
		setting = getProfileSetting(name).replace(',', '.')
		return float(eval(setting, {}, {}))
	except:
		return 0.0

def putProfileSetting(name, value):
	#Check if we have a configuration file loaded, else load the default.
	global settingsDictionary
	if name in settingsDictionary and settingsDictionary[name].isProfile():
		settingsDictionary[name].setValue(value)

def isProfileSetting(name):
	global settingsDictionary
	if name in settingsDictionary and settingsDictionary[name].isProfile():
		return True
	return False

## Preferences functions
def getPreferencePath():
	return os.path.join(getBasePath(), 'preferences.ini')

def getPreferenceFloat(name):
	try:
		setting = getPreference(name).replace(',', '.')
		return float(eval(setting, {}, {}))
	except:
		return 0.0

def getPreferenceColour(name):
	colorString = getPreference(name)
	return [float(int(colorString[1:3], 16)) / 255, float(int(colorString[3:5], 16)) / 255, float(int(colorString[5:7], 16)) / 255, 1.0]

def loadPreferences(filename):
	#Read a configuration file as global config
	profileParser = ConfigParser.ConfigParser()
	try:
		profileParser.read(filename)
	except ConfigParser.ParsingError:
		return
	global settingsList
	for set in settingsList:
		if set.isPreference():
			if profileParser.has_option('preference', set.getName()):
				set.setValue(unicode(profileParser.get('preference', set.getName()), 'utf-8', 'replace'))

def savePreferences(filename):
	#Save the current profile to an ini file
	parser = ConfigParser.ConfigParser()
	parser.add_section('preference')
	global settingsList
	for set in settingsList:
		if set.isPreference():
			parser.set('preference', set.getName(), set.getValue().encode('utf-8'))
	parser.write(open(filename, 'w'))

def getPreference(name):
	if name in tempOverride:
		return tempOverride[name]
	global settingsDictionary
	if name in settingsDictionary and settingsDictionary[name].isPreference():
		return settingsDictionary[name].getValue()
	print 'Error: "%s" not found in profile settings' % (name)
	return ''

def putPreference(name, value):
	#Check if we have a configuration file loaded, else load the default.
	global settingsDictionary
	if name in settingsDictionary and settingsDictionary[name].isPreference():
		settingsDictionary[name].setValue(value)
	savePreferences(getPreferencePath())

def isPreference(name):
	global settingsDictionary
	if name in settingsDictionary and settingsDictionary[name].isPreference():
		return True
	return False

## Temp overrides for multi-extruder slicing and the project planner.
tempOverride = {}
def setTempOverride(name, value):
	tempOverride[name] = unicode(value).encode("utf-8")
def clearTempOverride(name):
	del tempOverride[name]
def resetTempOverride():
	tempOverride.clear()

#########################################################
## Utility functions to calculate common profile values
#########################################################
def calculateEdgeWidth():
	wallThickness = getProfileSettingFloat('wall_thickness')
	nozzleSize = getProfileSettingFloat('nozzle_size')

	if wallThickness < 0.01:
		return nozzleSize
	if wallThickness < nozzleSize:
		return wallThickness

	lineCount = int(wallThickness / nozzleSize + 0.0001)
	lineWidth = wallThickness / lineCount
	lineWidthAlt = wallThickness / (lineCount + 1)
	if lineWidth > nozzleSize * 1.5:
		return lineWidthAlt
	return lineWidth

def calculateLineCount():
	wallThickness = getProfileSettingFloat('wall_thickness')
	nozzleSize = getProfileSettingFloat('nozzle_size')

	if wallThickness < 0.01:
		return 0
	if wallThickness < nozzleSize:
		return 1

	lineCount = int(wallThickness / nozzleSize + 0.0001)
	lineWidth = wallThickness / lineCount
	lineWidthAlt = wallThickness / (lineCount + 1)
	if lineWidth > nozzleSize * 1.5:
		return lineCount + 1
	return lineCount

def calculateSolidLayerCount():
	layerHeight = getProfileSettingFloat('layer_height')
	solidThickness = getProfileSettingFloat('solid_layer_thickness')
	if layerHeight == 0.0:
		return 1
	return int(math.ceil(solidThickness / layerHeight - 0.0001))

def calculateObjectSizeOffsets():
	size = 0.0

	if getProfileSetting('platform_adhesion') == 'Brim':
		size += getProfileSettingFloat('brim_line_count') * calculateEdgeWidth()
	elif getProfileSetting('platform_adhesion') == 'Raft':
		pass
	else:
		if getProfileSettingFloat('skirt_line_count') > 0:
			size += getProfileSettingFloat('skirt_line_count') * calculateEdgeWidth() + getProfileSettingFloat('skirt_gap')

	#if getProfileSetting('enable_raft') != 'False':
	#	size += profile.getProfileSettingFloat('raft_margin') * 2
	#if getProfileSetting('support') != 'None':
	#	extraSizeMin = extraSizeMin + numpy.array([3.0, 0, 0])
	#	extraSizeMax = extraSizeMax + numpy.array([3.0, 0, 0])
	return [size, size]

def getMachineCenterCoords():
	if getPreference('machine_center_is_zero') == 'True':
		return [0, 0]
	return [getPreferenceFloat('machine_width') / 2, getPreferenceFloat('machine_depth') / 2]

#########################################################
## Alteration file functions
#########################################################
def replaceTagMatch(m):
	pre = m.group(1)
	tag = m.group(2)
	if tag == 'time':
		return pre + time.strftime('%H:%M:%S').encode('utf-8', 'replace')
	if tag == 'date':
		return pre + time.strftime('%d %b %Y').encode('utf-8', 'replace')
	if tag == 'day':
		return pre + time.strftime('%a').encode('utf-8', 'replace')
	if tag == 'print_time':
		return pre + '#P_TIME#'
	if tag == 'filament_amount':
		return pre + '#F_AMNT#'
	if tag == 'filament_weight':
		return pre + '#F_WGHT#'
	if tag == 'filament_cost':
		return pre + '#F_COST#'
	if pre == 'F' and tag in ['print_speed', 'retraction_speed', 'travel_speed', 'max_z_speed', 'bottom_layer_speed', 'cool_min_feedrate']:
		f = getProfileSettingFloat(tag) * 60
	elif isProfileSetting(tag):
		f = getProfileSettingFloat(tag)
	elif isPreference(tag):
		f = getProfileSettingFloat(tag)
	else:
		return '%s?%s?' % (pre, tag)
	if (f % 1) == 0:
		return pre + str(int(f))
	return pre + str(f)

def replaceGCodeTags(filename, gcodeInt):
	f = open(filename, 'r+')
	data = f.read(2048)
	data = data.replace('#P_TIME#', ('%5d:%02d' % (int(gcodeInt.totalMoveTimeMinute / 60), int(gcodeInt.totalMoveTimeMinute % 60)))[-8:])
	data = data.replace('#F_AMNT#', ('%8.2f' % (gcodeInt.extrusionAmount / 1000))[-8:])
	data = data.replace('#F_WGHT#', ('%8.2f' % (gcodeInt.calculateWeight() * 1000))[-8:])
	cost = gcodeInt.calculateCost()
	if cost is None:
		cost = 'Unknown'
	data = data.replace('#F_COST#', ('%8s' % (cost.split(' ')[0]))[-8:])
	f.seek(0)
	f.write(data)
	f.close()

### Get aleration raw contents. (Used internally in Cura)
def getAlterationFile(filename):
	if filename in tempOverride:
		return tempOverride[filename]
	global settingsDictionary
	if filename in settingsDictionary and settingsDictionary[filename].isAlteration():
		return settingsDictionary[filename].getValue()
	print 'Error: "%s" not found in profile settings' % (filename)
	return ''

def setAlterationFile(name, value):
	#Check if we have a configuration file loaded, else load the default.
	global settingsDictionary
	if name in settingsDictionary and settingsDictionary[name].isAlteration():
		settingsDictionary[name].setValue(value)
	saveProfile(getDefaultProfilePath())

### Get the alteration file for output. (Used by Skeinforge)
def getAlterationFileContents(filename, extruderCount = 1):
	prefix = ''
	postfix = ''
	alterationContents = getAlterationFile(filename)
	if filename == 'start.gcode':
		if extruderCount > 1:
			alterationContents = getAlterationFile("start%d.gcode" % (extruderCount))
		#For the start code, hack the temperature and the steps per E value into it. So the temperature is reached before the start code extrusion.
		#We also set our steps per E here, if configured.
		eSteps = getPreferenceFloat('steps_per_e')
		if eSteps > 0:
			prefix += 'M92 E%f\n' % (eSteps)
		temp = getProfileSettingFloat('print_temperature')
		bedTemp = 0
		if getPreference('has_heated_bed') == 'True':
			bedTemp = getProfileSettingFloat('print_bed_temperature')
		
		if bedTemp > 0 and not '{print_bed_temperature}' in alterationContents:
			prefix += 'M140 S%f\n' % (bedTemp)
		if temp > 0 and not '{print_temperature}' in alterationContents:
			if extruderCount > 0:
				for n in xrange(1, extruderCount):
					t = temp
					if n > 0 and getProfileSettingFloat('print_temperature%d' % (n+1)) > 0:
						t = getProfileSettingFloat('print_temperature%d' % (n+1))
					prefix += 'M104 T%d S%f\n' % (n, t)
				for n in xrange(0, extruderCount):
					t = temp
					if n > 0 and getProfileSettingFloat('print_temperature%d' % (n+1)) > 0:
						t = getProfileSettingFloat('print_temperature%d' % (n+1))
					prefix += 'M109 T%d S%f\n' % (n, t)
				prefix += 'T0\n'
			else:
				prefix += 'M109 S%f\n' % (temp)
		if bedTemp > 0 and not '{print_bed_temperature}' in alterationContents:
			prefix += 'M190 S%f\n' % (bedTemp)
	elif filename == 'end.gcode':
		if extruderCount > 1:
			alterationContents = getAlterationFile("end%d.gcode" % (extruderCount))
		#Append the profile string to the end of the GCode, so we can load it from the GCode file later.
		postfix = ';CURA_PROFILE_STRING:%s\n' % (getProfileString())
	elif filename == 'replace.csv':
		#Always remove the extruder on/off M codes. These are no longer needed in 5D printing.
		prefix = 'M101\nM103\n'
	elif filename == 'support_start.gcode' or filename == 'support_end.gcode':
		#Add support start/end code 
		if getProfileSetting('support_dual_extrusion') == 'True' and int(getPreference('extruder_amount')) > 1:
			if filename == 'support_start.gcode':
				setTempOverride('extruder', '1')
			else:
				setTempOverride('extruder', '0')
			alterationContents = getAlterationFileContents('switchExtruder.gcode')
			clearTempOverride('extruder')
		else:
			alterationContents = ''
	return unicode(prefix + re.sub("(.)\{([^\}]*)\}", replaceTagMatch, alterationContents).rstrip() + '\n' + postfix).strip().encode('utf-8') + '\n'

###### PLUGIN #####

def getPluginConfig():
	try:
		return pickle.loads(str(getProfileSetting('plugin_config')))
	except:
		return []

def setPluginConfig(config):
	putProfileSetting('plugin_config', pickle.dumps(config))

def getPluginBasePaths():
	ret = []
	if platform.system() != "Windows":
		ret.append(os.path.expanduser('~/.cura/plugins/'))
	if platform.system() == "Darwin" and hasattr(sys, 'frozen'):
		ret.append(os.path.normpath(os.path.join(resources.resourceBasePath, "Cura/plugins")))
	else:
		ret.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'plugins')))
	return ret

def getPluginList():
	ret = []
	for basePath in getPluginBasePaths():
		for filename in glob.glob(os.path.join(basePath, '*.py')):
			filename = os.path.basename(filename)
			if filename.startswith('_'):
				continue
			with open(os.path.join(basePath, filename), "r") as f:
				item = {'filename': filename, 'name': None, 'info': None, 'type': None, 'params': []}
				for line in f:
					line = line.strip()
					if not line.startswith('#'):
						break
					line = line[1:].split(':', 1)
					if len(line) != 2:
						continue
					if line[0].upper() == 'NAME':
						item['name'] = line[1].strip()
					elif line[0].upper() == 'INFO':
						item['info'] = line[1].strip()
					elif line[0].upper() == 'TYPE':
						item['type'] = line[1].strip()
					elif line[0].upper() == 'DEPEND':
						pass
					elif line[0].upper() == 'PARAM':
						m = re.match('([a-zA-Z][a-zA-Z0-9_]*)\(([a-zA-Z_]*)(?::([^\)]*))?\) +(.*)', line[1].strip())
						if m is not None:
							item['params'].append({'name': m.group(1), 'type': m.group(2), 'default': m.group(3), 'description': m.group(4)})
					else:
						print "Unknown item in effect meta data: %s %s" % (line[0], line[1])
				if item['name'] is not None and item['type'] == 'postprocess':
					ret.append(item)
	return ret

def runPostProcessingPlugins(gcodefilename):
	pluginConfigList = getPluginConfig()
	pluginList = getPluginList()

	for pluginConfig in pluginConfigList:
		plugin = None
		for pluginTest in pluginList:
			if pluginTest['filename'] == pluginConfig['filename']:
				plugin = pluginTest
		if plugin is None:
			continue
		
		pythonFile = None
		for basePath in getPluginBasePaths():
			testFilename = os.path.join(basePath, pluginConfig['filename'])
			if os.path.isfile(testFilename):
				pythonFile = testFilename
		if pythonFile is None:
			continue
		
		locals = {'filename': gcodefilename}
		for param in plugin['params']:
			value = param['default']
			if param['name'] in pluginConfig['params']:
				value = pluginConfig['params'][param['name']]
			
			if param['type'] == 'float':
				try:
					value = float(value)
				except:
					value = float(param['default'])
			
			locals[param['name']] = value
		try:
			execfile(pythonFile, locals)
		except:
			locationInfo = traceback.extract_tb(sys.exc_info()[2])[-1]
			return "%s: '%s' @ %s:%s:%d" % (str(sys.exc_info()[0].__name__), str(sys.exc_info()[1]), os.path.basename(locationInfo[0]), locationInfo[2], locationInfo[1])
	return None
