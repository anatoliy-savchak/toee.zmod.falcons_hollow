import toee, debug, utils_toee, utils_storage, utils_obj, utils_item, const_toee, ctrl_daemon, ctrl_daemon2
import ctrl_behaviour, py06122_cormyr_prompter, factions_zmod, utils_npc
import monster_info, module_quests, module_consts, const_proto_sceneries

DAEMON_SCRIPT_ID = 6612
DAEMON_GID = "G_382FD8FF_9C44_4CBC_9C2D_53E2269EBB69"
DEBUG = 0
DEBUG_NAMES = 1

def san_new_map(attachee, triggerer):
	return ctrl_daemon2.do_san_new_map(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_TOWN_BUILDINGS, CtrlTownBuildings)

def san_first_heartbeat(attachee, triggerer):
	return ctrl_daemon2.do_san_first_heartbeat(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_TOWN_BUILDINGS, CtrlTownBuildings)

def san_heartbeat(attachee, triggerer):
	return ctrl_daemon2.do_san_heartbeat(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_TOWN_BUILDINGS, cs())

def san_dying(attachee, triggerer):
	return ctrl_daemon2.do_san_dying(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_TOWN_BUILDINGS, cs())

def san_use(attachee, triggerer):
	return ctrl_daemon2.do_san_use(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_TOWN_BUILDINGS, cs())

def san_bust(attachee, triggerer):
	return ctrl_daemon2.do_san_bust(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_TOWN_BUILDINGS, cs())

def cs():
	o = utils_storage.obj_storage_by_id(DAEMON_GID)
	if (not o): 
		return None
	result = o.data.get(CtrlTownBuildings.get_name())
	assert isinstance(result, CtrlTownBuildings)
	return result

class CtrlTownBuildings(ctrl_daemon2.CtrlDaemon2):
	def created(self, npc):
		self.init_daemon2_fields(module_consts.MAP_ID_ZMOD_D_TOWN_BUILDINGS, DAEMON_SCRIPT_ID, "town_buildings")
		super(CtrlTownBuildings, self).created(npc)
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
		loc, ox, oy = utils_obj.sec2loc(463, 473), -12.7279215, -12.7279215
		passage = toee.game.obj_create(const_proto_sceneries.PROTO_SCENERY_ICON_DOOR, loc, ox, oy)
		if (passage):
			passage.move(loc, ox, oy)
			passage.scripts[const_toee.sn_use] = self.default_script_id
			self.vars["passage_town_gates"] = passage.id
			print("passage_town_gates = {}".format(passage.id))

		loc, ox, oy = utils_obj.sec2loc(499, 480), -12.7279215, -12.7279215
		passage = toee.game.obj_create(const_proto_sceneries.PROTO_SCENERY_ICON_DOOR, loc, ox, oy)
		if (passage):
			passage.move(loc, ox, oy)
			passage.scripts[const_toee.sn_use] = self.default_script_id
			self.vars["passage_town_square_north_building"] = passage.id
			print("passage_town_square_north_building = {}".format(passage.id))

		loc, ox, oy = utils_obj.sec2loc(493, 465), -12.7279215, -12.7279215
		passage = toee.game.obj_create(const_proto_sceneries.PROTO_SCENERY_ICON_DOOR, loc, ox, oy)
		if (passage):
			passage.move(loc, ox, oy)
			passage.scripts[const_toee.sn_use] = self.default_script_id
			self.vars["passage_town_square_west_building"] = passage.id
			print("passage_town_square_west_building = {}".format(passage.id))
		return

	def do_san_use(self, attachee, triggerer):
		assert isinstance(attachee, toee.PyObjHandle)
		print("san_use id: {}, nameid: {}".format(attachee.id, attachee.name))

		if (attachee.id == self.vars["passage_town_gates"]):
			toee.game.fade_and_teleport(0, 0, 0, module_consts.MAP_ID_ZMOD_D_TOWN_GATES, module_consts.ZMOD_D_TOWN_GATES_ENTRY_TAVERN_COORDS_ENTRY[0], module_consts.ZMOD_D_TOWN_GATES_ENTRY_TAVERN_COORDS_ENTRY[1])
		elif (attachee.id == self.vars["passage_town_square_north_building"]):
			toee.game.fade_and_teleport(0, 0, 0, module_consts.MAP_ID_ZMOD_D_TOWN_SQUARE, module_consts.ZMOD_D_TOWN_SQUARE_GSHOP_COORDS_ENTRY[0], module_consts.ZMOD_D_TOWN_SQUARE_GSHOP_COORDS_ENTRY[1])
		elif (attachee.id == self.vars["passage_town_square_west_building"]):
			toee.game.fade_and_teleport(0, 0, 0, module_consts.MAP_ID_ZMOD_D_TOWN_SQUARE, module_consts.ZMOD_D_TOWN_SQUARE_CHURCH_COORDS_ENTRY[0], module_consts.ZMOD_D_TOWN_SQUARE_CHURCH_COORDS_ENTRY[1])

		return toee.RUN_DEFAULT
