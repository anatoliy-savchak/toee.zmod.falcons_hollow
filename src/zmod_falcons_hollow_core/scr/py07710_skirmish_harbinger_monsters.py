import toee, debug, tpdp, utils_storage, utils_npc_spells, const_toee, utils_tactics, const_proto_weapon, utils_item, const_proto_armor, const_proto_scrolls, ctrl_behaviour, utils_toee
import const_proto_potions, utils_obj, const_proto_food, utils_npc, utils_target_list, const_proto_wands, utils_sneak, const_deseases, utils_npc_spells, utils_npc
import const_proto_items, const_proto_rings, const_proto_cloth, const_proto_wondrous, utils_races, utils_npc_build, const_proto_npc, utils_npc_spells_tactics

THIS_SCRIPT_ID = 7710
def ctrl(npc): return ctrl_behaviour.get_ctrl(npc.id)
def san_start_combat(attachee, triggerer): return ctrl_behaviour.san_start_combat(attachee, triggerer)
def san_enter_combat(attachee, triggerer): return ctrl_behaviour.san_enter_combat(attachee, triggerer)
def san_end_combat(attachee, triggerer): return ctrl_behaviour.san_end_combat(attachee, triggerer)
def san_exit_combat(attachee, triggerer): return ctrl_behaviour.san_exit_combat(attachee, triggerer)
def san_will_kos(attachee, triggerer): return ctrl_behaviour.san_will_kos(attachee, triggerer)
def san_dialog(attachee, triggerer): return ctrl_behaviour.san_dialog(attachee, triggerer)
def san_heartbeat(attachee, triggerer): return ctrl_behaviour.san_heartbeat(attachee, triggerer)
def san_wield_off(attachee, triggerer): return ctrl_behaviour.san_wield_off(attachee, triggerer)

class CtrlSkirmisher(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_commander_level(cls): return 0

	@classmethod
	def get_price(cls): return 0

	@classmethod
	def get_alignment_group(cls): return toee.ALIGNMENT_NEUTRAL

	def setup_name(self, npc, title):
		if (self.get_proto_id() // 1000 == 13):
			npc.obj_set_string(toee.obj_f_pc_player_name, title)
			return

		name_id = utils_toee.make_custom_name(title)
		if (name_id):
			npc.obj_set_int(toee.obj_f_critter_description_unknown, name_id)
			npc.obj_set_int(const_toee.obj_f_description_correct, name_id)
		return

	@staticmethod
	def _hide_loot(item):
		assert isinstance(item, toee.PyObjHandle)
		item.item_flag_set(toee.OIF_NO_LOOT)
		item.item_flag_set(toee.OIF_WONT_SELL)
		item.item_flag_set(toee.OIF_NO_PICKPOCKET)
		item.item_flag_set(toee.OIF_NO_DROP)
		item.item_flag_set(toee.OIF_NO_TRANSFER)
		return item

	@staticmethod
	def _lower_weight_small(item):
		assert isinstance(item, toee.PyObjHandle)
		item.obj_set_int(toee.obj_f_item_weight, item.obj_get_int(toee.obj_f_item_weight) // 2)
		return item

class CtrlSkirmisherLG(CtrlSkirmisher):
	@classmethod
	def get_alignment_group(cls): return toee.ALIGNMENT_LAWFUL_GOOD

class CtrlLGClericOfOrder(CtrlSkirmisherLG):
	# COMMANDER EFFECT: Followers rallied by this creature can take their turn normally if they	rally successfully.				
	# SPECIAL ABILITIES: Turn Undead 4 *.				
	# SPELLS: 1st-command ** (range 6; Stun; DC 13), shield of faith * (touch; +2 AC); 2nd—major resistance ** (touch; Save +3).
	#
	@classmethod
	def get_proto_id(cls): return const_proto_npc.PROTO_NPC_MAN #13000 #

	@classmethod
	def get_commander_level(cls): return 5

	@classmethod
	def get_price(cls): return 24

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)

		npc.make_class(toee.stat_level_cleric, 4)
		#AC 16 = 10 + 4 chain shirt + 2 dex
		#SPD 40 (6) should be light armor
		#HP 25 = 1d8 + 3d8 + 4*x => 8 + 1 + 4.5 + 1 + 4.5 + 1 + 4.5 + 1 = 8 + 4 + 13.5 = 25 => con: 12

		#STR: 12 due to atk is 4 = 3 bab (lv 4) + 1 str; but dmg will be 1d6+1 = 7 not 5!
		#DEX: 14 due to AC dex mod = 2
		#CON: 12, see HP calculation
		#WIS: 14 due to 1st level DC: 13 => 10 + 1 lv + 2 mod wis
		#INT: 08 any
		#CHA: 12 due to Turn undead 4 times = 3 + 1 mod cha

		utils_npc.npc_abilities_set(npc, [12, 14, 12, 8, 14, 12])

		npc.obj_set_int(toee.obj_f_critter_portrait, 1060) #ELM_1060_b_paladin
		npc.obj_set_int(toee.obj_f_critter_alignment, self.get_alignment_group())
		npc.obj_set_int(toee.obj_f_critter_deity, toee.DEITY_HEIRONEOUS)
		npc.obj_set_int(toee.obj_f_critter_domain_1, toee.good)
		npc.obj_set_int(toee.obj_f_critter_domain_1, toee.law)

		self.setup_name(npc, "Cleric of Order")

		hairStyle = utils_npc.HairStyle.from_npc(npc)
		hairStyle.style = const_toee.hair_style_shorthair
		hairStyle.color = const_toee.hair_color_white
		hairStyle.update_npc(npc)

		self._hide_loot(utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_BOOTS_CHAINMAIL_BOOTS, npc))
		self._hide_loot(utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_GLOVES_CHAINMAIL_GLOVES, npc))
		self._hide_loot(utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_CHAIN_SHIRT, npc))
		self._hide_loot(utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOAK_BLUE, npc))

		self._hide_loot(utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_QUARTERSTAFF, npc))

		npc.spells_memorized_forget()
		npc.spell_memorized_add(toee.spell_command, toee.stat_level_cleric, 1)
		npc.spell_memorized_add(toee.spell_command, toee.stat_level_cleric, 1)
		npc.spell_memorized_add(toee.spell_shield_of_faith, toee.stat_level_cleric, 1)

		npc.spell_memorized_add(toee.spell_resist_elements, toee.stat_level_cleric, 2)
		npc.spell_memorized_add(toee.spell_resist_elements, toee.stat_level_cleric, 2)
		npc.spells_pending_to_memorized()

		utils_npc.npc_generate_hp_avg_first(npc)
		npc.item_wield_best_all()
		return

