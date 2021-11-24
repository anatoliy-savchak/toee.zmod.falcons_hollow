import toee, debug, utils_toee, utils_storage, utils_obj, utils_item, const_toee, ctrl_daemon, ctrl_daemon2
import ctrl_behaviour, py06122_cormyr_prompter, factions_zmod, utils_npc
import monster_info, module_quests, module_consts, const_proto_sceneries

DAEMON_SCRIPT_ID = 6611
DAEMON_GID = "G_A0040F92_F24C_45AB_AC8D_6B93220481DC"
DEBUG = 0
DEBUG_SKIP_C01 = 1
DEBUG_NAMES = 1

def san_new_map(attachee, triggerer):
	return ctrl_daemon2.do_san_new_map(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_TOWN_SQUARE, CtrlTownSquare)

def san_first_heartbeat(attachee, triggerer):
	#print(attachee.id)
	#debug.breakp('')
	return ctrl_daemon2.do_san_first_heartbeat(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_TOWN_SQUARE, CtrlTownSquare)

def san_heartbeat(attachee, triggerer):
	return ctrl_daemon2.do_san_heartbeat(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_TOWN_SQUARE, cs())

def san_dying(attachee, triggerer):
	return ctrl_daemon2.do_san_dying(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_TOWN_SQUARE, cs())

def san_use(attachee, triggerer):
	return ctrl_daemon2.do_san_use(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_TOWN_SQUARE, cs())

def san_bust(attachee, triggerer):
	return ctrl_daemon2.do_san_bust(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_TOWN_SQUARE, cs())

def cs():
	o = utils_storage.obj_storage_by_id(DAEMON_GID)
	if (not o): 
		return None
	result = o.data.get(CtrlTownSquare.get_name())
	assert isinstance(result, CtrlTownSquare)
	return result

class CtrlTownSquare(ctrl_daemon2.CtrlDaemon2):
	def created(self, npc):
		self.init_daemon2_fields(module_consts.MAP_ID_ZMOD_D_TOWN_SQUARE, DAEMON_SCRIPT_ID, "town_square")
		super(CtrlTownSquare, self).created(npc)
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
		loc, ox, oy = utils_obj.sec2loc(463, 450), -12.7279215, -12.7279215
		passage = toee.game.obj_create(const_proto_sceneries.PROTO_SCENERY_ICON_DOOR, loc, ox, oy)
		if (passage):
			passage.move(loc, ox, oy)
			passage.scripts[const_toee.sn_use] = self.default_script_id
			self.vars["passage_town_square"] = passage.id
			print("passage_town_square = {}".format(passage.id))

		loc, ox, oy = utils_obj.sec2loc(478, 455), -12.7279215, -12.7279215
		passage = toee.game.obj_create(const_proto_sceneries.PROTO_SCENERY_ICON_DOOR, loc, ox, oy)
		if (passage):
			passage.move(loc, ox, oy)
			passage.scripts[const_toee.sn_use] = self.default_script_id
			self.vars["passage_town_square_generic_shop"] = passage.id
			print("passage_town_square_generic_shop = {}".format(passage.id))

		loc, ox, oy = utils_obj.sec2loc(505, 479), -12.7279215, -12.7279215
		passage = toee.game.obj_create(const_proto_sceneries.PROTO_SCENERY_ICON_DOOR, loc, ox, oy)
		if (passage):
			passage.move(loc, ox, oy)
			passage.scripts[const_toee.sn_use] = self.default_script_id
			self.vars["passage_town_square_church"] = passage.id
			print("passage_town_square_church = {}".format(passage.id))
		return

	def do_san_use(self, attachee, triggerer):
		assert isinstance(attachee, toee.PyObjHandle)
		print("san_use id: {}, nameid: {}".format(attachee.id, attachee.name))

		if (attachee.id == self.vars["passage_town_square"]):
			toee.game.fade_and_teleport(0, 0, 0, module_consts.MAP_ID_ZMOD_D_TOWN_GATES, module_consts.ZMOD_D_TOWN_GATES_ENTRY_COORDS_SOUTH[0], module_consts.ZMOD_D_TOWN_GATES_ENTRY_COORDS_SOUTH[1])
		elif (attachee.id == self.vars["passage_town_square_generic_shop"]):
			toee.game.fade_and_teleport(0, 0, 0, module_consts.MAP_ID_ZMOD_D_TOWN_BUILDINGS, module_consts.ZMOD_D_TOWN_BUILDINGS_GSHOP_COORDS_ENTRY[0], module_consts.ZMOD_D_TOWN_BUILDINGS_GSHOP_COORDS_ENTRY[1])
		elif (attachee.id == self.vars["passage_town_square_church"]):
			toee.game.fade_and_teleport(0, 0, 0, module_consts.MAP_ID_ZMOD_D_TOWN_BUILDINGS, module_consts.ZMOD_D_TOWN_BUILDINGS_CHURCH_COORDS_ENTRY[0], module_consts.ZMOD_D_TOWN_BUILDINGS_CHURCH_COORDS_ENTRY[1])

		return toee.RUN_DEFAULT
