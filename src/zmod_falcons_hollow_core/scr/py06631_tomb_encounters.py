import toee, debug, tpdp, utils_storage, utils_npc_spells, const_toee, utils_tactics, const_proto_weapon, utils_item, const_proto_armor, const_proto_scrolls, ctrl_behaviour
import const_proto_potions, utils_obj, const_proto_food, utils_npc, utils_target_list, const_proto_wands, utils_sneak, const_deseases, utils_npc_spells, utils_npc
import const_proto_items, const_proto_rings, const_proto_cloth, const_proto_wondrous, utils_races, utils_npc_build, const_proto_npc

THIS_SCRIPT_ID = 06631
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