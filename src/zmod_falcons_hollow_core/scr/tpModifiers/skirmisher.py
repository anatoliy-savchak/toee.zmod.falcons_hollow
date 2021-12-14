import toee, templeplus.pymod, sys, tpdp, math, traceback, debug, debugg
import const_proto_weapon, const_proto_list_weapons, const_proto_list_weapons_masterwork, const_toee, const_proto_map_weapons, const_proto_map_armor, utils_pc, utils_obj
import json
import utils_skirmish, utils_npc

###################################################

def GetConditionName():
	return "SkirmisherStart"

print("Registering " + GetConditionName())
###################################################

PA_SKIRMISHER = 3022
def SkirmisherStart_OnBuildRadialMenuEntry(attachee, args, evt_obj):
	try:
		root = tpdp.RadialMenuEntryParent("Skirmish")
		root_id = root.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Class)

		party = tpdp.RadialMenuEntryParent("Warband")
		party_id = party.add_as_child(attachee, root_id)

		commander = tpdp.RadialMenuEntryParent("Commanders")
		commander_id = commander.add_as_child(attachee, party_id)

		commander_menu_dict = utils_skirmish.menu_get_commander_dict()
		for kv in sorted(commander_menu_dict.items(), reverse = False, key = lambda kv: kv[0]):
			title = kv[0]
			print(title)
			value = kv[1] #commander_menu_dict[title]
			tag = 1100 + value[1]
			item = tpdp.RadialMenuEntryPythonAction(title, toee.D20A_PYTHON_ACTION, PA_SKIRMISHER, tag, "TAG_INTERFACE_HELP")
			item_id = item.add_as_child(attachee, commander_id)

	except Exception, e:
		print "SkirmisherStart_OnBuildRadialMenuEntry:"
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60		
	return 0

def SkirmisherStart_OnD20PythonActionCheck(attachee, args, evt_obj):
	return 1

def SkirmisherStart_OnD20PythonActionPerform(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Action)
	#print("SkirmisherStart_OnD20PythonActionPerform start")
	try:
		def do_error_message(text):
			attachee.float_text_line(text, toee.tf_red)
			print(text)
			return

		tag = evt_obj.d20a.data1
		print("tag: {}".format(tag))
		if (tag >= 1100 and tag < 2000):
			error_msg = utils_skirmish.menu_commander_place_click(tag - 1100)
			if (error_msg):
				do_error_message(error_msg)
		else:
			do_error_message("Unknown tag: {}".format(tag))
	except Exception, e:
		print "SkirmisherStart_OnD20PythonActionPerform:"
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60		
	return 1


modObj = templeplus.pymod.PythonModifier(GetConditionName(), 3) # 
modObj.AddHook(toee.ET_OnBuildRadialMenuEntry, toee.EK_NONE, SkirmisherStart_OnBuildRadialMenuEntry, ())
modObj.AddHook(toee.ET_OnD20PythonActionCheck, PA_SKIRMISHER, SkirmisherStart_OnD20PythonActionCheck, ())
modObj.AddHook(toee.ET_OnD20PythonActionPerform, PA_SKIRMISHER, SkirmisherStart_OnD20PythonActionPerform, ())