class CtrlLGClericOfOrderAsPC(CtrlLGClericOfOrder):
	@classmethod
	def get_proto_id(cls): return const_proto_npc.PROTO_PC_HUMAN_MAN

class CtrlLGClericOfYondalla(CtrlSkirmisherLG):
	# COMMANDER EFFECT: Attack +2 against larger creatures. WARBAND BUILDING: Halflings of any faction are legal in your warband.
	# SPECIAL ABILITIES: Turn Undead 2 *.				
	# SPELLS: 1st-cure light wounds ** (touch; heal 5 hp), magic weapon * (touch; attack +1, ignore DR).
	#
	@classmethod
	def get_proto_id(cls): return const_proto_npc.PROTO_NPC_HALFLING_MAN

	@classmethod
	def get_commander_level(cls): return 3

	@classmethod
	def get_price(cls): return 14

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)

		npc.make_class(toee.stat_level_cleric, 2)
		#AC 23 = 10 + 8 full plate + 1 dex + 1 small being + 3 heavy shield +1
		#SPD 15 (2)
		#HP 15 = 1d8 + 1d8 + 2*x => 8 + 4 + 1 + 2*1 = 15 => con: 12

		#STR: 06 due to atk is 0 = 1 bab (lv 2) + 1 small - 2 str; dmg will be 1d6-1 = 5
		#DEX: 12 due to AC dex mod = 1
		#CON: 12, see HP calculation
		#WIS: 14 due to 1st level DC: 13 => 10 + 1 lv + 2 mod wis
		#INT: 08 any
		#CHA: 08 due to Turn undead 2 times = 3 - 1 mod cha

		utils_npc.npc_abilities_set(npc, [8, 10, 12, 12, 12, 8]) # -2 STR, +2 DEX

		npc.obj_set_int(toee.obj_f_critter_portrait, 10) #GNM_0010_b_illusionist
		npc.obj_set_int(toee.obj_f_critter_alignment, self.get_alignment_group())
		npc.obj_set_int(toee.obj_f_critter_deity, toee.DEITY_YONDALLA)
		npc.obj_set_int(toee.obj_f_critter_domain_1, toee.good)
		npc.obj_set_int(toee.obj_f_critter_domain_1, toee.protection)

		npc.feat_add(toee.feat_martial_weapon_proficiency_short_sword, 1)

		self.setup_name(npc, "Cleric of Yondalla")

		hairStyle = utils_npc.HairStyle.from_npc(npc)
		hairStyle.style = const_toee.hair_style_shorthair
		hairStyle.color = const_toee.hair_color_white
		hairStyle.update_npc(npc)

		self._lower_weight_small(self._hide_loot(utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_BOOTS_GILDED_BOOTS, npc)))
		self._lower_weight_small(self._hide_loot(utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_GLOVES_GILDED_GLOVES, npc)))
		self._lower_weight_small(self._hide_loot(utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_HELM_PLUMED_SILVER, npc)))
		self._lower_weight_small(self._hide_loot(utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_FULL_PLATE, npc)))
		item = self._lower_weight_small(self._hide_loot(utils_item.item_create_in_inventory(const_proto_armor.PROTO_SHIELD_LARGE_STEEL, npc)))
		item.item_condition_add_with_args("Shield Enhancement Bonus", 1)

		self._lower_weight_small(self._hide_loot(utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOAK_BLUE, npc)))

		self._lower_weight_small(self._hide_loot(utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_SHORTSWORD, npc)))

		npc.spells_memorized_forget()
		npc.spell_memorized_add(toee.spell_cure_light_wounds, toee.stat_level_cleric, 1)
		npc.spell_memorized_add(toee.spell_cure_light_wounds, toee.stat_level_cleric, 1)
		npc.spell_memorized_add(toee.spell_magic_weapon, toee.stat_level_cleric, 1)
		npc.spells_pending_to_memorized()

		utils_npc.npc_generate_hp_avg_first(npc)
		npc.item_wield_best_all()
		return

class CtrlLGClericOfYondallaAsPC(CtrlLGClericOfYondalla):
	@classmethod
	def get_proto_id(cls): return const_proto_npc.PROTO_PC_HALFLING_MAN
