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
		#self.place_encounter_m03()
		#self.place_encounter_m04()
		#self.place_encounter_m05()
		#self.place_encounter_m06()
		self.place_encounter_m08()
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

	def place_encounter_m04(self):
		PROMTER_SET = {
			"loc": utils_obj.sec2loc(464, 478),
			"title": "Mural Chamber",
			"rot": const_toee.rotation_0800_oclock
		}
		npc = self.create_promter_at(PROMTER_SET["loc"], self.get_dialogid_default(), 40, 10 \
			, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, PROMTER_SET["title"], PROMTER_SET["rot"] \
		)
		#self.vars["promter_id_accursed_entry"] = npc.id
		#npc.scripts[const_toee.sn_bust] = DAEMON_SCRIPT_ID
		if (not self.delayed_monsters()):
			self.place_monsters_m04()
		return

	def place_monsters_m04(self):
		self.create_npc_at(utils_obj.sec2loc(465, 477), py06631_tomb_encounters.CtrlBelker, const_toee.rotation_0500_oclock, "m04", "belker", factions_zmod.FACTION_ENEMY)
		return

	def display_encounter_m04(self):
		p = toee.game.party
		l = len(p)
		p[0].move(utils_obj.sec2loc(475, 480))
		if (l >= 1): p[0].move(utils_obj.sec2loc(468, 476))
		if (l >= 2): p[1].move(utils_obj.sec2loc(468, 478))
		if (l >= 3): p[2].move(utils_obj.sec2loc(470, 478))
		if (l >= 4): p[3].move(utils_obj.sec2loc(470, 476))
		if (l >= 5): p[4].move(utils_obj.sec2loc(468, 480))
		print("display_encounter_m04")
		if (self.delayed_monsters()):
			self.place_monsters_m04()
		self.reveal_monster("m04", "belker")
		return

	def activate_encounter_m04(self):
		self.display_encounter_m04()
		print("activate_encounter_m04")
		self.activate_monster("m04", "belker")
		return

	def place_encounter_m05(self):
		PROMTER_SET = {
			"loc": utils_obj.sec2loc(466, 471),
			"title": "Sepulcher of the Honor guard",
			"rot": const_toee.rotation_0800_oclock
		}
		npc = self.create_promter_at(PROMTER_SET["loc"], self.get_dialogid_default(), 50, 5 \
			, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, PROMTER_SET["title"], PROMTER_SET["rot"] \
		)
		#self.vars["promter_id_accursed_entry"] = npc.id
		#npc.scripts[const_toee.sn_bust] = DAEMON_SCRIPT_ID
		if (not self.delayed_monsters()):
			self.place_monsters_m05()
		return

	def place_monsters_m05(self):
		self.create_npc_at(utils_obj.sec2loc(464, 471), py06631_tomb_encounters.CtrlWight, const_toee.rotation_0500_oclock, "m05", "wight01", factions_zmod.FACTION_ENEMY)
		self.create_npc_at(utils_obj.sec2loc(464, 469), py06631_tomb_encounters.CtrlWight, const_toee.rotation_0500_oclock, "m05", "wight02", factions_zmod.FACTION_ENEMY)
		self.create_npc_at(utils_obj.sec2loc(468, 471), py06631_tomb_encounters.CtrlWight, const_toee.rotation_0500_oclock, "m05", "wight03", factions_zmod.FACTION_ENEMY)
		self.create_npc_at(utils_obj.sec2loc(468, 469), py06631_tomb_encounters.CtrlWight, const_toee.rotation_0500_oclock, "m05", "wight04", factions_zmod.FACTION_ENEMY)
		self.create_npc_at(utils_obj.sec2loc(466, 467), py06631_tomb_encounters.CtrlWight, const_toee.rotation_0500_oclock, "m05", "wight05", factions_zmod.FACTION_ENEMY)
		return

	def display_encounter_m05(self):
		print("display_encounter_m05")
		if (self.delayed_monsters()):
			self.place_monsters_m05()
		self.reveal_monster("m05", "wight01")
		self.reveal_monster("m05", "wight02")
		self.reveal_monster("m05", "wight03")
		self.reveal_monster("m05", "wight04")
		self.reveal_monster("m05", "wight05")
		return

	def activate_encounter_m05(self):
		self.display_encounter_m05()
		print("activate_encounter_m05")
		self.activate_monster("m05", "wight01")
		self.activate_monster("m05", "wight02")
		self.activate_monster("m05", "wight03")
		self.activate_monster("m05", "wight04")
		self.activate_monster("m05", "wight05")
		return

	def place_encounter_m06(self):
		PROMTER_SET = {
			"loc": utils_obj.sec2loc(466, 486),
			"title": "The Consort",
			"rot": const_toee.rotation_0800_oclock
		}
		npc = self.create_promter_at(PROMTER_SET["loc"], self.get_dialogid_default(), 60, 10 \
			, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, PROMTER_SET["title"], PROMTER_SET["rot"] \
		)
		#self.vars["promter_id_accursed_entry"] = npc.id
		#npc.scripts[const_toee.sn_bust] = DAEMON_SCRIPT_ID
		if (not self.delayed_monsters()):
			self.place_monsters_m06()
		return

	def place_monsters_m06(self):
		self.create_npc_at(utils_obj.sec2loc(468, 488), py06631_tomb_encounters.CtrlWraith, const_toee.rotation_1100_oclock, "m06", "wraith", factions_zmod.FACTION_ENEMY)
		return

	def display_encounter_m06(self):
		print("display_encounter_m06")
		if (self.delayed_monsters()):
			self.place_monsters_m06()
		self.reveal_monster("m06", "wraith")
		return

	def activate_encounter_m06(self):
		self.display_encounter_m06()
		print("activate_encounter_m06")
		self.activate_monster("m06", "wraith")
		return

	def place_encounter_m08(self):
		PROMTER_SET = {
			"loc": utils_obj.sec2loc(447, 478),
			"title": "The Consort",
			"rot": const_toee.rotation_0800_oclock
		}
		npc = self.create_promter_at(PROMTER_SET["loc"], self.get_dialogid_default(), 80, 5 \
			, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, PROMTER_SET["title"], PROMTER_SET["rot"] \
		)
		#self.vars["promter_id_accursed_entry"] = npc.id
		#npc.scripts[const_toee.sn_bust] = DAEMON_SCRIPT_ID
		if (not self.delayed_monsters()):
			self.place_monsters_m08()
		return

	def place_monsters_m08(self):
		king_npc, king_ctrl = self.create_npc_at(utils_obj.sec2loc(445, 478), py06631_tomb_encounters.CtrlKoboldKing, const_toee.rotation_0700_oclock, "m08", "king", factions_zmod.FACTION_ENEMY)
		self.vars['king_id'] = king_npc.id
		return

	def display_encounter_m08(self):
		print("display_encounter_m08")
		if (self.delayed_monsters()):
			self.place_monsters_m08()
		self.reveal_monster("m08", "king")
		return

	def activate_encounter_m08(self):
		#self.display_encounter_m08()
		print("activate_encounter_m08")
		self.activate_monster("m08", "king")
		return

	def get_king_ctrl(self):
		king_id = self.vars.get('king_id')
		ctrl = ctrl_behaviour.get_ctrl(king_id)
		return ctrl