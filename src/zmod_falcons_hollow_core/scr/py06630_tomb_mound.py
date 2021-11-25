import toee, debug, utils_toee, utils_storage, utils_obj, utils_item, const_toee, ctrl_daemon, ctrl_daemon2
import ctrl_behaviour, py06122_cormyr_prompter, factions_zmod, utils_npc
import monster_info, module_quests, module_consts, const_proto_sceneries
import py06631_tomb_encounters

DAEMON_SCRIPT_ID = 6630
DAEMON_GID = "G_99937EEC_DAAD_476D_8346_09C9F0345275"
DEBUG = 0
DEBUG_NAMES = 1

def san_new_map(attachee, triggerer):
	return ctrl_daemon2.do_san_new_map(attachee, triggerer, module_consts.MAP_ID_ZMOD_D_TOMB_MOUND, CtrlTombMound)

def san_first_heartbeat(attachee, triggerer):
	#print(attachee.id)
	#debug.breakp("")
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
		#self.place_encounter_m01()
		self.place_encounter_m03()
		return

	def delayed_mode(self):
		return 1

	# Sleep interface
	def can_sleep(self):
		return toee.SLEEP_IMPOSSIBLE

	def delayed_monsters(self):
		return True

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

	def place_encounter_m01(self):
		PROMTER_SET = {
			"loc": utils_obj.sec2loc(486, 478),
			"title": "Accursed Entry",
			"rot": const_toee.rotation_0800_oclock
		}
		npc = self.create_promter_at(PROMTER_SET["loc"], self.get_dialogid_default(), 10, 5 \
			, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, PROMTER_SET["title"], PROMTER_SET["rot"] \
		)
		self.vars["promter_id_accursed_entry"] = npc.id
		#npc.scripts[const_toee.sn_bust] = DAEMON_SCRIPT_ID
		if (not self.delayed_monsters()):
			self.place_monsters_m01()
		return

	def place_monsters_m01(self):
		self.create_npc_at(utils_obj.sec2loc(488, 476), py06631_tomb_encounters.CtrlShadow, const_toee.rotation_0500_oclock, "m01", "shadow01", factions_zmod.FACTION_ENEMY)
		self.create_npc_at(utils_obj.sec2loc(488, 480), py06631_tomb_encounters.CtrlShadow, const_toee.rotation_0500_oclock, "m01", "shadow02", factions_zmod.FACTION_ENEMY)
		return

	def display_encounter_m01(self):
		print("display_encounter_m01")
		if (self.delayed_monsters()):
			self.place_monsters_m01()
		self.reveal_monster("m01", "shadow01")
		self.reveal_monster("m01", "shadow02")
		return

	def activate_encounter_m01(self):
		self.display_encounter_m01()
		print("activate_encounter_m01")
		self.activate_monster("m01", "shadow01")
		self.activate_monster("m01", "shadow02")
		return

	def place_encounter_m03(self):
		PROMTER_SET = {
			"loc": utils_obj.sec2loc(475, 478),
			"title": "The Broken Fountain",
			"rot": const_toee.rotation_0800_oclock
		}
		npc = self.create_promter_at(PROMTER_SET["loc"], self.get_dialogid_default(), 20, 5 \
			, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, PROMTER_SET["title"], PROMTER_SET["rot"] \
		)
		self.vars["promter_id_accursed_entry"] = npc.id
		#npc.scripts[const_toee.sn_bust] = DAEMON_SCRIPT_ID
		if (not self.delayed_monsters()):
			self.place_monsters_m03()
		return

	def place_monsters_m03(self):
		self.create_npc_at(utils_obj.sec2loc(475, 476), py06631_tomb_encounters.CtrlElementalWaterSmall, const_toee.rotation_0500_oclock, "m03", "water01", factions_zmod.FACTION_ENEMY)
		self.create_npc_at(utils_obj.sec2loc(477, 476), py06631_tomb_encounters.CtrlElementalWaterSmall, const_toee.rotation_0500_oclock, "m03", "water02", factions_zmod.FACTION_ENEMY)
		self.create_npc_at(utils_obj.sec2loc(479, 478), py06631_tomb_encounters.CtrlElementalWaterSmall, const_toee.rotation_0500_oclock, "m03", "water03", factions_zmod.FACTION_ENEMY)
		return

	def display_encounter_m03(self):
		p = toee.game.party
		l = len(p)
		p[0].move(utils_obj.sec2loc(475, 480))
		if (l > 1): p[0].move(utils_obj.sec2loc(475, 478))
		if (l > 2): p[1].move(utils_obj.sec2loc(477, 478))
		if (l > 3): p[2].move(utils_obj.sec2loc(479, 478))
		if (l > 4): p[3].move(utils_obj.sec2loc(479, 480))
		if (l > 5): p[4].move(utils_obj.sec2loc(477, 480))
		print("display_encounter_m03")
		if (self.delayed_monsters()):
			self.place_monsters_m03()
		self.reveal_monster("m03", "water01")
		self.reveal_monster("m03", "water02")
		self.reveal_monster("m03", "water03")
		return

	def activate_encounter_m03(self):
		self.display_encounter_m03()
		print("activate_encounter_m03")
		self.activate_monster("m03", "water01")
		self.activate_monster("m03", "water02")
		self.activate_monster("m03", "water03")
		return
