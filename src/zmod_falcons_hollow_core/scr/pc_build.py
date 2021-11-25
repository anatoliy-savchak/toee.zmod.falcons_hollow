import toee, debug
import utils_item, const_proto_weapon, const_proto_armor, const_proto_cloth, const_proto_scrolls, const_proto_wondrous

# import pc_build
# pc_build.kots_b1()
def kots_b1():
	# 1: cleric
	# 2: fighter tank
	# 3: fighter dex
	# 4: wizard

	# fighter tank
	pc = toee.game.party[1]
	if (pc):
		#utils_item.item_create_in_inventory_buy(const_proto_weapon.PROTO_WEAPON_SWORD_BASTARD, pc)
		utils_item.item_create_in_inventory_buy(const_proto_armor.PROTO_ARMOR_BREASTPLATE_GOLD, pc)
		utils_item.item_create_in_inventory_buy(const_proto_armor.PROTO_SHIELD_LARGE_STEEL, pc)
		utils_item.item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_BOOTS_GOLD_BOOTS, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		pc.item_wield_best_all()

	# fighter dex
	pc = toee.game.party[2]
	if (pc):
		utils_item.item_create_in_inventory_buy(const_proto_weapon.PROTO_LONGSWORD, pc)
		utils_item.item_create_in_inventory_buy(const_proto_armor.PROTO_ARMOR_BANDED_MAIL, pc)
		utils_item.item_create_in_inventory_buy(const_proto_armor.PROTO_SHIELD_LARGE_STEEL_2, pc)
		utils_item.item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_BOOTS_GILDED_BOOTS, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		pc.item_wield_best_all()

	# cleric
	pc = toee.game.party[0]
	if (pc):
		utils_item.item_create_in_inventory_buy(const_proto_weapon.PROTO_WEAPON_CROSSBOW_LIGHT, pc)
		utils_item.item_create_in_inventory_buy(const_proto_weapon.PROTO_AMMO_BOLT_QUIVER, pc)
		
		utils_item.item_create_in_inventory_buy(const_proto_armor.PROTO_ARMOR_CHAIN_SHIRT, pc)
		utils_item.item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_BOOTS_GILDED_BOOTS, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		pc.item_wield_best_all()

	# wizard
	pc = toee.game.party[3]
	if (pc):
		utils_item.item_create_in_inventory_buy(const_proto_weapon.PROTO_WEAPON_CROSSBOW_LIGHT, pc)
		utils_item.item_create_in_inventory_buy(const_proto_weapon.PROTO_AMMO_BOLT_QUIVER, pc)
		
		utils_item.item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_BOOTS_MONK, pc)
		utils_item.item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_MONK_OUTFIT, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		pc.item_wield_best_all()

	return

def kots_b2():
	# what if all equipment is max out lv1
	# 1: cleric
	# 2: fighter tank
	# 3: fighter dex
	# 4: wizard

	# fighter tank
	pc = toee.game.party[1]
	if (pc):
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_SWORD_BASTARD_MASTERWORK, pc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_FULL_PLATE, pc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_SHIELD_LARGE_STEEL, pc)
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_BOOTS_GILDED_BOOTS, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		utils_item.item_clear_by_proto(pc, const_proto_weapon.PROTO_WEAPON_SWORD_BASTARD)
		pc.item_wield_best_all()

	# fighter dex
	pc = toee.game.party[2]
	if (pc):
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_LONGSWORD_MASTERWORK, pc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_FULL_PLATE, pc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_SHIELD_LARGE_STEEL_2, pc)
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_BOOTS_GILDED_BOOTS, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		pc.item_wield_best_all()

	# cleric
	pc = toee.game.party[0]
	if (pc):
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_CROSSBOW_LIGHT_MASTERWORK, pc)
		item = utils_item.item_create_in_inventory(const_proto_weapon.PROTO_AMMO_BOLT_QUIVER, pc)
		if (item):
			item.obj_set_int(toee.obj_f_ammo_quantity, 50)

		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_MACE_LIGHT_MASTERWORK, pc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_SHIELD_SMALL_STEEL, pc)
		
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_FULL_PLATE, pc)
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_BOOTS_GILDED_BOOTS, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		pc.item_wield_best_all()

	# wizard
	pc = toee.game.party[3]
	if (pc):
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_CROSSBOW_LIGHT_MASTERWORK, pc)
		item = utils_item.item_create_in_inventory(const_proto_weapon.PROTO_AMMO_BOLT_QUIVER, pc)
		if (item):
			item.obj_set_int(toee.obj_f_ammo_quantity, 50)
		
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_BOOTS_MONK, pc)
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_MONK_OUTFIT, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		pc.item_wield_best_all()

	return

