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

		utils_npc.npc_hitdice_set(npc, 0, 0, 0)
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

		utils_npc.npc_hitdice_set(npc, 0, 0, 0)
		npc.make_class(toee.stat_level_cleric, 2)
		#AC 23 = 10 + 8 full plate + 1 dex + 1 small being + 3 heavy shield +1
		#SPD 15 (2)
		#HP 15 = 1d8 + 1d8 + 2*x => 8 + 4 + 1 + 2*1 = 15 => con: 12

		#STR: 06 due to atk is 0 = 1 bab (lv 2) + 1 small - 2 str; dmg will be 1d6-2 = 4 not 5!
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
		hairStyle.color = const_toee.hair_color_brown
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

class CtrlLGDwarfAxefighter(CtrlSkirmisherLG):
	# SPECIAL ABILITIES: Cleave; Save +4.
	@classmethod
	def get_proto_id(cls): return const_proto_npc.PROTO_NPC_DWARF_MAN

	@classmethod
	def get_price(cls): return 12

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)

		utils_npc.npc_hitdice_set(npc, 0, 0, 0)
		npc.make_class(toee.stat_level_fighter, 3)
		#AC 19 = 10 + 5 chain mail + 2 dex + 2 heavy shield
		#SPD 20 (4)
		#HP 30 = 1d10 + 2d10 + 3*x => 10 + 2*10/2 + 1 + 3*2 = 31 => con: 14

		#STR: 16 due to atk is 7 = 3 bab (lv 3) + 2 str + 1 wpn foc + 1 mkw; dmg will be 1d8 + 2 = 10
		#DEX: 12 due to AC dex mod = 1
		#CON: 12, see HP calculation
		#WIS: 12 any
		#INT: 08 any
		#CHA: 08 due to Turn undead 2 times = 3 - 1 mod cha

		utils_npc.npc_abilities_set(npc, [14, 14, 12, 8, 12, 8]) # -2 CHA, +2 CON

		npc.obj_set_int(toee.obj_f_critter_portrait, 2000) #DWM_2000_b_fighter
		npc.obj_set_int(toee.obj_f_critter_alignment, self.get_alignment_group())
		npc.obj_set_int(toee.obj_f_critter_deity, toee.DEITY_HEIRONEOUS)

		npc.feat_add(toee.feat_weapon_focus_battleaxe, 0)
		npc.feat_add(toee.feat_cleave, 1)

		self.setup_name(npc, "Dwarf Axefighter")

		hairStyle = utils_npc.HairStyle.from_npc(npc)
		hairStyle.style = const_toee.hair_style_shorthair
		hairStyle.color = const_toee.hair_color_red
		hairStyle.update_npc(npc)

		self._hide_loot(utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_BOOTS_CHAINMAIL_BOOTS, npc))
		self._hide_loot(utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_GLOVES_CHAINMAIL_GLOVES, npc))
		self._hide_loot(utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_HELMET_CHAIN, npc))
		self._hide_loot(utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_CHAINMAIL, npc))
		self._hide_loot(utils_item.item_create_in_inventory(const_proto_armor.PROTO_SHIELD_LARGE_STEEL, npc))

		self._hide_loot(utils_item.item_create_in_inventory(const_proto_weapon.PROTO_BATTLEAXE_MASTERWORK, npc))

		utils_npc.npc_generate_hp_avg_first(npc)
		npc.item_wield_best_all()
		return

