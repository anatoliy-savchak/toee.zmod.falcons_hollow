import toee, utils_npc, utils_obj, ctrl_behaviour, const_toee, utils_storage
import py07710_skirmish_harbinger_monsters

def menu_get_commander_dict():
	#result = {title: (class, order)}
	result = {}
	if (1):
		i = -1
		for c in py07710_skirmish_harbinger_monsters.get_character_classes():
			assert isinstance(c, py07710_skirmish_harbinger_monsters.CtrlSkirmisher)
			i += 1
			commander_level = c.get_commander_level()
			if (commander_level <= 0): continue

			result[menu_get_commander_title(c)] = (c, i)
	return result

def menu_get_compatible_creatures_dict():
	result = {}
	all = []
	if (1):
		i = -1
		for c in py07710_skirmish_harbinger_monsters.get_character_classes():
			assert isinstance(c, py07710_skirmish_harbinger_monsters.CtrlSkirmisher)
			i += 1
			commander_level = c.get_commander_level()
			if (commander_level > 0): continue

			all.append((c, i))

	if (all):
		commanders = []
		for pc in toee.game.party:
			ctrl = critter_is_commander(pc)
			if not ctrl: continue
			commanders.append((pc, ctrl))

		if commanders:
			for t in all:
				compatible = 0
				c = t[0]
				for ct in commanders:
					if critter_ctrl_is_compatible_with_commander(c, ct[1]):
						compatible = 1
						break
				if (compatible):
					result[menu_get_creature_title(c)] = t
	return result

def menu_get_creature_title(c):
	assert isinstance(c, py07710_skirmish_harbinger_monsters.CtrlSkirmisher)
	alignment = c.get_alignment_group()
	al_str = utils_npc.get_alignment_short(alignment)
	title = c.get_title()
	price = c.get_price()
	text = "{} {}. Cost: {}".format(al_str, title, price)
	return text

def menu_get_commander_title(c):
	assert isinstance(c, py07710_skirmish_harbinger_monsters.CtrlSkirmisher)
	commander_level = c.get_commander_level()
	alignment = c.get_alignment_group()
	al_str = utils_npc.get_alignment_short(alignment)
	title = c.get_title()
	price = c.get_price()
	text = "{} {} (Cmdr {}). Cost: {}".format(al_str, title, commander_level, price)
	return text

def menu_commander_place_click(class_id):
	assert isinstance(class_id, int)
	# create commander
	# remove incompatible

	c = py07710_skirmish_harbinger_monsters.get_character_classes()[class_id]
	assert isinstance(c, py07710_skirmish_harbinger_monsters.CtrlSkirmisher)

	skirmish_settings = skirmish_settings_get()
	if (skirmish_settings.points_left < c.get_price()):
		return "Insufficient points {} left to buy this commander, cost: {}".format(skirmish_settings.points_left, c.get_price())

	# check if same commander already exists
	for pc in toee.game.party:
		ctrl = critter_is_commander(pc)
		if not ctrl: continue
		if (ctrl.__class__ == c):
			return "Commanders cannot be duplicated!"

	npc, ctrl = c.create_obj_and_class(utils_obj.sec2loc(478, 480), 1, 1)
	npc.condition_add("SkirmisherStart")
	npc.rotation = const_toee.rotation_0600_oclock
	added = toee.game.leader.pc_add(npc)

	warband_clear_incompatible(npc, ctrl)

	if (get_commander_count() == 1):
		skirmish_settings.faction_alignment = ctrl.get_alignment_group()
	return None # no error

def menu_creature_place_click(class_id):
	assert isinstance(class_id, int)
	# create creature

	c = py07710_skirmish_harbinger_monsters.get_character_classes()[class_id]
	assert isinstance(c, py07710_skirmish_harbinger_monsters.CtrlSkirmisher)

	skirmish_settings = skirmish_settings_get()
	if (skirmish_settings.points_left < c.get_price()):
		return "Insufficient points {} left to buy this creature, cost: {}".format(skirmish_settings.points_left, c.get_price())

	# check if compatible
	if (1):
		commanders = []
		for pc in toee.game.party:
			ctrl = critter_is_commander(pc)
			if not ctrl: continue
			commanders.append((pc, ctrl))

		if commanders:
			compatible = False
			for ct in commanders:
				if critter_ctrl_is_compatible_with_commander(c, ct[1]):
					compatible = True
					break
			if not compatible:
				return "{} is incompatible with any Commanders!".format(ctrl.get_title())

	npc, ctrl = c.create_obj_and_class(utils_obj.sec2loc(478, 480), 1, 1)
	npc.condition_add("SkirmisherStart")
	npc.rotation = const_toee.rotation_0600_oclock
	added = toee.game.leader.pc_add(npc)

	warband_recalc_points()
	return None # no error