# import pc_build
# pc_build.kots_b3()
def kots_b3():
	# 1: cleric
	# 2: fighter tank
	# 3: fighter dex
	# 4: wizard

	# instead of cleric armor buy her used acid splash

	# fighter tank
	pc = toee.game.party[1]
	if (pc):
		#utils_item.item_create_in_inventory_buy(const_proto_weapon.PROTO_WEAPON_SWORD_BASTARD, pc)
		utils_item.item_create_in_inventory_buy(const_proto_armor.PROTO_ARMOR_BREASTPLATE_GOLD, pc)
		utils_item.item_create_in_inventory_buy(const_proto_armor.PROTO_SHIELD_LARGE_STEEL, pc)
		utils_item.item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_BOOTS_GOLD_BOOTS, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		pc.item_wield_best_all()

	# fighter dex
	pc = toee.game.party[2]
	if (pc):
		utils_item.item_create_in_inventory_buy(const_proto_weapon.PROTO_LONGSWORD, pc)
		utils_item.item_create_in_inventory_buy(const_proto_armor.PROTO_ARMOR_BANDED_MAIL, pc)
		utils_item.item_create_in_inventory_buy(const_proto_armor.PROTO_SHIELD_LARGE_STEEL_2, pc)
		utils_item.item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_BOOTS_GILDED_BOOTS, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		pc.item_wield_best_all()

	# cleric
	pc = toee.game.party[0]
	if (pc):
		#utils_item.item_create_in_inventory_buy(const_proto_weapon.PROTO_WEAPON_CROSSBOW_LIGHT, pc)
		#utils_item.item_create_in_inventory_buy(const_proto_weapon.PROTO_AMMO_BOLT_QUIVER, pc)
		
		#utils_item.item_create_in_inventory_buy(const_proto_armor.PROTO_ARMOR_CHAIN_SHIRT, pc)
		#utils_item.item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_BOOTS_GILDED_BOOTS, pc)
		#utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		pc.item_wield_best_all()

	# wizard
	pc = toee.game.party[3]
	if (pc):
		utils_item.item_create_in_inventory_buy(const_proto_weapon.PROTO_WEAPON_CROSSBOW_LIGHT, pc)
		utils_item.item_create_in_inventory_buy(const_proto_weapon.PROTO_AMMO_BOLT_QUIVER, pc)
		
		utils_item.item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_BOOTS_MONK, pc)
		utils_item.item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_MONK_OUTFIT, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		pc.item_wield_best_all()

	return

def kots_b4():
	# 1: cleric
	# 2: fighter tank
	# 3: fighter dex
	# 4: wizard

	# fighter tank
	pc = toee.game.party[1]
	if (pc):
		#utils_item.item_create_in_inventory_buy(const_proto_weapon.PROTO_WEAPON_SWORD_BASTARD, pc)
		utils_item.item_create_in_inventory_buy(const_proto_armor.PROTO_ARMOR_BREASTPLATE_GOLD, pc)
		utils_item.item_create_in_inventory_buy(const_proto_armor.PROTO_SHIELD_LARGE_STEEL, pc)
		utils_item.item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_BOOTS_GOLD_BOOTS, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		pc.item_wield_best_all()

	# fighter dex
	pc = toee.game.party[2]
	if (pc):
		utils_item.item_create_in_inventory_buy(const_proto_weapon.PROTO_WEAPON_GUISARME, pc)
		utils_item.item_create_in_inventory_buy(const_proto_armor.PROTO_ARMOR_BANDED_MAIL, pc)
		utils_item.item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_BOOTS_GILDED_BOOTS, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		pc.item_wield_best_all()

	# cleric
	pc = toee.game.party[0]
	if (pc):
		utils_item.item_create_in_inventory_buy(const_proto_weapon.PROTO_WEAPON_CROSSBOW_LIGHT, pc)
		utils_item.item_create_in_inventory_buy(const_proto_weapon.PROTO_AMMO_BOLT_QUIVER, pc)
		
		utils_item.item_create_in_inventory_buy(const_proto_armor.PROTO_ARMOR_CHAIN_SHIRT, pc)
		utils_item.item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_BOOTS_GILDED_BOOTS, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		pc.item_wield_best_all()

	# wizard
	pc = toee.game.party[3]
	if (pc):
		utils_item.item_create_in_inventory_buy(const_proto_weapon.PROTO_WEAPON_CROSSBOW_LIGHT, pc)
		utils_item.item_create_in_inventory_buy(const_proto_weapon.PROTO_AMMO_BOLT_QUIVER, pc)
		
		utils_item.item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_BOOTS_MONK, pc)
		utils_item.item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_MONK_OUTFIT, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)

		utils_item.item_create_in_inventory_buy(const_proto_scrolls.PROTO_SCROLL_OF_ENLARGE_PERSON, pc)
		
		pc.item_wield_best_all()

	return

