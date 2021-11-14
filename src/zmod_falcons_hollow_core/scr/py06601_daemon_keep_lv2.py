import toee, debug, ctrl_daemon, ctrl_daemon2, utils_toee, utils_storage, utils_obj, utils_item, const_proto_weapon, const_proto_armor, const_toee
import ctrl_behaviour, py06122_cormyr_prompter, factions_zmod, const_proto_scrolls, const_proto_wands, utils_npc
import module_consts, const_proto_sceneries, py14712_wizard, py06123_event_object_fireplace, py14715_wizard_help
import py04000_monster_manual1_p1, module_globals, py14716_gambler

KEEP_LV2 = 6601
KEEP_LV2_DAEMON_ID = "G_A68BA524_3C42_4D5E_A647_7F74A3C37925"

def san_new_map(attachee, triggerer):
	return ctrl_daemon2.do_san_new_map(attachee, triggerer, module_consts.MAP_ID_ZMOD_KEEP_LV2, CtrlKeepLv2)

def san_first_heartbeat(attachee, triggerer):
	return ctrl_daemon2.do_san_first_heartbeat(attachee, triggerer, module_consts.MAP_ID_ZMOD_KEEP_LV2, CtrlKeepLv2)

def san_heartbeat(attachee, triggerer):
	return ctrl_daemon2.do_san_heartbeat(attachee, triggerer, module_consts.MAP_ID_ZMOD_KEEP_LV2, cs())

def san_dying(attachee, triggerer):
	return ctrl_daemon2.do_san_dying(attachee, triggerer, module_consts.MAP_ID_ZMOD_KEEP_LV2, cs())

def san_use(attachee, triggerer):
	return ctrl_daemon2.do_san_use(attachee, triggerer, module_consts.MAP_ID_ZMOD_KEEP_LV2, cs())

def cs():
	o = utils_storage.obj_storage_by_id(KEEP_LV2_DAEMON_ID)
	if (not o): return None
	if (CtrlKeepLv2.get_name() in o.data):
		result = o.data[CtrlKeepLv2.get_name()]
	else: return None
	assert isinstance(result, CtrlKeepLv2)
	return result

