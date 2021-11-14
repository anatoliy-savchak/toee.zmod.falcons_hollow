import toee, debug, utils_toee, utils_storage, utils_obj, utils_item, const_proto_weapon, const_proto_armor, const_toee, ctrl_daemon, ctrl_daemon2
import ctrl_behaviour, py06122_cormyr_prompter, factions_zmod, const_proto_scrolls, const_proto_wands, utils_npc
import startup_zmod, utils_sneak, monster_info, copy, module_quests, const_animate, module_consts
import py14710_smith, py14711_smith_wife, py14712_wizard, py14713_cleric, py06603_keep_encounters
import const_proto_sceneries, utils_pc

KEEP_LV1 = 6600
KEEP_LV1_DAEMON_ID = "G_5C512D62_5E78_4965_9EAA_1821DA9CB841"
KEEP_LV1_BATTLE_ALL = 1
DEBUG = 0

def san_new_map(attachee, triggerer):
	return ctrl_daemon2.do_san_new_map(attachee, triggerer, module_consts.MAP_ID_ZMOD_KEEP_LV1, CtrlKeepLv1)

def san_first_heartbeat(attachee, triggerer):
	return ctrl_daemon2.do_san_first_heartbeat(attachee, triggerer, module_consts.MAP_ID_ZMOD_KEEP_LV1, CtrlKeepLv1)

def san_heartbeat(attachee, triggerer):
	return ctrl_daemon2.do_san_heartbeat(attachee, triggerer, module_consts.MAP_ID_ZMOD_KEEP_LV1, cs())

def san_dying(attachee, triggerer):
	return ctrl_daemon2.do_san_dying(attachee, triggerer, module_consts.MAP_ID_ZMOD_KEEP_LV1, cs())

def san_use(attachee, triggerer):
	return ctrl_daemon2.do_san_use(attachee, triggerer, module_consts.MAP_ID_ZMOD_KEEP_LV1, cs())

def cs():
	o = utils_storage.obj_storage_by_id(KEEP_LV1_DAEMON_ID)
	if (not o): return None
	if (CtrlKeepLv1.get_name() in o.data):
		result = o.data[CtrlKeepLv1.get_name()]
	else: return None
	assert isinstance(result, CtrlKeepLv1)
	return result