class CtrlLGEmberHumanMonk(CtrlSkirmisherLG):
	# SPECIAL ABILITIES: Unique. Deflect Arrows (+4 AC against ranged attacks); Mobility (+4 AC against attacks of opportunity); Save +4; Stunning Attack ** (DC 15).
	@classmethod
	def get_proto_id(cls): return const_proto_npc.PROTO_NPC_WOMAN

	@classmethod
	def get_price(cls): return 18

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)

		utils_npc.npc_hitdice_set(npc, 0, 0, 0)
		npc.make_class(toee.stat_level_monk, 6)
		#AC 19 = 10 + 2 wis + 4 dex + 1 monk
		#SPD 20 (4)
		#HP 30 = 1d8 + 5d8 + 3*x => 8 + 5*(8+1)/2 + 6*1 = 36 => con: 12

		#STR: 16 due to atk is 7 = 4 bab (lv 6) + 1 str + 2 wpn foc + 1 magic - 1 flurry; dmg will be 1d6 + 2 = 8
		#DEX: 18 due to AC dex mod = 4
		#CON: 12, see HP calculation
		#WIS: 14 due to AC wis bonus = 2
		#INT: 08 any
		#CHA: 08 any

		utils_npc.npc_abilities_set(npc, [12, 18, 12, 8, 14, 8]) 

		npc.obj_set_int(toee.obj_f_critter_portrait, 570) #HUF_0570_b_monk
		npc.obj_set_int(toee.obj_f_critter_alignment, self.get_alignment_group())
		npc.obj_set_int(toee.obj_f_critter_deity, toee.DEITY_HEIRONEOUS)

		npc.feat_add(toee.feat_weapon_focus_quarterstaff, 0)
		npc.feat_add(toee.feat_greater_weapon_focus_quarterstaff, 0)
		npc.feat_add(toee.feat_dodge, 0)
		npc.feat_add(toee.feat_weapon_finesse_quarterstaff, 0)
		npc.feat_add(toee.feat_mobility, 1)

		self.setup_name(npc, "Ember, Human Monk")

		hairStyle = utils_npc.HairStyle.from_npc(npc)
		hairStyle.style = const_toee.hair_style_ponytail
		hairStyle.color = const_toee.hair_color_black
		hairStyle.update_npc(npc)

		self._hide_loot(utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_BOOTS_MONK, npc))
		self._hide_loot(utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_MONK_OUTFIT, npc))
		
		self._hide_loot(utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_MONK_OUTFIT, npc))

		self._hide_loot(utils_item.item_create_in_inventory(const_proto_wondrous.PROTO_WONDROUS_BRACERS_OF_ARMOR_PLUS_2, npc))
		#self._hide_loot(utils_item.item_create_in_inventory(const_proto_wondrous.PROTO_WONDROUS_AMULET_OF_NATURAL_ARMOR_PLUS_1, npc))

		item = self._hide_loot(utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_QUARTERSTAFF, npc))
		item.item_condition_add_with_args("Weapon Enhancement Bonus", 1)

		utils_npc.npc_generate_hp_avg_first(npc)
		npc.item_wield_best_all()
		return

class CtrlLGEvokersApprentice(CtrlSkirmisherLG):
	# SPELLS: 1st—magic missile * (sight; 5 damage), magic weapon * (touch; attack +1, ignore DR).
	#
	@classmethod
	def get_proto_id(cls): return const_proto_npc.PROTO_NPC_MAN #13000 #

	@classmethod
	def get_price(cls): return 10

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)

		utils_npc.npc_hitdice_set(npc, 0, 0, 0)
		npc.make_class(toee.stat_level_wizard, 1)
		#AC 12 = 10 + 2 dex
		#SPD 30 (6) should be light armor
		#HP 5 = 1d4 + 1 => con: 12

		#STR: 8 atk 0
		#DEX: 14 due to AC dex mod = 2
		#CON: 12, see HP calculation
		#INT: 12 wiz
		#WIS: 12 
		#CHA: 8 any

		utils_npc.npc_abilities_set(npc, [10, 14, 12, 12, 12, 8])

		npc.obj_set_int(toee.obj_f_critter_portrait, 6200) #NPC_6201_m_Mickey
		npc.obj_set_int(toee.obj_f_critter_alignment, self.get_alignment_group())
		npc.obj_set_int(toee.obj_f_critter_deity, toee.DEITY_HEIRONEOUS)

		self.setup_name(npc, "Evoker's Apprentice")

		hairStyle = utils_npc.HairStyle.from_npc(npc)
		hairStyle.style = const_toee.hair_style_shorthair
		hairStyle.color = const_toee.hair_color_blonde
		hairStyle.update_npc(npc)

		self._hide_loot(utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_BOOTS_LEATHER_BOOTS_WHITE, npc))
		self._hide_loot(utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_ROBES_GREEN, npc))
		self._hide_loot(utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_CIRCLET_HOODLESS, npc))
		
		self._hide_loot(utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_QUARTERSTAFF, npc))

		npc.spells_memorized_forget()
		npc.spell_memorized_add(toee.spell_magic_missile, toee.stat_level_wizard, 1)
		npc.spell_memorized_add(toee.spell_magic_weapon, toee.stat_level_wizard, 1)
		npc.spells_pending_to_memorized()

		utils_npc.npc_generate_hp_avg_first(npc)
		npc.item_wield_best_all()
		return