class CtrlKeepLv2(ctrl_daemon2.CtrlDaemon2):
	def created(self, npc):
		self.init_daemon2_fields(module_consts.MAP_ID_ZMOD_KEEP_LV2, KEEP_LV2, "keep_lv2")
		super(CtrlKeepLv2, self).created(npc)
		return

	def place_encounters_initial(self):
		self.place_passages()
		self.place_wizard()
		self.ensure_fireplace()
		self.place_wizard_assistant()
		self.place_gambler()
		return

	def place_encounters_next(self):
		#debug.breakp("place_encounters_next")
		print("place_encounters_next for {}".format(self))
		self.place_fireplace()
		return
	
	def place_passages(self):
		# stairs down
		loc, ox, oy = utils_obj.sec2loc(482, 489), -12.7279215, -12.7279215
		passage = toee.game.obj_create(const_proto_sceneries.PROTO_SCENERY_ICON_STAIRS_DOWN, loc, ox, oy)
		if (passage):
			passage.move(loc, ox, oy)
			passage.scripts[const_toee.sn_use] = self.default_script_id
			self.vars["passage_down"] = passage.id
			print("passage_up = {}".format(passage.id))

		# stairs up
		loc, ox, oy = utils_obj.sec2loc(490, 489), -12.7279215, -12.7279215
		passage = toee.game.obj_create(const_proto_sceneries.PROTO_SCENERY_ICON_STAIRS_UP, loc, ox, oy)
		if (passage):
			passage.move(loc, ox, oy)
			passage.scripts[const_toee.sn_use] = self.default_script_id
			self.vars["passage_up"] = passage.id
			print("passage_up = {}".format(passage.id))
		return

	def do_san_use(self, attachee, triggerer):
		assert isinstance(attachee, toee.PyObjHandle)
		print("san_use id: {}, nameid: {}".format(attachee.id, attachee.name))

		if (attachee.id == self.vars["passage_up"]):
			toee.game.fade_and_teleport(0, 0, 0, module_consts.MAP_ID_ZMOD_KEEP_LV3, module_consts.ZMOD_KEEP_LV3_ENTRY_COORDS_STAIRS[0], module_consts.ZMOD_KEEP_LV3_ENTRY_COORDS_STAIRS[1])
		elif (attachee.id == self.vars["passage_down"]):
			toee.game.fade_and_teleport(0, 0, 0, module_consts.MAP_ID_ZMOD_KEEP_LV1, module_consts.ZMOD_KEEP_LV1_ENTRY_COORDS_STAIRS[0], module_consts.ZMOD_KEEP_LV1_ENTRY_COORDS_STAIRS[1])

		return toee.RUN_DEFAULT

	def place_wizard(self):
		m = self.get_monsterinfo("keep", "wizard")
		if (m): return

		loc = utils_obj.sec2loc(487, 466)
		npc, ctrl = self.create_npc_at(loc, py14712_wizard.CtrlWizardQuoris, const_toee.rotation_0400_oclock, "keep", "wizard", factions_zmod.FACTION_FIRENDY_NPC, 0, 1)
		return

	def place_wizard_assistant(self):
		m = self.get_monsterinfo("keep", "wizard_assistant")
		if (m): return

		loc = utils_obj.sec2loc(488, 468)
		npc, ctrl = self.create_npc_at(loc, py14715_wizard_help.CtrlWizardShania, const_toee.rotation_0300_oclock, "keep", "wizard_assistant", factions_zmod.FACTION_FIRENDY_NPC, 0, 1)
		return

	def place_gambler(self):
		m = self.get_monsterinfo("keep", "gambler")
		if (m): return

		loc = utils_obj.sec2loc(469, 467)
		npc, ctrl = self.create_npc_at(loc, py14716_gambler.CtrlKeepGabler, const_toee.rotation_0500_oclock, "keep", "gambler", factions_zmod.FACTION_FIRENDY_NPC, 0, 1)

		loc = utils_obj.sec2loc(474, 470)
		npc, ctrl = self.create_npc_at(loc, py14716_gambler.CtrlKeepGablerBystander, const_toee.rotation_0200_oclock, "keep", "gambler2", factions_zmod.FACTION_FIRENDY_NPC, 0, 1)
		
		return

	# Sleep interface
	def can_sleep(self):
		fireplace = self.ensure_fireplace()
		if (fireplace):
			for pc in toee.game.party:
				if (py06123_event_object_fireplace.fireplace_is_in_area(fireplace, pc)):
					return toee.SLEEP_SAFE
		#print("return toee.SLEEP_PASS_TIME_ONLY")
		return toee.SLEEP_PASS_TIME_ONLY

	def ensure_fireplace(self):
		fireplace = self.get_fireplace()
		print("ensure_fireplace: {}".format(fireplace))
		if (not fireplace):
			print("ensure_fireplace recreating...")
			fireplace = self.place_fireplace()

		return fireplace

	def place_fireplace(self):
		fireplace = self.get_fireplace()
		if (fireplace):
			fireplace.destroy()
			self.vars["fireplace_id"] = 0

		radius_feet_int = 10
		fireplace = py06123_event_object_fireplace.fireplace_create(module_consts.ZMOD_KEEP_LV2_COORDS_FIREPLACE[0], module_consts.ZMOD_KEEP_LV2_COORDS_FIREPLACE[1], radius_feet_int, -10, -10)
		self.vars["fireplace_id"] = fireplace.id
		return fireplace

	def get_fireplace(self):
		fireplace_id = self.get_var("fireplace_id")
		if (fireplace_id):
			fireplace = toee.game.get_obj_by_id(fireplace_id)
			if (fireplace and fireplace.object_flags_get() & toee.OF_DESTROYED):
				print("no fireplace!")
				return
			return fireplace
		return

	def fireplace_change_effect(self, part_name):
		fireplace = self.get_fireplace()
		if (fireplace):
			py06123_event_object_fireplace.fireplace_change_effect(fireplace, part_name)
		return

	def storage_data_loaded(self):
		self.place_fireplace()
		return

	def on_quoris_summon_1(self, ctrl):
		def do_summon(x, y, name):
			loc = utils_obj.sec2loc(x, y)
			npc, ctrl = self.create_npc_at(loc, py04000_monster_manual1_p1.CtrlElementalWaterSmall, const_toee.rotation_0700_oclock, "quest_summon_1", name, factions_zmod.FACTION_ENEMY, 0, 0)
			if (npc): 
				npc.condition_add_with_args("sp-Summoned", 0, 10, 0)
				# npc.condition_add("Augment Summoning Enhancement") # too tough, vanilla does not have it although Shania has
				utils_npc.npc_generate_hp(npc)
				toee.game.particles("sp-Summon Monster I", npc)
				print("summoned sn_dying: {}, {}".format(npc.scripts[const_toee.sn_dying], npc))
			return npc

		count = 0
		if (do_summon(479, 471, "water1")): count += 1
		if (do_summon(482, 469, "water2")): count += 1
		if (do_summon(480, 474, "water3")): count += 1
		self.vars["quest_summon_1_count"] = count
		self.vars["quest_summon_1_left"] = count

		toee.game.global_vars[module_globals.GVAR_KEEP_QUORIS_SUMMON_1_STATE] = module_globals.GVAL_KEEP_QUORIS_SUMMON_1_STATE_COMBAT
		return

	def critter_dying(self, attachee, triggerer):
		assert isinstance(attachee, toee.PyObjHandle)
		info = self.get_monsterinfo_by_npc(attachee)
		#print("critter_dying attachee: {}, name: {}".format(attachee, info.monster_code_name))
		if (info and "water" in info.monster_code_name): 
			count = int(self.get_var("quest_summon_1_left"))
			#print("quest_summon_1_left: {}".format(count))
			count -= 1
			self.vars["quest_summon_1_left"] = count
			if (count <= 0):
				wiz_info, wiz_npc, wiz_ctrl = self.get_monsterinfo_and_npc_and_ctrl("keep", "wizard")
				#print("wiz_info, wiz_npc, wiz_ctrl: {}, {}, {}".format(wiz_info, wiz_npc, wiz_ctrl))
				if (wiz_ctrl and "do_summon_1_killed_all" in dir(wiz_ctrl)):
					#print("wiz_ctrl.do_summon_1_killed_all")
					wiz_ctrl.do_summon_1_killed_all(wiz_npc)

		super(CtrlKeepLv2, self).critter_dying(attachee, triggerer)
		return