def critter_is_compatible_with_skirmishing(critter): # -> ctrl
	assert isinstance(critter, toee.PyObjHandle)
	critter_ctrl = ctrl_behaviour.get_ctrl(critter.id)

	if (critter_ctrl is None): 
		print("critter_ctrl is None for {}, id: {}".format(critter, critter.id))
		return None
	if not issubclass(critter_ctrl.__class__, py07710_skirmish_harbinger_monsters.CtrlSkirmisher): 
		print("not issubclass(critter_ctrl.__class__(), py07710_skirmish_harbinger_monsters.CtrlSkirmisher) {} for {}".format(critter_ctrl, critter))
		return None
	assert isinstance(critter_ctrl, py07710_skirmish_harbinger_monsters.CtrlSkirmisher)
	return critter_ctrl

def critter_is_compatible_with_commander(critter, commander, commander_ctrl):
	assert isinstance(critter, toee.PyObjHandle)
	assert isinstance(commander, toee.PyObjHandle)
	assert isinstance(commander_ctrl, py07710_skirmish_harbinger_monsters.CtrlSkirmisher)

	if (critter == commander): return True

	critter_ctrl = critter_is_compatible_with_skirmishing(critter)
	if (critter_ctrl is None): return False

	return critter_ctrl_is_compatible_with_commander(critter_ctrl, commander_ctrl)

def critter_ctrl_is_compatible_with_commander(critter_ctrl, commander_ctrl):
	assert isinstance(critter_ctrl, py07710_skirmish_harbinger_monsters.CtrlSkirmisher)
	assert isinstance(commander_ctrl, py07710_skirmish_harbinger_monsters.CtrlSkirmisher)

	if (critter_ctrl.get_alignment_group() != commander_ctrl.get_alignment_group()): 
		print("critter_ctrl.get_alignment_group({}) != commander_ctrl.get_alignment_group({}) for {}".format(critter_ctrl.get_alignment_group(), commander_ctrl.get_alignment_group(), critter))
		return False
	return True

def critter_is_compatible_with_faction_alignment(critter, faction_alignment):
	assert isinstance(critter, toee.PyObjHandle)
	assert isinstance(faction_alignment, int)
	critter_ctrl = critter_is_compatible_with_skirmishing(critter)
	if (critter_ctrl is None): return False

	if (critter_ctrl.get_alignment_group() != faction_alignment): 
		print("critter_ctrl.get_alignment_group({}) != faction_alignment({}) for {}".format(critter_ctrl.get_alignment_group(), faction_alignment, critter))
		return False
	return True

def critter_is_commander(critter):
	assert isinstance(critter, toee.PyObjHandle)
	critter_ctrl = critter_is_compatible_with_skirmishing(critter)
	if (critter_ctrl is None): return None
	if (critter_ctrl.get_commander_level() > 0): return critter_ctrl
	return None

def warband_clear_incompatible(primary_commander = None, primary_commander_ctrl = None):
	assert isinstance(primary_commander, toee.PyObjHandle)
	assert isinstance(primary_commander_ctrl, py07710_skirmish_harbinger_monsters.CtrlSkirmisher)
	""" Remove all incompatible commanders to primary commander (if any) and then remove all incompatible creatures to all commanders"""

	# check commanders first
	if (primary_commander):
		for pc in toee.game.party:
			if not critter_is_commander(pc): continue
			if not critter_is_compatible_with_commander(pc, primary_commander, primary_commander_ctrl):
				print("PC is not compatible to any primary commander: {} | {}".format(pc, primary_commander))
				remove_pc(pc)

	# for each non commander check if critter is compatible with at least one commander
	for pc in toee.game.party:
		if critter_is_commander(pc): continue
		compatible = False
		for commander in toee.game.party:
			commander_ctrl = critter_is_commander(commander)
			if not commander_ctrl: continue
			if critter_is_compatible_with_commander(pc, commander, commander_ctrl):
				compatible = True
				break
		if (not compatible):
			print("PC is not compatible to any commander: {}".format(pc))
			remove_pc(pc)

	warband_recalc_points()
	return

