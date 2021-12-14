import toee, utils_npc, utils_obj, ctrl_behaviour, const_toee
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
	# remove incompatible, for now everyone

	c = py07710_skirmish_harbinger_monsters.get_character_classes()[class_id]
	assert isinstance(c, py07710_skirmish_harbinger_monsters.CtrlSkirmisher)

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
	return None # no error

def critter_is_compatible_with_skirmishing(critter): # -> ctrl
	assert isinstance(critter, toee.PyObjHandle)
	critter_ctrl = ctrl_behaviour.get_ctrl(critter.id)

	if (critter_ctrl is None): 
		print("critter_ctrl is None for {}".format(critter))
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
	return

def remove_pc(pc):
	pc.obj_remove_from_all_groups(pc)
	pc.destroy()
	return