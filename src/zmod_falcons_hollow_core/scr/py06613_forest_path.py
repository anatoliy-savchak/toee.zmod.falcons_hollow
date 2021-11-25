import toee, debug, utils_toee, utils_storage, utils_obj, utils_item, const_toee, ctrl_daemon, ctrl_daemon2
import ctrl_behaviour, py06122_cormyr_prompter, factions_zmod, utils_npc
import monster_info, module_quests, module_consts, const_proto_sceneries

DAEMON_SCRIPT_ID = 6613
DAEMON_GID = "G_FEFDDC50_B97D_4BFD_AD13_3ACE03C6B813"
DEBUG = 0
DEBUG_NAMES = 1

def san_new_map(attachee, triggerer):
	return ctrl_daemon2.do_san_new_map(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_FOREST_PATH, CtrlForestPath)

def san_first_heartbeat(attachee, triggerer):
	#print(attachee.id)
	#debug.breakp("")
	return ctrl_daemon2.do_san_first_heartbeat(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_FOREST_PATH, CtrlForestPath)

def san_heartbeat(attachee, triggerer):
	return ctrl_daemon2.do_san_heartbeat(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_FOREST_PATH, cs())

def san_dying(attachee, triggerer):
	return ctrl_daemon2.do_san_dying(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_FOREST_PATH, cs())

def san_use(attachee, triggerer):
	return ctrl_daemon2.do_san_use(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_FOREST_PATH, cs())

def san_bust(attachee, triggerer):
	return ctrl_daemon2.do_san_bust(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_FOREST_PATH, cs())

def cs():
	o = utils_storage.obj_storage_by_id(DAEMON_GID)
	if (not o): 
		return None
	result = o.data.get(CtrlForestPath.get_name())
	assert isinstance(result, CtrlForestPath)
	return result

class CtrlForestPath(ctrl_daemon2.CtrlDaemon2):
	def created(self, npc):
		self.init_daemon2_fields(module_consts.MAP_ID_ZMOD_D_FOREST_PATH, DAEMON_SCRIPT_ID, "forest_path")
		super(CtrlForestPath, self).created(npc)
		return

	def place_encounters_initial(self):
		self.place_passages()
		#self.place_encounter_c03(self.delayed_mode())
		return

	def delayed_mode(self):
		return 1

	# Sleep interface
	def can_sleep(self):
		return toee.SLEEP_PASS_TIME_ONLY

	def place_passages(self):
		loc, ox, oy = utils_obj.sec2loc(464, 509), -12.7279215, -12.7279215
		passage = toee.game.obj_create(const_proto_sceneries.PROTO_SCENERY_ICON_DOOR, loc, ox, oy)
		if (passage):
			passage.move(loc, ox, oy)
			passage.scripts[const_toee.sn_use] = self.default_script_id
			self.vars["passage_to_town_gates_north"] = passage.id
			print("passage_to_town_gates_north = {}".format(passage.id))

		loc, ox, oy = utils_obj.sec2loc(484, 461), -12.7279215, -12.7279215
		passage = toee.game.obj_create(const_proto_sceneries.PROTO_SCENERY_ICON_DOOR, loc, ox, oy)
		if (passage):
			passage.move(loc, ox, oy)
			passage.scripts[const_toee.sn_use] = self.default_script_id
			self.vars["passage_to_ashop"] = passage.id
			print("passage_to_ashop = {}".format(passage.id))

		loc, ox, oy = utils_obj.sec2loc(504, 463), -12.7279215, -12.7279215
		passage = toee.game.obj_create(const_proto_sceneries.PROTO_SCENERY_ICON_DOOR, loc, ox, oy)
		if (passage):
			passage.move(loc, ox, oy)
			passage.scripts[const_toee.sn_use] = self.default_script_id
			self.vars["passage_to_west"] = passage.id
			print("passage_to_west = {}".format(passage.id))

		loc, ox, oy = utils_obj.sec2loc(456, 465), -12.7279215, -12.7279215
		passage = toee.game.obj_create(const_proto_sceneries.PROTO_SCENERY_ICON_DOOR, loc, ox, oy)
		if (passage):
			passage.move(loc, ox, oy)
			passage.scripts[const_toee.sn_use] = self.default_script_id
			self.vars["passage_to_east"] = passage.id
			print("passage_to_east = {}".format(passage.id))
		return

	def do_san_use(self, attachee, triggerer):
		assert isinstance(attachee, toee.PyObjHandle)
		print("san_use id: {}, nameid: {}".format(attachee.id, attachee.name))

		if (attachee.id == self.vars["passage_to_town_gates_north"]):
			toee.game.fade_and_teleport(0, 0, 0, module_consts.MAP_ID_ZMOD_D_TOWN_GATES, module_consts.ZMOD_D_TOWN_GATES_ENTRY_COORDS_BEFORE_GATES[0], module_consts.ZMOD_D_TOWN_GATES_ENTRY_COORDS_BEFORE_GATES[1])
		elif (attachee.id == self.vars["passage_to_ashop"]):
			toee.game.fade_and_teleport(0, 0, 0, module_consts.MAP_ID_ZMOD_D_APOTHECARY, module_consts.ZMOD_D_APOTHECARY_COORDS_ENTRY[0], module_consts.ZMOD_D_APOTHECARY_COORDS_ENTRY[1])

		return toee.RUN_DEFAULT
