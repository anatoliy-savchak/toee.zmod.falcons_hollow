import toee, debug, tpdp, utils_storage, utils_npc_spells, const_toee, utils_tactics, const_proto_weapon, utils_item, const_proto_armor, const_proto_scrolls, ctrl_behaviour
import const_proto_potions, utils_obj, const_proto_food, utils_npc, utils_target_list, const_proto_wands, utils_sneak, const_deseases, utils_npc_spells, utils_npc
import const_proto_items, const_proto_rings, const_proto_cloth, const_proto_wondrous, utils_races, utils_npc_build, const_proto_npc, utils_toee, tpai, tpactions, utils_strategy
import py06620_daemon_battlefield1, py04000_monster_manual1_p1, utils_npc_spells_tactics

MODULE_SCRIPT_ID = 6621

def san_start_combat(attachee, triggerer): return ctrl_behaviour.san_start_combat(attachee, triggerer)
def san_enter_combat(attachee, triggerer): return ctrl_behaviour.san_enter_combat(attachee, triggerer)
def san_end_combat(attachee, triggerer): return ctrl_behaviour.san_end_combat(attachee, triggerer)
def san_exit_combat(attachee, triggerer): return ctrl_behaviour.san_exit_combat(attachee, triggerer)
def san_will_kos(attachee, triggerer): return ctrl_behaviour.san_will_kos(attachee, triggerer)
def san_dialog(attachee, triggerer): return ctrl_behaviour.san_dialog(attachee, triggerer)
def san_heartbeat(attachee, triggerer): return ctrl_behaviour.san_heartbeat(attachee, triggerer)
def san_wield_off(attachee, triggerer): return ctrl_behaviour.san_wield_off(attachee, triggerer)

def cs(): return py06620_daemon_battlefield1.cs()

class CtrlOrc(ctrl_behaviour.CtrlBehaviourAI):
	@classmethod
	def get_proto_id(cls): return 14899

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		npc.scripts[const_toee.sn_start_combat] = MODULE_SCRIPT_ID
		npc.scripts[const_toee.sn_enter_combat] = MODULE_SCRIPT_ID

		utils_npc_build.NPCAbilitiesSetup(6, 12, utils_races.RACE_ABILITY_BONUSES_ORC).generate().focus_melee().npc_setup_random(npc)
		self.generate_hp(npc)

		# create inventory
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_LEATHER_ARMOR_BROWN, npc)
		item = utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_BOOTS_LEATHER_BOOTS_COMBAT, npc)
		if (item):
			item.item_flag_set(toee.OIF_NO_LOOT)
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_FALCHION, npc)
		npc.item_wield_best_all()
		return

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		tac = utils_tactics.TacticsHelper(self.get_name())

		num = self.get_var('num', 0)
		if (num < 1 or num > 3): return None

		foes = self.tactics_get_foes()
		loc = cs().chess(5, 1 + num)
		print(loc)
		abs_x, abs_y = loc.get_overall_offset()
		tac.add_move_to(abs_x, abs_y)
		#tac.add_goto_loc(loc.get_location())
		tac.add_target_obj(foes[0].id)
		tac.add_strike()
		tac.add_stop()
		return tac
