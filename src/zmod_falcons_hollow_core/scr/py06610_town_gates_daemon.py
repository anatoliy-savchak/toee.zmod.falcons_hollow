import toee, debug, utils_toee, utils_storage, utils_obj, utils_item, const_toee, ctrl_daemon, ctrl_daemon2
import ctrl_behaviour, py06122_cormyr_prompter, factions_zmod, utils_npc
import monster_info, module_quests, module_consts

DAEMON_SCRIPT_ID = 6610
DAEMON_GID = "G_44471338_B2A6_4FF7_A636_8D13F81C1B69"
DEBUG = 0
DEBUG_SKIP_C01 = 1
DEBUG_NAMES = 1

def san_new_map(attachee, triggerer):
	return ctrl_daemon2.do_san_new_map(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_TOWN_GATES, CtrlTownGates)

def san_first_heartbeat(attachee, triggerer):
	print(attachee.id)
	debug.breakp('')
	return ctrl_daemon2.do_san_first_heartbeat(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_TOWN_GATES, CtrlTownGates)

def san_heartbeat(attachee, triggerer):
	return ctrl_daemon2.do_san_heartbeat(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_TOWN_GATES, cs())

def san_dying(attachee, triggerer):
	return ctrl_daemon2.do_san_dying(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_TOWN_GATES, cs())

def san_use(attachee, triggerer):
	return ctrl_daemon2.do_san_use(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_TOWN_GATES, cs())

def san_bust(attachee, triggerer):
	return ctrl_daemon2.do_san_bust(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_TOWN_GATES, cs())

def cs():
	o = utils_storage.obj_storage_by_id(DAEMON_GID)
	if (not o): 
		return None
	result = o.data.get(CtrlTownGates.get_name())
	assert isinstance(result, CtrlTownGates)
	return result

class CtrlTownGates(ctrl_daemon2.CtrlDaemon2):
	def created(self, npc):
		self.init_daemon2_fields(module_consts.MAP_ID_ZMOD_D_TOWN_GATES, DAEMON_SCRIPT_ID, "town_gates")
		super(CtrlTownGates, self).created(npc)
		return

	def place_encounters_initial(self):
		#self.place_encounter_c03(self.delayed_mode())
		return

	def delayed_mode(self):
		return 1

	# Sleep interface
	def can_sleep(self):
		return toee.SLEEP_PASS_TIME_ONLY