def warband_recalc_points():
	total = 0
	for pc in toee.game.party:
		critter_ctrl = critter_is_compatible_with_skirmishing(pc)
		if not critter_ctrl: continue
		total += critter_ctrl.get_price()
	s = skirmish_settings_get()
	s.points_left = s.points_max - total
	return total

def remove_pc(pc):
	pc.obj_remove_from_all_groups(pc)
	pc.destroy()
	return

def get_commander_count():
	result = 0
	for pc in toee.game.party:
		if critter_is_commander(pc): result += 1
	return result

def skirmish_settings_get(recreate = 0):
	objectStorage = utils_storage.obj_storage_by_id("skirmish_settings")
	skirmish_settings = objectStorage.get_data("skirmish_settings")
	if (not skirmish_settings):
		skirmish_settings = SkirmishSettings()
		objectStorage.data["skirmish_settings"] = skirmish_settings
	assert isinstance(skirmish_settings, SkirmishSettings)
	return skirmish_settings

class SkirmishSettings(object):
	def __init__(self):
		self.faction_alignment = toee.ALIGNMENT_LAWFUL_GOOD
		self.points_max = 100
		self.points_left = self.points_max
		return

def menu_show_info_click():
	skirmish_settings = skirmish_settings_get()

	lines = []
	lines.append("Faction: {}. ".format(utils_npc.get_alignment_short(skirmish_settings.faction_alignment))\
	   + "Points: {} left out of {}".format(skirmish_settings.points_left, skirmish_settings.points_max))

	lines.append("")
	lines.append("Warband:")

	if (1):
		creatures = []
		for pc in toee.game.party:
			ctrl = critter_is_compatible_with_skirmishing(pc)
			if not ctrl: continue
			line = "{}, {}. Cost: {}".format(ctrl.get_title(), utils_npc.get_alignment_short(ctrl.get_alignment_group()), ctrl.get_price())
			creatures.append((line, ctrl.get_price()))

		if (creatures):
			i = 0
			for critter_tup in sorted(critters, reverse = False, key = lambda kv: kv[1]):
				lines.append("{}. {}".format(i, critter_tup[0]))

	result = "\n".join(lines)
	toee.game.alert_show(result, "Close")
	return

def menu_map_start_click(map_id):
	assert isinstance(map_id, int)
	toee.game.fade_and_teleport(0, 0, 0, map_id, 495, 506)
	return

def generate_enemies1(points, alignment_group):
	assert isinstance(points, int)
	assert isinstance(alignment_group, int)

	left = points
	result = []
	available_commanders = []
	available_critters = [] #(class, cost)
	if (1):
		for c in py07710_skirmish_harbinger_monsters.get_enemy_classes():
			assert isinstance(c, py07710_skirmish_harbinger_monsters.CtrlSkirmisher)
			if c.get_alignment_group() != alignment_group: continue
			commander_level = c.get_commander_level()
			if (commander_level > 0): 
				available_commanders.append((c, c.get_price()))
			else:
				available_critters.append((c, c.get_price()))
	
	if (not available_commanders): return result

	available_critters.sort(reverse = False, key = lambda kv: kv[1])

	primary_commander_class_t = available_commanders[toee.game.random_range(0, len(available_commanders)-1)]
	primary_commander_class = primary_commander_class_t[0]
	available_commanders.remove(primary_commander_class_t)
	left -= primary_commander_class_t[1]
	result.append(primary_commander_class)

	lowest_cost = available_critters[0][1]

	max_loop = 1000
	i = -1
	while (left > lowest_cost):
		i += 1
		if (i > max_loop): break
		if (left == lowest_cost):
			critter_class_t = available_critters[0]
		else:
			critter_class_t = available_critters[toee.game.random_range(0, len(available_critters)-1)]
			if (left - critter_class_t[1] < 0): continue
		left -= critter_class_t[1]
		result.append(critter_class_t[0])
	return result