import toee, debug, utils_toee, utils_storage, utils_obj, utils_item, const_toee, ctrl_daemon, ctrl_daemon2
import ctrl_behaviour, py06122_cormyr_prompter, factions_zmod, utils_npc
import monster_info, module_quests, module_consts
import py06611_corinth_encounters, py04000_monster_manual1_p1

DAEMON_SCRIPT_ID = 6610
DAEMON_GID = "G_44471338_B2A6_4FF7_A636_8D13F81C1B69"
DEBUG = 0
DEBUG_SKIP_C01 = 1
DEBUG_NAMES = 1

def san_new_map(attachee, triggerer):
	return ctrl_daemon2.do_san_new_map(attachee, triggerer, module_consts.MAP_ID_ZMOD_CORINTH, CtrlCorinth)

def san_first_heartbeat(attachee, triggerer):
	return ctrl_daemon2.do_san_first_heartbeat(attachee, triggerer, module_consts.MAP_ID_ZMOD_CORINTH, CtrlCorinth)

def san_heartbeat(attachee, triggerer):
	return ctrl_daemon2.do_san_heartbeat(attachee, triggerer, module_consts.MAP_ID_ZMOD_CORINTH, cs())

def san_dying(attachee, triggerer):
	return ctrl_daemon2.do_san_dying(attachee, triggerer, module_consts.MAP_ID_ZMOD_CORINTH, cs())

def san_use(attachee, triggerer):
	return ctrl_daemon2.do_san_use(attachee, triggerer, module_consts.MAP_ID_ZMOD_CORINTH, cs())

def san_bust(attachee, triggerer):
	return ctrl_daemon2.do_san_bust(attachee, triggerer, module_consts.MAP_ID_ZMOD_CORINTH, cs())

def cs():
	o = utils_storage.obj_storage_by_id(DAEMON_GID)
	if (not o): 
		return None
	result = o.data.get(CtrlCorinth.get_name())
	assert isinstance(result, CtrlCorinth)
	return result