# import pc_build
# pc_build.kots_c1()

def kots_c1():
	# 1: barbarian
	# 2: fighter dex
	# 3: cleric
	# 4: wizard

	# fighter tank
	pc = toee.game.party[0]
	if (pc):
		utils_item.item_create_in_inventory_buy(const_proto_weapon.PROTO_WEAPON_GREATAXE, pc)
		utils_item.item_create_in_inventory_buy(const_proto_armor.PROTO_ARMOR_BREASTPLATE, pc)
		utils_item.item_create_in_inventory_buy(const_proto_armor.PROTO_SHIELD_BUCKLER, pc)
		utils_item.item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_BOOTS_SILVER_PLATE_BOOTS, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		pc.item_wield_best_all()

	# fighter dex
	pc = toee.game.party[1]
	if (pc):
		utils_item.item_create_in_inventory_buy(const_proto_weapon.PROTO_WEAPON_GUISARME, pc)
		utils_item.item_create_in_inventory_buy(const_proto_armor.PROTO_ARMOR_BANDED_MAIL, pc)
		utils_item.item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_BOOTS_GILDED_BOOTS, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		pc.item_wield_best_all()

	# cleric
	pc = toee.game.party[2]
	if (pc):
		#utils_item.item_create_in_inventory_buy(const_proto_weapon.PROTO_WEAPON_CROSSBOW_LIGHT, pc)
		#utils_item.item_create_in_inventory_buy(const_proto_weapon.PROTO_AMMO_BOLT_QUIVER, pc)
		
		utils_item.item_create_in_inventory_buy(const_proto_armor.PROTO_SHIELD_LARGE_WOODEN, pc)
		utils_item.item_create_in_inventory_buy(const_proto_armor.PROTO_ARMOR_CHAIN_SHIRT, pc)
		utils_item.item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_BOOTS_GILDED_BOOTS, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		pc.item_wield_best_all()

	# wizard
	pc = toee.game.party[3]
	if (pc):
		utils_item.item_create_in_inventory_buy(const_proto_weapon.PROTO_WEAPON_CROSSBOW_LIGHT, pc)
		item = utils_item.item_create_in_inventory(const_proto_weapon.PROTO_AMMO_BOLT_QUIVER, pc)
		if (item):
			item.obj_set_int(toee.obj_f_ammo_quantity, 50)
		
		utils_item.item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_BOOTS_MONK, pc)
		utils_item.item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_MONK_OUTFIT, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)

		#utils_item.item_create_in_inventory_buy(const_proto_scrolls.PROTO_SCROLL_OF_ENLARGE_PERSON, pc)
		
		pc.item_wield_best_all()

	return

# import pc_build
# pc_build.kots_l1()