class CtrlKeepLv1(ctrl_daemon2.CtrlDaemon2):
	def created(self, npc):
		self.init_daemon2_fields(module_consts.MAP_ID_ZMOD_KEEP_LV1, KEEP_LV1, "keep_lv1")
		super(CtrlKeepLv1, self).created(npc)
		return

	def place_encounters_initial(self):
		self.place_passages()
		self.place_guards()
		#self.place_monsters_k01()
		#self.display_encounter_k01()
		self.place_encounter_k01()
		if (DEBUG):
			self.cheat_finish_battle()
		return

	def setwp(self, npc, x1, y1, x2, y2):
		assert isinstance(npc, toee.PyObjHandle)
		if (not "npc_waypoints_set" in dir(npc)): return
		wpl = list()
		wpl.append(utils_npc.Waypoint(x1, y1, const_toee.rotation_1000_oclock, 2000, utils_npc.WaypointFlag.Delay))
		wpl.append(utils_npc.Waypoint(x2, y2, const_toee.rotation_0400_oclock, 2000, utils_npc.WaypointFlag.Delay))
		npc.npc_waypoints_set(wpl, 0)
		npc.npc_flag_set(toee.ONF_WAYPOINTS_DAY)
		npc.npc_flag_set(toee.ONF_WAYPOINTS_NIGHT)
		return wpl

	def place_guards(self):
		nameid = utils_toee.make_custom_name("Guard")

		fx, fy = 479, 470

		npc, ctrl = self.create_npc_at(utils_obj.sec2loc(fx, fy), py06603_keep_encounters.CtrlWarriorGuard1, const_toee.rotation_0200_oclock, "k01", "guard1", factions_zmod.FACTION_ALLY_NPC, 0, 0)
		self.setwp(npc, fx, fy, fx, fy + 21)
		npc.faction_add(factions_zmod.FACTION_NEUTRAL_NPC)
		nameid = utils_toee.make_custom_name("Guard 1")
		if (nameid):
			npc.obj_set_int(toee.obj_f_critter_description_unknown, nameid)
			npc.obj_set_int(const_toee.obj_f_description_correct, nameid)
		npc.condition_add("ExperienceExempt")

		npc, ctrl = self.create_npc_at(utils_obj.sec2loc(fx + 2, fy), py06603_keep_encounters.CtrlWarriorGuard2, const_toee.rotation_0200_oclock, "k01", "guard2", factions_zmod.FACTION_ALLY_NPC, 0, 0)
		self.setwp(npc, fx + 2, fy, fx + 2, fy + 21)
		npc.faction_add(factions_zmod.FACTION_NEUTRAL_NPC)
		nameid = utils_toee.make_custom_name("Guard 2")
		if (nameid):
			npc.obj_set_int(toee.obj_f_critter_description_unknown, nameid)
			npc.obj_set_int(const_toee.obj_f_description_correct, nameid)
		npc.condition_add("ExperienceExempt")

		npc, ctrl = self.create_npc_at(utils_obj.sec2loc(fx + 4, fy), py06603_keep_encounters.CtrlWarriorGuard2, const_toee.rotation_0200_oclock, "k01", "guard3", factions_zmod.FACTION_ALLY_NPC, 0, 0)
		self.setwp(npc, fx + 4, fy, fx + 4, fy + 21)
		npc.faction_add(factions_zmod.FACTION_NEUTRAL_NPC)
		nameid = utils_toee.make_custom_name("Guard 3")
		if (nameid):
			npc.obj_set_int(toee.obj_f_critter_description_unknown, nameid)
			npc.obj_set_int(const_toee.obj_f_description_correct, nameid)
		npc.condition_add("ExperienceExempt")

		npc, ctrl = self.create_npc_at(utils_obj.sec2loc(fx, fy + 2), py06603_keep_encounters.CtrlWarriorGuard3, const_toee.rotation_0200_oclock, "k01", "guard4", factions_zmod.FACTION_ALLY_NPC, 0, 0)
		self.setwp(npc, fx, fy + 2, fx, fy + 21 + 2)
		npc.faction_add(factions_zmod.FACTION_NEUTRAL_NPC)
		nameid = utils_toee.make_custom_name("Guard 4")
		if (nameid):
			npc.obj_set_int(toee.obj_f_critter_description_unknown, nameid)
			npc.obj_set_int(const_toee.obj_f_description_correct, nameid)
		npc.condition_add("ExperienceExempt")

		npc, ctrl = self.create_npc_at(utils_obj.sec2loc(fx + 2, fy + 2), py06603_keep_encounters.CtrlWarriorGuardDwarf, const_toee.rotation_0200_oclock, "k01", "guard5", factions_zmod.FACTION_ALLY_NPC, 0, 1)
		self.setwp(npc, fx + 2, fy + 2, fx + 2, fy + 21 + 2)
		npc.faction_add(factions_zmod.FACTION_NEUTRAL_NPC)
		nameid = utils_toee.make_custom_name("Guard 5")
		if (nameid):
			npc.obj_set_int(toee.obj_f_critter_description_unknown, nameid)
			npc.obj_set_int(const_toee.obj_f_description_correct, nameid)
		npc.condition_add("ExperienceExempt")

		npc, ctrl = self.create_npc_at(utils_obj.sec2loc(fx + 4, fy + 2), py06603_keep_encounters.CtrlWarriorGuardDwarf, const_toee.rotation_0200_oclock, "k01", "guard6", factions_zmod.FACTION_ALLY_NPC, 0, 1)
		self.setwp(npc, fx + 4, fy + 2, fx + 4, fy + 21 + 2)
		npc.faction_add(factions_zmod.FACTION_NEUTRAL_NPC)
		nameid = utils_toee.make_custom_name("Guard 6")
		if (nameid):
			npc.obj_set_int(toee.obj_f_critter_description_unknown, nameid)
			npc.obj_set_int(const_toee.obj_f_description_correct, nameid)
		npc.condition_add("ExperienceExempt")

		# gates
		npc, ctrl = self.create_npc_at(utils_obj.sec2loc(471, 477), py06603_keep_encounters.CtrlWarriorGuard2, const_toee.rotation_0100_oclock, "k01", "gates1", factions_zmod.FACTION_ALLY_NPC, 0, 1)
		npc.faction_add(factions_zmod.FACTION_NEUTRAL_NPC)
		nameid = utils_toee.make_custom_name("Guard Gates 1")
		if (nameid):
			npc.obj_set_int(toee.obj_f_critter_description_unknown, nameid)
			npc.obj_set_int(const_toee.obj_f_description_correct, nameid)
		npc.condition_add("ExperienceExempt")

		npc, ctrl = self.create_npc_at(utils_obj.sec2loc(471, 487), py06603_keep_encounters.CtrlWarriorGuard2, const_toee.rotation_0100_oclock, "k01", "gates2", factions_zmod.FACTION_ALLY_NPC, 0, 1)
		npc.faction_add(factions_zmod.FACTION_NEUTRAL_NPC)
		nameid = utils_toee.make_custom_name("Guard Gates 2")
		if (nameid):
			npc.obj_set_int(toee.obj_f_critter_description_unknown, nameid)
			npc.obj_set_int(const_toee.obj_f_description_correct, nameid)
		npc.condition_add("ExperienceExempt")
		return

	def place_encounter_k01(self):
		npc = self.create_promter_at(utils_obj.sec2loc(470, 482), self.get_dialogid_default(), 10, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Gates", const_toee.rotation_0800_oclock)
		self.vars["battle_promter_id"] = npc.id
		return

	def place_monsters_k01(self):
		npc, ctrl = self.create_npc_at(utils_obj.sec2loc(457, 478), py06603_keep_encounters.CtrlOrcWizard, const_toee.rotation_0800_oclock, "k01", "orc_wizard")
		nameid = utils_toee.make_custom_name("Orc Wizard")
		if (nameid):
			npc.obj_set_int(toee.obj_f_critter_description_unknown, nameid)
			npc.obj_set_int(const_toee.obj_f_description_correct, nameid)

		if (KEEP_LV1_BATTLE_ALL):
			self.create_npc_at(utils_obj.sec2loc(459, 479), py06603_keep_encounters.CtrlOrcLeader, const_toee.rotation_0700_oclock, "k01", "orc_leader")
			self.create_npc_at(utils_obj.sec2loc(460, 476), py06603_keep_encounters.CtrlOrc, const_toee.rotation_0700_oclock, "k01", "orc1")
			self.create_npc_at(utils_obj.sec2loc(461, 474), py06603_keep_encounters.CtrlOrc, const_toee.rotation_0800_oclock, "k01", "orc2")
			self.create_npc_at(utils_obj.sec2loc(461, 482), py06603_keep_encounters.CtrlOrc, const_toee.rotation_0800_oclock, "k01", "orc3")
			self.create_npc_at(utils_obj.sec2loc(461, 487), py06603_keep_encounters.CtrlOrc, const_toee.rotation_0500_oclock, "k01", "orc4")

			npc, ctrl = self.create_npc_at(utils_obj.sec2loc(458, 486), py06603_keep_encounters.CtrlOrcCleric, const_toee.rotation_0500_oclock, "k01", "orc_cleric")
			nameid = utils_toee.make_custom_name("Orc Cleric")
			if (nameid):
				npc.obj_set_int(toee.obj_f_critter_description_unknown, nameid)
				npc.obj_set_int(const_toee.obj_f_description_correct, nameid)


			self.create_npc_at(utils_obj.sec2loc(465, 472), py06603_keep_encounters.CtrlGnoll, const_toee.rotation_0500_oclock, "k01", "gnoll1")
			self.create_npc_at(utils_obj.sec2loc(464, 475), py06603_keep_encounters.CtrlGnoll, const_toee.rotation_0500_oclock, "k01", "gnoll2")
			self.create_npc_at(utils_obj.sec2loc(463, 480), py06603_keep_encounters.CtrlGnoll, const_toee.rotation_0500_oclock, "k01", "gnoll3")
			self.create_npc_at(utils_obj.sec2loc(463, 486), py06603_keep_encounters.CtrlGnoll, const_toee.rotation_0500_oclock, "k01", "gnoll4")
			self.create_npc_at(utils_obj.sec2loc(464, 489), py06603_keep_encounters.CtrlGnoll, const_toee.rotation_0500_oclock, "k01", "gnoll5")
		return

	def display_encounter_k01(self):
		print("display_encounter_k01")

		if (0): # debug thing
			self.cheat_finish_battle()
			return

		self.place_monsters_k01()

		self.reveal_monster("k01", "orc_wizard")
		if (KEEP_LV1_BATTLE_ALL):
			self.reveal_monster("k01", "orc_leader")
			self.reveal_monster("k01", "orc1")
			self.reveal_monster("k01", "orc2")
			self.reveal_monster("k01", "orc3")
			self.reveal_monster("k01", "orc4")
			self.reveal_monster("k01", "orc_cleric")

			self.reveal_monster("k01", "gnoll1")
			self.reveal_monster("k01", "gnoll2")
			self.reveal_monster("k01", "gnoll3")
			self.reveal_monster("k01", "gnoll4")
			self.reveal_monster("k01", "gnoll5")
		return

	def get_battle_foes_and_allies(self):
		foes = list()
		allies = list()
		for foe_key in self.monsters.keys():
			if (not "k01" in foe_key): continue
			info = self.monsters[foe_key]
			if (not info): continue
			assert isinstance(info, monster_info.MonsterInfo)
			npc = info.get_npc()
			if (not npc): continue
			if (npc.object_flags_get() & toee.OF_DONTDRAW): continue
			if (not "guard" in foe_key and not "gates" in foe_key):
				foes.append(npc)
			else: allies.append(npc)
		return foes, allies

	def activate_encounter_k01(self):
		print("activate_encounter_k01")
		if (toee.game.quests[module_quests.QUEST_KEEP_DEFEND].state >= toee.qs_completed): return

		self.activate_monster("k01", "orc_wizard")
		if (KEEP_LV1_BATTLE_ALL):
			self.activate_monster("k01", "orc_leader")
			self.activate_monster("k01", "orc1")
			self.activate_monster("k01", "orc2")
			self.activate_monster("k01", "orc3")
			self.activate_monster("k01", "orc4")
			self.activate_monster("k01", "orc_cleric")

			self.activate_monster("k01", "gnoll1")
			self.activate_monster("k01", "gnoll2")
			self.activate_monster("k01", "gnoll3")
			self.activate_monster("k01", "gnoll4")
			self.activate_monster("k01", "gnoll5")

		foes, allies = self.get_battle_foes_and_allies()

		pc0 = toee.game.leader
		for npc in allies:
			pc0.ai_follower_add(npc)

		for npc in foes:
			npc.attack(pc0)
			npc.add_to_initiative()
			#npc.obj_set_obj(toee.obj_f_npc_who_hit_me_last, toee.OBJ_HANDLE_NULL)

		for npc in allies:
			npc.add_to_initiative()

		toee.game.quests[module_quests.QUEST_KEEP_DEFEND].state = toee.qs_mentioned;
		return



	def place_priest(self):
		loc = utils_obj.sec2loc(480, 470)
		npc, ctrl = self.create_npc_at(loc, py14713_cleric.CtrlGimrid, const_toee.rotation_0500_oclock, "keep", "priest", factions_zmod.FACTION_NEUTRAL_NPC, 0, 1)

		if (1):
			wpl = list()
			wpl.append(utils_npc.Waypoint(480, 470, const_toee.rotation_1000_oclock, 1000, utils_npc.WaypointFlag.Delay))
			wpl.append(utils_npc.Waypoint(480, 481, const_toee.rotation_0600_oclock, 1000, utils_npc.WaypointFlag.Delay))
			npc.npc_waypoints_set(wpl, 1)
			npc.npc_flag_set(toee.ONF_WAYPOINTS_DAY)
			npc.npc_flag_set(toee.ONF_WAYPOINTS_NIGHT)
		return

	def assign_npc_waypoints_after_first_battle(self, npc):
		if ("npc_waypoints_set" in dir(npc)):
			info = self.get_monsterinfo_by_npc(npc)
			self.assign_npc_waypoints_after_first_battle_info(info)
		return

	def assign_npc_waypoints_after_first_battle_info(self, info):
		npc = info.get_npc()
		if (not npc): return
		if ("npc_waypoints_set" in dir(npc)):
			if (info.encounter_code == "k01" and info.monster_code_name.startswith("guard")):
				x = 100
				y = 73
				if (info.monster_code_name == "guard1"):
					pass
				elif (info.monster_code_name == "guard2"):
					y = 78
				elif (info.monster_code_name == "guard3"):
					y = 87
				elif (info.monster_code_name == "guard4"):
					y = 118
				elif (info.monster_code_name == "guard5"):
					y = 112
				elif (info.monster_code_name == "guard6"):
					y = 103
				wpl = list()
				wpl.append(utils_npc.Waypoint(x, y, const_toee.rotation_1000_oclock, 3000, utils_npc.WaypointFlag.Delay))
				wpl.append(utils_npc.Waypoint(x, y, const_toee.rotation_0600_oclock, 3000, utils_npc.WaypointFlag.Delay))
				wpl.append(utils_npc.Waypoint(x, y, const_toee.rotation_0900_oclock, 3000, utils_npc.WaypointFlag.Delay))
				npc.npc_waypoints_set(wpl, 1)
				npc.npc_flag_set(toee.ONF_WAYPOINTS_DAY)
				npc.npc_flag_set(toee.ONF_WAYPOINTS_NIGHT)
		return

	def npc_enter_combat(self, npc, ctrl):
		pc_combat_started = 0
		if (self.vars and "pc_combat_started" in self.vars and self.vars["pc_combat_started"]):
			pc_combat_started = 1

		if (not pc_combat_started):
			for pc in toee.game.party:
				pc.condition_add("Surprised2")
			self.vars["pc_combat_started"] = 1
		return

	def npc_exit_combat(self, npc, ctrl):
		return

	def heartbeat(self, npc):
		pc_combat_ended = self.get_var("pc_combat_ended")
		if (not pc_combat_ended):
			pc_combat_started = self.get_var("pc_combat_started")
			if (pc_combat_started):
				if (not toee.game.combat_is_active()):
					alive_foe = None
					foes, allies = self.get_battle_foes_and_allies()
					for obj in foes:
						assert isinstance(obj, toee.PyObjHandle)
						if (obj and utils_npc.npc_is_alive(obj)):
							alive_foe = obj
							break
					if (not alive_foe):
						self.vars["pc_combat_ended"] = 1
						self.battle_ended()
		return

	def battle_ended(self):
		if (toee.game.quests[module_quests.QUEST_KEEP_DEFEND].state == toee.qs_completed): return
		toee.game.quests[module_quests.QUEST_KEEP_DEFEND].state = toee.qs_completed

		pc0 = toee.game.party[0]
		alive_allies = 0
		# handle allies
		if (1):
			foes, allies = self.get_battle_foes_and_allies()
			for obj in allies:
				pc0.follower_remove(obj)
				if (utils_npc.npc_hp_current(obj) >= 0):
					alive_allies += 1
				obj.destroy()
			self.validate_minfo()
			self.factions_existance_refresh()

		if (1):
			xpgain = 100 * alive_allies
			message = "\nYou receive 100 xp for each healthy ally: {}!\n\n".format(xpgain)
			toee.game.create_history_freeform(message)
			if (xpgain):
				utils_pc.pc_award_experience_party(xpgain, 1)

		self.place_guards2()
		self.place_priest()
		return

	def get_npc_priest(self):
		# import py06600_daemon_keep
		# py06600_daemon_keep.cs().get_npc_priest()
		return self.get_monsterinfo_and_npc_and_ctrl("keep", "priest")

	def port_road_use(self, portal):
		assert isinstance(portal, toee.PyObjHandle)

		obj = toee.game.obj_create(py06122_cormyr_prompter.PROTO_NPC_PROMPTER, portal.location)
		obj.scripts[const_toee.sn_dialog] = self.get_dialogid_default()
		#obj.begin_dialog(toee.game.leader, 20)
		toee.game.leader.begin_dialog(obj, 20)
		return toee.SKIP_DEFAULT

	def dialog_travel_corinth(self):
		#toee.game.fade_and_teleport(2*24*60*60, 0, 0, kots_consts.MAP_ID_CORINTH, kots_consts.MAP_COORDS_CORINTH_START[0], kots_consts.MAP_COORDS_CORINTH_START[1])
		toee.game.fade_and_teleport(2*24*60*60, 0, 0, module_consts.MAP_ID_ZMOD_CORINTH, module_consts.ZMOD_CORINTH_ENTRY_COORDS[0], module_consts.ZMOD_CORINTH_ENTRY_COORDS[1])
		return
	
	def place_passages(self):
		# staris up
		loc, ox, oy = utils_obj.sec2loc(501, 493), -12.7279215, -12.7279215
		passage = toee.game.obj_create(const_proto_sceneries.PROTO_SCENERY_ICON_STAIRS_UP, loc, ox, oy)
		if (passage):
			passage.move(loc, ox, oy)
			passage.scripts[const_toee.sn_use] = self.default_script_id
			self.vars["passage_up"] = passage.id
			print("passage_up = {}".format(passage.id))

		self.place_passage_wayout()
		return

	def place_passage_wayout(self):
		#py06600_daemon_keep.cs().place_passage_wayout()
		id = self.vars.get("passage_way_out")
		if (id): return

		# way out
		loc, ox, oy = utils_obj.sec2loc(454, 477), -12.7279215, -12.7279215
		passage = toee.game.obj_create(const_proto_sceneries.PROTO_SCENERY_ICON_DOOR, loc, ox, oy)
		if (passage):
			passage.move(loc, ox, oy)
			passage.scripts[const_toee.sn_use] = self.default_script_id
			self.vars["passage_way_out"] = passage.id
			print("passage_way_out = {}".format(passage.id))
		return

	def do_san_use(self, attachee, triggerer):
		assert isinstance(attachee, toee.PyObjHandle)
		print("san_use id: {}, nameid: {}".format(attachee.id, attachee.name))

		if (attachee.id == self.vars["passage_up"]):
			toee.game.fade_and_teleport(0, 0, 0, module_consts.MAP_ID_ZMOD_KEEP_LV2, module_consts.ZMOD_KEEP_LV2_ENTRY_COORDS_STAIRS[0], module_consts.ZMOD_KEEP_LV2_ENTRY_COORDS_STAIRS[1])
		elif (attachee.id == self.vars["passage_way_out"]):
			self.port_road_use(attachee)

		return toee.RUN_DEFAULT

	# Sleep interface
	def can_sleep(self):
		return toee.SLEEP_PASS_TIME_ONLY

	def place_guards2(self):
		nameid = utils_toee.make_custom_name("Guard")

		def place_g(x, y, name):
			npc, ctrl = self.create_npc_at(utils_obj.sec2loc(x, y), py06603_keep_encounters.CtrlWarriorGuard1, const_toee.rotation_0200_oclock, "k02", name, factions_zmod.FACTION_ALLY_NPC, 0, 0)
			npc.faction_add(factions_zmod.FACTION_NEUTRAL_NPC)
			if (nameid):
				npc.obj_set_int(toee.obj_f_critter_description_unknown, nameid)
				npc.obj_set_int(const_toee.obj_f_description_correct, nameid)
			return

		place_g(471, 478, "guard1")
		place_g(471, 476, "guard2")
		place_g(471, 486, "guard3")
		place_g(471, 488, "guard4")

		place_g(484, 471, "guard5")
		place_g(484, 478, "guard6")

		return

	def cheat_finish_battle(self):
		# import py06600_daemon_keep
		# py06600_daemon_keep.cs().cheat_finish_battle()

		battle_promter_id = self.get_var("battle_promter_id")
		if (battle_promter_id):
			battle_promter = toee.game.get_obj_by_id(battle_promter_id)
			if (battle_promter):
				battle_promter.destroy()
				self.vars["battle_promter_id"] = None

		toee.game.leader.money_adj(1200*100)
		utils_pc.pc_award_experience_party(1650*4, 1)
		self.vars["pc_combat_ended"] = 1
		self.battle_ended()
		return