class CtrlCorinth(ctrl_daemon2.CtrlDaemon2):
	def created(self, npc):
		self.init_daemon2_fields(module_consts.MAP_ID_ZMOD_CORINTH, DAEMON_SCRIPT_ID, "corinth")
		super(CtrlCorinth, self).created(npc)
		return

	def place_encounters_initial(self):
		self.place_dead_bodies()
		self.place_doors()
		#self.place_general_notices()
		if (not DEBUG_SKIP_C01):
			self.place_encounter_c01()
		#self.place_encounter_c02()
		self.place_encounter_c03(self.delayed_mode())
		return

	def delayed_mode(self):
		return 1

	# Sleep interface
	def can_sleep(self):
		return toee.SLEEP_PASS_TIME_ONLY

	def do_san_bust(self, attachee, triggerer):
		assert isinstance(attachee, toee.PyObjHandle)
		print("san_bust id: {}, nameid: {}".format(attachee.id, attachee.name))
		# used as a hook from promters

		id = attachee.id
		if (self.vars.get("promter_id_ambush_1") == id):
			self.place_monsters_c01()
		elif (self.vars.get("promter_id_c02") == id):
			self.place_monsters_c02()
		return toee.RUN_DEFAULT

	def place_encounter_c01(self):
		npc = self.create_promter_at(utils_obj.sec2loc(526, 419), self.get_dialogid_default(), 0, 20, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_EXEC, "Ambush 1", const_toee.rotation_0800_oclock)
		self.vars["promter_id_ambush_1"] = npc.id
		npc.scripts[const_toee.sn_bust] = DAEMON_SCRIPT_ID
		return

	def place_monsters_c01(self):
		self.create_npc_at(utils_obj.sec2loc(526, 422), py06611_corinth_encounters.CtrlThugLeader, const_toee.rotation_0900_oclock, "c01", "thug_leader", factions_zmod.FACTION_ENEMY, 0, 1)
		if (1):
			self.create_npc_at(utils_obj.sec2loc(534, 412), py06611_corinth_encounters.CtrlThug, const_toee.rotation_0300_oclock, "c01", "thug_1", factions_zmod.FACTION_ENEMY, 0, 1)
			self.create_npc_at(utils_obj.sec2loc(537, 413), py06611_corinth_encounters.CtrlThug, const_toee.rotation_0300_oclock, "c01", "thug_2", factions_zmod.FACTION_ENEMY, 0, 1)
			self.create_npc_at(utils_obj.sec2loc(538, 416), py06611_corinth_encounters.CtrlThug, const_toee.rotation_0300_oclock, "c01", "thug_3", factions_zmod.FACTION_ENEMY, 0, 1)
			self.create_npc_at(utils_obj.sec2loc(524, 420), py06611_corinth_encounters.CtrlThug, const_toee.rotation_0300_oclock, "c01", "thug_4", factions_zmod.FACTION_ENEMY, 0, 1)
		return

	def activate_encounter_c01(self):
		print("activate_encounter_c01")
		self.activate_monster("c01", "thug_leader")
		if (1):
			self.activate_monster("c01", "thug_1")
			self.activate_monster("c01", "thug_2")
			self.activate_monster("c01", "thug_3")
			self.activate_monster("c01", "thug_4")
		return

	def place_general_notices(self):
		npc = self.create_promter_at(utils_obj.sec2loc(506, 437), self.get_dialogid_default(), 10, 20, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Corinth", const_toee.rotation_0900_oclock)
		return

	def place_dead_bodies(self):
		#npc, ctrl = self.create_npc_at(utils_obj.sec2loc(491, 432), py04000_monster_manual1_p1.CtrlCommoner, const_toee.rotation_0300_oclock, "dead_body", "1", factions_zmod.FACTION_NEUTRAL_NPC, 0, 1)
		#npc.obj_set_int(toee.obj_f_hp_damage, npc.obj_get_int(toee.obj_f_hp_pts) + 11)

		toee.game.obj_create(2112, utils_obj.sec2loc(491, 432))
		return

	def place_doors(self):
		# C03
		for obj in toee.game.obj_list_range(utils_obj.sec2loc(469, 438), 10, toee.OLC_PORTAL):
			assert isinstance(obj, toee.PyObjHandle)
			obj.scripts[const_toee.sn_use] = 6214 #py06214_doors_autodestroy

		return

	def place_encounter_c02(self, for_delayed = 0):
		if (for_delayed == 0 and self.delayed_mode()):
			npc = self.create_promter_at(utils_obj.sec2loc(465, 442), self.get_dialogid_default(), 0, 20, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_EXEC, "Lizards", const_toee.rotation_0800_oclock)
			self.vars["promter_id_c02"] = npc.id
			npc.scripts[const_toee.sn_bust] = DAEMON_SCRIPT_ID

		if (for_delayed == 1 and self.delayed_mode() == 0):
			self.place_monsters_c02()
		return

	def place_monsters_c02(self):
		self.create_npc_at(utils_obj.sec2loc(460, 442), py06611_corinth_encounters.CtrlLizardmanLeaderC02, const_toee.rotation_0800_oclock, "c02", "lizard_leader", factions_zmod.FACTION_ENEMY, 0, 1)
		if (1):
			self.create_npc_at(utils_obj.sec2loc(457, 436), py06611_corinth_encounters.CtrlLizardman, const_toee.rotation_0800_oclock, "c02", "lizard_1", factions_zmod.FACTION_ENEMY, 0, 1)
			self.create_npc_at(utils_obj.sec2loc(457, 436), py06611_corinth_encounters.CtrlLizardman, const_toee.rotation_0800_oclock, "c02", "lizard_2", factions_zmod.FACTION_ENEMY, 0, 1)
		return

	def activate_encounter_c02(self):
		print("activate_encounter_c02")
		self.activate_monster("c02", "lizard_leader")
		if (1):
			self.activate_monster("c02", "lizard_1")
			self.activate_monster("c02", "lizard_2")
		return

	def place_encounter_c03(self, for_delayed = 0):
		if (for_delayed == self.delayed_mode()):
			self.place_monsters_c03()
		return

	def place_monsters_c03(self):

		npc_leader, ctrl = self.create_npc_at(utils_obj.sec2loc(469, 421), py06611_corinth_encounters.CtrlLizardmanClericC03, const_toee.rotation_0500_oclock, "c03", "lizard_cleric", factions_zmod.FACTION_ENEMY, 0, 0)
		if (DEBUG_NAMES):
			nameid = utils_toee.make_custom_name("Lizardman Cleric")
			if (nameid):
				npc_leader.obj_set_int(toee.obj_f_critter_description_unknown, nameid)
				npc_leader.obj_set_int(const_toee.obj_f_description_correct, nameid)

		def add_sub(x, y, num, rot):
			npc, ctrl = self.create_npc_at(utils_obj.sec2loc(x, y), py06611_corinth_encounters.CtrlLizardman, rot, "c03", "lizard_{}".format(num), factions_zmod.FACTION_ENEMY, 0, 0)
			npc.obj_set_obj(toee.obj_f_npc_leader, npc_leader)
			if (DEBUG_NAMES):
				nameid = utils_toee.make_custom_name("Lizardman {}".format(num))
				if (nameid):
					npc.obj_set_int(toee.obj_f_critter_description_unknown, nameid)
					npc.obj_set_int(const_toee.obj_f_description_correct, nameid)
			return npc

		if (1):
			add_sub(469, 434, 1, const_toee.ROT05)
			add_sub(460, 425, 2, const_toee.ROT11)
			add_sub(478, 422, 3, const_toee.ROT05)
			add_sub(477, 432, 4, const_toee.ROT03)
		return