class CtrlLGHalflingVeteran(CtrlSkirmisherLG):
	@classmethod
	def get_proto_id(cls): return const_proto_npc.PROTO_NPC_HALFLING_MAN

	@classmethod
	def get_price(cls): return 11

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)

		utils_npc.npc_hitdice_set(npc, 0, 0, 0)
		npc.make_class(toee.stat_level_fighter, 5)
		#AC 19 = 10 + 5 chain mail + 2 dex + 1 dodge + 1 twd
		#SPD 20 (4)
		#HP 35 = 1d10 + 4d10 + 3*x => 32 + 5*1 = 37 => con: 12

		#STR: 14 due to atk is 9 = 5 bab (lv 5) + 4 dex + 1 wpf + 1 mkw - 2 twf; dmg will be 1d4 + 1 = 5, str-2
		#DEX: 18 due to AC dex mod = 3 and 4 finesse
		#CON: 12, see HP calculation
		#INT: 08 any
		#WIS: 10
		#CHA: 08 any

		utils_npc.npc_abilities_set(npc, [14, 16, 12, 8, 10, 8]) # -2 STR, +2 DEX

		npc.obj_set_int(toee.obj_f_critter_portrait, 2500) #HAM_2500_b_rogue
		npc.obj_set_int(toee.obj_f_critter_alignment, self.get_alignment_group())
		npc.obj_set_int(toee.obj_f_critter_deity, toee.DEITY_HEIRONEOUS)

		#npc.feat_add(toee.feat_weapon_focus_dagger, 0)
		#npc.feat_add(toee.feat_greater_weapon_focus_quarterstaff, 0)
		npc.feat_add(toee.feat_dodge, 0)
		npc.feat_add(toee.feat_weapon_finesse_dagger, 0)
		npc.feat_add(toee.feat_two_weapon_fighting, 1)

		self.setup_name(npc, "Halfling Veteran")

		hairStyle = utils_npc.HairStyle.from_npc(npc)
		hairStyle.style = const_toee.hair_style_shorthair
		hairStyle.color = const_toee.hair_color_black
		hairStyle.update_npc(npc)

		self._lower_weight_small(self._hide_loot(utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_BOOTS_CHAINMAIL_BOOTS, npc)))
		self._lower_weight_small(self._hide_loot(utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_GLOVES_CHAINMAIL_GLOVES, npc)))
		#self._lower_weight_small(self._hide_loot(utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_HELMET_CHAIN, npc)))
		self._lower_weight_small(self._hide_loot(utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_CHAINMAIL, npc)))

		dagger1 = self._hide_loot(utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_DAGGER_MASTERWORK, npc))
		dagger2 = self._hide_loot(utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_DAGGER_MASTERWORK, npc))

		utils_npc.npc_generate_hp_avg_first(npc)
		npc.item_wield_best_all()
		npc.item_wield(dagger1, toee.item_wear_weapon_primary)
		npc.item_wield(dagger2, toee.item_wear_weapon_secondary)
		return

class CtrlLGHoundArchon(CtrlSkirmisherLG):
	@classmethod
	def get_proto_id(cls): return const_proto_npc.PROTO_NPC_JACKALWERE_EMPTY

	@classmethod
	def get_price(cls): return 31

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)

		utils_npc.npc_hitdice_set(npc, 6, 8, 0)
		utils_npc.npc_abilities_set(npc, [15, 10, 13, 10, 13, 12])

		#npc.obj_set_int(toee.obj_f_critter_portrait, 2500) #HAM_2500_b_rogue
		npc.obj_set_int(toee.obj_f_critter_alignment, self.get_alignment_group())
		npc.obj_set_int(toee.obj_f_critter_deity, toee.DEITY_HEIRONEOUS)
		npc.obj_set_int(toee.obj_f_npc_ac_bonus, 9) # natural ac
		npc.obj_set_int(toee.obj_f_npc_save_fortitude_bonus, 5)
		npc.obj_set_int(toee.obj_f_npc_save_reflexes_bonus, 5)
		npc.obj_set_int(toee.obj_f_npc_save_willpower_bonus, 5)

		npc.feat_add(toee.feat_improved_initiative, 0)
		npc.feat_add(toee.feat_power_attack, 1)

		#npc.condition_add_with_args("Base_Attack_Bonus1", 5)
		#npc.condition_add("Base_Attack_Bonus5")
		npc.condition_add_with_args("Spell Resistance", 16)
		npc.condition_add_with_args("Monster DR Magic", 5)

		self.setup_name(npc, "Hound Archon")
		self._hide_loot(utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_GREATSWORD, npc))

		utils_npc.npc_generate_hp_avg_first(npc, 0)
		npc.item_wield_best_all()
		return