def kots_l1():
	# 1: fighter bastard
	# 2: fighter longsword
	# 3: cleric
	# 4: wizard

	# fighter tank
	pc = toee.game.party[0]
	if (pc):
		utils_item.item_create_in_inventory_buy(const_proto_armor.PROTO_ARMOR_CHAIN_SHIRT, pc)
		utils_item.item_create_in_inventory_buy(const_proto_armor.PROTO_SHIELD_LARGE_STEEL, pc)
		utils_item.item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_BOOTS_SILVER_PLATE_BOOTS, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		pc.item_wield_best_all()

	# fighter dex
	pc = toee.game.party[1]
	if (pc):
		utils_item.item_create_in_inventory_buy(const_proto_weapon.PROTO_LONGSWORD, pc)
		utils_item.item_create_in_inventory_buy(const_proto_armor.PROTO_ARMOR_CHAIN_SHIRT, pc)
		utils_item.item_create_in_inventory_buy(const_proto_armor.PROTO_SHIELD_LARGE_STEEL_2, pc)
		utils_item.item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_BOOTS_SILVER_PLATE_BOOTS, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		pc.item_wield_best_all()

	# cleric
	pc = toee.game.party[2]
	if (pc):
		utils_item.item_create_in_inventory_buy(const_proto_weapon.PROTO_WEAPON_MORNINGSTAR, pc)
		utils_item.item_create_in_inventory_buy(const_proto_armor.PROTO_ARMOR_CHAIN_SHIRT, pc)
		utils_item.item_create_in_inventory_buy(const_proto_armor.PROTO_SHIELD_SMALL_WOODEN, pc)
		utils_item.item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_BOOTS_SILVER_PLATE_BOOTS, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		pc.item_wield_best_all()

	# wizard
	pc = toee.game.party[3]
	if (pc):
		utils_item.item_create_in_inventory_buy(const_proto_weapon.PROTO_WEAPON_CROSSBOW_LIGHT, pc)
		item = utils_item.item_create_in_inventory(const_proto_weapon.PROTO_AMMO_BOLT_QUIVER, pc)
		if (item):
			item.obj_set_int(toee.obj_f_ammo_quantity, 50)
		
		utils_item.item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_BOOTS_MONK, pc)
		utils_item.item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_MONK_OUTFIT, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)

		#utils_item.item_create_in_inventory_buy(const_proto_scrolls.PROTO_SCROLL_OF_ENLARGE_PERSON, pc)
		
		pc.item_wield_best_all()

	return

def hallow_l1():
	# 1: ostap pal
	# 2: roman rogue fighter 4
	# 3: eug warmage
	# 4: vol cleric
	# 5: andr barb

	# paladin
	pc = toee.game.party[0]
	if (pc):
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_FULL_PLATE, pc)
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_BATTLEAXE_PLUS_1, pc)
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_GLOVES_LEATHER_BROWN, pc)
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_BOOTS_SILVER_PLATE_BOOTS, pc)
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_HELM_PLUMED_SILVER, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		utils_item.item_create_in_inventory(const_proto_wondrous.PROTO_WONDROUS_GAUNTLETS_OF_OGRE_POWER, pc)
		utils_item.item_create_in_inventory(const_proto_wondrous.PROTO_WONDROUS_AMULET_OF_NATURAL_ARMOR_PLUS_2, pc)
		utils_item.item_create_in_inventory(const_proto_wondrous.PROTO_WONDROUS_CLOAK_OF_CHARISMA_PLUS_2_WHITE, pc)

		pc.item_wield_best_all()

	# fighter
	pc = toee.game.party[1]
	if (pc):
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_BATTLEAXE_PLUS_1, pc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_FULL_PLATE_MITHRAL, pc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_SHIELD_BUCKLER, pc)
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_BOOTS_SILVER_PLATE_BOOTS, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		pc.item_wield_best_all()

	# warmage
	pc = toee.game.party[2]
	if (pc):
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_CROSSBOW_LIGHT, pc)
		item = utils_item.item_create_in_inventory(const_proto_weapon.PROTO_AMMO_BOLT_QUIVER, pc)
		if (item):
			item.obj_set_int(toee.obj_f_ammo_quantity, 50)
		
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_BOOTS_MONK, pc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_STUDDED_LEATHER_ARMOR_MASTERWORK, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		utils_item.item_create_in_inventory(const_proto_wondrous.PROTO_WONDROUS_CLOAK_OF_RESISTANCE_PLUS_2_BLUE, pc)

		#utils_item.item_create_in_inventory(const_proto_scrolls.PROTO_SCROLL_OF_ENLARGE_PERSON, pc)
		
		pc.item_wield_best_all()

	# cleric
	pc = toee.game.party[3]
	if (pc):
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_MORNINGSTAR, pc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_FULL_PLATE, pc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_SHIELD_SMALL_WOODEN, pc)
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_BOOTS_SILVER_PLATE_BOOTS, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		pc.item_wield_best_all()

	# barb
	pc = toee.game.party[4]
	if (pc):
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_GREATAXE_PLUS_1, pc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_STUDDED_LEATHER_ARMOR_PLUS_2, pc)
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_BOOTS_LEATHER_BOOTS_COMBAT, pc)
		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		pc.item_wield_best_all()

	return

