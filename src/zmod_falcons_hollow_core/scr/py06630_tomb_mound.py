import toee, debug, utils_toee, utils_storage, utils_obj, utils_item, const_toee, ctrl_daemon, ctrl_daemon2
import ctrl_behaviour, py06122_cormyr_prompter, factions_zmod, utils_npc
import monster_info, module_quests, module_consts, const_proto_sceneries

DAEMON_SCRIPT_ID = 6614
DAEMON_GID = "G_99937EEC_DAAD_476D_8346_09C9F0345275"
DEBUG = 0
DEBUG_NAMES = 1

def san_new_map(attachee, triggerer):
	return ctrl_daemon2.do_san_new_map(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_TOMB_MOUND, CtrlTombMound)

def san_first_heartbeat(attachee, triggerer):
	print(attachee.id)
	debug.breakp("")
	return ctrl_daemon2.do_san_first_heartbeat(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_TOMB_MOUND, CtrlTombMound)

def san_heartbeat(attachee, triggerer):
	return ctrl_daemon2.do_san_heartbeat(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_TOMB_MOUND, cs())

def san_dying(attachee, triggerer):
	return ctrl_daemon2.do_san_dying(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_TOMB_MOUND, cs())

def san_use(attachee, triggerer):
	return ctrl_daemon2.do_san_use(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_TOMB_MOUND, cs())

def san_bust(attachee, triggerer):
	return ctrl_daemon2.do_san_bust(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_TOMB_MOUND, cs())

def cs():
	o = utils_storage.obj_storage_by_id(DAEMON_GID)
	if (not o): 
		return None
	result = o.data.get(CtrlTombMound.get_name())
	assert isinstance(result, CtrlTombMound)
	return result

class CtrlTombMound(ctrl_daemon2.CtrlDaemon2):
	def created(self, npc):
		self.init_daemon2_fields(module_consts.MAP_ID_ZMOD_D_TOMB_MOUND, DAEMON_SCRIPT_ID, "tomb_mound")
		super(CtrlTombMound, self).created(npc)
		return

	def place_encounters_initial(self):
		self.place_passages()
		#self.place_encounter_c03(self.delayed_mode())
		return

	def delayed_mode(self):
		return 1

	# Sleep interface
	def can_sleep(self):
		return toee.SLEEP_IMPOSSIBLE

	def place_passages(self):
		loc, ox, oy = utils_obj.sec2loc(518, 277), -12.7279215, -12.7279215
		passage = toee.game.obj_create(const_proto_sceneries.PROTO_SCENERY_ICON_DOOR, loc, ox, oy)
		if (passage):
			passage.move(loc, ox, oy)
			passage.scripts[const_toee.sn_use] = self.default_script_id
			self.vars["passage_west"] = passage.id
			print("passage_west = {}".format(passage.id))
		return

	def do_san_use(self, attachee, triggerer):
		assert isinstance(attachee, toee.PyObjHandle)
		print("san_use id: {}, nameid: {}".format(attachee.id, attachee.name))

		if (attachee.id == self.vars["passage_west"]):
			toee.game.fade_and_teleport(0, 0, 0, module_consts.MAP_ID_ZMOD_D_FOREST_PATH, module_consts.ZMOD_D_FOREST_PATH_ASHOP_COORDS_ENTRY[0], module_consts.ZMOD_D_FOREST_PATH_ASHOP_COORDS_ENTRY[1])

		return toee.RUN_DEFAULT
