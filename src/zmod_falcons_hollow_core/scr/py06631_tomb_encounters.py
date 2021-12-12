import toee, debug, tpdp, utils_storage, utils_npc_spells, const_toee, utils_tactics, const_proto_weapon, utils_item, const_proto_armor, const_proto_scrolls, ctrl_behaviour
import const_proto_potions, utils_obj, const_proto_food, utils_npc, utils_target_list, const_proto_wands, utils_sneak, const_deseases, utils_npc_spells, utils_npc
import const_proto_items, const_proto_rings, const_proto_cloth, const_proto_wondrous, utils_races, utils_npc_build, const_proto_npc, utils_npc_spells_tactics

THIS_SCRIPT_ID = 6631
def ctrl(npc): return ctrl_behaviour.get_ctrl(npc.id)
def san_start_combat(attachee, triggerer): return ctrl_behaviour.san_start_combat(attachee, triggerer)
def san_enter_combat(attachee, triggerer): return ctrl_behaviour.san_enter_combat(attachee, triggerer)
def san_end_combat(attachee, triggerer): return ctrl_behaviour.san_end_combat(attachee, triggerer)
def san_exit_combat(attachee, triggerer): return ctrl_behaviour.san_exit_combat(attachee, triggerer)
def san_will_kos(attachee, triggerer): return ctrl_behaviour.san_will_kos(attachee, triggerer)
def san_dialog(attachee, triggerer): return ctrl_behaviour.san_dialog(attachee, triggerer)
def san_heartbeat(attachee, triggerer): return ctrl_behaviour.san_heartbeat(attachee, triggerer)
def san_wield_off(attachee, triggerer): return ctrl_behaviour.san_wield_off(attachee, triggerer)

class CtrlShadow(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14828

	def created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		super(CtrlShadow, self).created(npc)
		npc.condition_add_with_args("Monster_Ability_Drain_Su", 0, 0, toee.stat_strength, toee.dice_new("1d6").packed, 0)
		npc.condition_add("Monster_Touch_Attack")
		#npc.condition_add("Monster_No_Damage")
		npc.condition_add_with_args("Monster Damage Type", toee.D20DT_SUBDUAL)
		return

class CtrlElementalWaterSmall(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14379

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		npc.scripts[const_toee.sn_enter_combat] = THIS_SCRIPT_ID
		return

class CtrlBelker(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14958

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		npc.scripts[const_toee.sn_enter_combat] = THIS_SCRIPT_ID
		return

class CtrlWight(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14929

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		npc.scripts[const_toee.sn_enter_combat] = THIS_SCRIPT_ID
		utils_npc.npc_skill_ensure(npc, toee.skill_hide, 8)

		atk_num = npc.obj_get_idx_int(toee.obj_f_critter_attacks_idx, 0)
		if (atk_num):
			#dmg_dice_packed = npc.obj_get_idx_int(toee.obj_f_critter_damage_idx, 0)
			dmg_dice = toee.dice_new("1d8")
			npc.obj_set_idx_int(toee.obj_f_critter_damage_idx, 0, dmg_dice.packed)

		#utils_item.item_create_in_inventory(const_proto_weapon.PROTO_LONGSWORD, npc)
		npc.item_wield_best_all()
		return

	def enter_combat(self, attachee, triggerer):
		#debug.breakp("enter_combat")
		#utils_sneak.npc_make_hide_and_surprise(attachee)
		return toee.RUN_DEFAULT

class CtrlWraith(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14959

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		npc.condition_add_with_args("Monster_Ability_Drain_Su", 0, 0, toee.stat_constitution, toee.dice_new("1d6").packed, 0)
		npc.condition_add("Monster_Touch_Attack")
		#npc.condition_add("Monster Incorporeal")
		npc.condition_add("Monster_Incorporeal2")
		
		return

class CtrlKoboldKing(ctrl_behaviour.CtrlBehaviourAI):
	@classmethod
	def get_proto_id(cls): return 14641

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		super(CtrlKoboldKing, self).after_created(npc)

		npc.scripts[const_toee.sn_enter_combat] = THIS_SCRIPT_ID
		npc.scripts[const_toee.sn_start_combat] = THIS_SCRIPT_ID

		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOAK_RED, npc)

		#npc.condition_add_with_args('Caster_Level_Mod', 15, 0, toee.spell_tashas_hideous_laughter)
		npc.feat_add(toee.feat_point_blank_shot)
		npc.feat_add(toee.feat_precise_shot)


		npc.item_wield_best_all()
		utils_npc.npc_generate_hp(npc)

		self.define_spells(npc)
		return

	def define_spells(self, npc):
		assert isinstance(npc, toee.PyObjHandle)

		stat_class = toee.stat_level_sorcerer
		stat_class = toee.domain_special
		caster_level = npc.highest_arcane_caster_level
		# 2
		#self.spells.add_spell(toee.spell_bulls_strength, stat_class, caster_level)
		#self.spells.add_spell(toee.spell_tashas_hideous_laughter, stat_class, caster_level)
		self.spells.add_spell(toee.spell_scorching_ray, stat_class, caster_level, 4)
		self.spells.add_spell(toee.spell_mirror_image, stat_class, caster_level)
		# 1
		self.spells.add_spell(toee.spell_mage_armor, stat_class, caster_level)
		self.spells.add_spell(toee.spell_magic_missile, stat_class, caster_level, 6)
		self.spells.add_spell(toee.spell_sleep, stat_class, caster_level)

		# 0
		self.spells.add_spell(toee.spell_daze, stat_class, caster_level)

		self.spells.memorize_all(npc)
		return
	
	def enter_combat(self, attachee, triggerer):
		#self.define_spells(attachee)
		return toee.RUN_DEFAULT

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		#debug.breakp("create_tactics")

		foes_adjacent = self._vars_tactics.get("foes_adjacent")
		assert isinstance(foes_adjacent, list)
		foes_threatening = self._vars_tactics.get("foes_threatening")
		assert isinstance(foes_threatening, list)

		tac = utils_tactics.TacticsHelper(self.get_name())
		
		target = npc.obj_get_obj(toee.obj_f_npc_who_hit_me_last)
		if (target and not utils_npc.npc_could_be_attacked(target)): target = None
		if (not target):
			target = self.tactics_determine_target(npc, 1)
		npc.obj_set_obj(toee.obj_f_npc_combat_focus, target)

		print("target: {}".format(target))
		while (target):
			if (not utils_npc_spells_tactics.STScorchingRay(npc, self.spells, tac, target).execute()):
				break
			if (not utils_npc_spells_tactics.STMagicMissle(npc, self.spells, tac, target).execute()):
				break
			tac.add_target_obj(target.id)
			tac.add_attack()
			tac.add_approach_single()
			tac.add_attack()
			tac.add_ready_vs_approach()
			tac.add_stop()
			break

		tac.add_total_defence()
		tac.add_stop()
		print("create_tactics {}".format(npc))
		return tac

	def do_spell_mage_armor(self):
		npc = self.npc_get()
		assert isinstance(npc, toee.PyObjHandle)
		npc.cast_spell(toee.spell_mage_armor, npc)
		return

	def do_spell_bull_strength(self):
		npc = self.npc_get()
		assert isinstance(npc, toee.PyObjHandle)
		npc.cast_spell(toee.spell_bulls_strength, npc)
		return

	def do_spell_mirror_image(self):
		npc = self.npc_get()
		assert isinstance(npc, toee.PyObjHandle)
		npc.cast_spell(toee.spell_mirror_image, npc)
		return