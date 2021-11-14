import toee, debug, tpdp, utils_toee, utils_storage, utils_obj, utils_item, const_toee, ctrl_daemon, ctrl_daemon2
import ctrl_behaviour, py06122_cormyr_prompter, factions_zmod, utils_npc
import monster_info, module_quests, module_consts
import py06621_battlefield1_monsters, py04000_monster_manual1_p1, math, utils_path, tpai

DAEMON_SCRIPT_ID = 6620
DAEMON_GID = "G_79D55646_C440_472E_A0EA_BF66F5DB9C40"
DEBUG = 0
DEBUG_NAMES = 1

# import module_consts
# game.fade_and_teleport( 0, 0, 0, module_consts.MAP_ID_ZMOD_BATTLEFIELD1, module_consts.ZMOD_BATTLEFIELD1_ENTRY1[0], module_consts.ZMOD_BATTLEFIELD1_ENTRY1[1])
# game.fade_and_teleport( 0, 0, 0, module_consts.MAP_ID_SHOP_MAP, module_consts.ZMOD_SHOPMAP_ENTRY1[0], module_consts.ZMOD_SHOPMAP_ENTRY1[1])
# import py06620_daemon_battlefield1
# 
# py06620_daemon_battlefield1.cs().pc_step()
# py06620_daemon_battlefield1.cs().pc_goto_square2(1, 1)
# pq, pqr = py06620_daemon_battlefield1.cs().pc_goto_square_from_dir(1)
# pq, pqr = py06620_daemon_battlefield1.cs().pc_goto_square_from_dir(1, 5, 0)
# py06620_daemon_battlefield1.cs().pc_goto_square_from_dir_get(1)

def san_new_map(attachee, triggerer):
	return ctrl_daemon2.do_san_new_map(attachee, triggerer, module_consts.MAP_ID_ZMOD_BATTLEFIELD1, CtrlBattlefield1)

def san_first_heartbeat(attachee, triggerer):
	return ctrl_daemon2.do_san_first_heartbeat(attachee, triggerer, module_consts.MAP_ID_ZMOD_BATTLEFIELD1, CtrlBattlefield1)

def san_heartbeat(attachee, triggerer):
	return ctrl_daemon2.do_san_heartbeat(attachee, triggerer, module_consts.MAP_ID_ZMOD_BATTLEFIELD1, cs())

def san_dying(attachee, triggerer):
	return ctrl_daemon2.do_san_dying(attachee, triggerer, module_consts.MAP_ID_ZMOD_BATTLEFIELD1, cs())

def san_use(attachee, triggerer):
	return ctrl_daemon2.do_san_use(attachee, triggerer, module_consts.MAP_ID_ZMOD_BATTLEFIELD1, cs())

def san_bust(attachee, triggerer):
	return ctrl_daemon2.do_san_bust(attachee, triggerer, module_consts.MAP_ID_ZMOD_BATTLEFIELD1, cs())

def cs():
	o = utils_storage.obj_storage_by_id(DAEMON_GID)
	if (not o): 
		return None
	result = o.data.get(CtrlBattlefield1.get_name())
	assert isinstance(result, CtrlBattlefield1)
	return result

class CtrlBattlefield1(ctrl_daemon2.CtrlDaemon2):
	def created(self, npc):
		self.init_daemon2_fields(module_consts.MAP_ID_ZMOD_BATTLEFIELD1, DAEMON_SCRIPT_ID, "battlefield1")
		super(CtrlBattlefield1, self).created(npc)
		return

	def place_encounters_initial(self):
		for pc in toee.game.party:
			pc.condition_add_with_args("Bonus_AC", 20)

		self.pc_position()
		self.place_encounter_e01()
		return

	def delayed_mode(self):
		return 1

	# Sleep interface
	def can_sleep(self):
		return toee.SLEEP_IMPOSSIBLE

	def chess(self, dx5, dy5):
		loc = tpdp.LocAndOffsets(536, 444, 6, -1)
		if (dx5 != 0):
			loc = loc.get_offset_loc(math.radians(45), dx5*5) # top right
		if (dy5 != 0):
			loc = loc.get_offset_loc(math.radians(45+90), dy5*5) # bottom right
		return loc

	def pc_move(self, pc, dx5, dy5, rot):
		loc = self.chess(dx5, dy5)
		#pc.anim_goal_push_walk_to_tile(loc.loc_xy.x, loc.loc_xy.y, loc.off_x, fl_new.off_y)
		pc.move(loc.get_location(), loc.off_x, loc.off_y)
		pc.rotation = rot
		return loc

	def pc_position(self):
		party = toee.game.party

		self.pc_move(party[0], 6, 3, const_toee.ROT02)
		self.pc_move(party[1], 1, 2, const_toee.ROT02)
		self.pc_move(party[2], 1, 3, const_toee.ROT02)
		self.pc_move(party[3], 1, 4, const_toee.ROT02)

		if (0):
			if (len(party) > 0):
				pc = party[0]
				assert isinstance(pc, toee.PyObjHandle)
				#pc.move(utils_obj.sec2loc(526, 453), -13, -15)
				pc.move(utils_obj.sec2loc(536, 444), 0, 0)
				pc.rotation = const_toee.ROT02

			if (len(party) > 1):
				pc = party[1]
				game.party[1].move(utils_obj.sec2loc(528, 453), -8, -15)
				pc.rotation = const_toee.ROT02

			if (len(party) > 2):
				pc = party[2]
				game.party[2].move(utils_obj.sec2loc(530, 453), -6, -15)
				pc.rotation = const_toee.ROT02

			if (len(party) > 3):
				pc = party[3]
				game.party[3].move(utils_obj.sec2loc(532, 453), -2, -15)
				pc.rotation = const_toee.ROT02
		return

	def pc_step(self, degr, dist_ft):
		pc = toee.game.leader

		# direction 0 is up

		fl = pc.location_full
		assert isinstance(fl, tpdp.LocAndOffsets)
		fl_new = fl.get_offset_loc(math.radians(degr), dist_ft)
		#pc.move(fl_new.loc_xy.x, fl_new.loc_xy.y, fl_new.off_x, fl_new.off_y)
		pc.anim_goal_push_walk_to_tile(fl_new.loc_xy.x, fl_new.loc_xy.y, fl_new.off_x, fl_new.off_y)
		return

	def place_encounter_e01(self):
		def add(num, loc):
			#loc = self.chess(6, 3)
			npc, ctrl = self.create_npc_at(loc.get_location(), py06621_battlefield1_monsters.CtrlOrc, const_toee.rotation_0700_oclock, "e01", "orc_0{}".format(num), factions_zmod.FACTION_ENEMY, 0, 0)
			ctrl.vars['num'] = num
			npc.move(loc.get_location(), loc.off_x, loc.off_y)
			utils_npc.npc_goto_loc_fullo(npc, loc)
			utils_npc.npc_description_set_new(npc, 'Orc {}'.format(num))
			npc.condition_add("Debug_Location")
			npc.condition_add("Debug_Rotation")
			npc.condition_add_with_args("Bonus_AC", 20)
			npc.condition_add_with_args('Monster DR Magic', 20)
			return

		add(1, self.chess(9, 2))
		#add(2, self.chess(9, 3))
		#add(3, self.chess(9, 4))

		toee.game.party[1].object_flag_set(toee.OF_INVULNERABLE)
		toee.game.party[2].object_flag_set(toee.OF_INVULNERABLE)
		toee.game.party[3].object_flag_set(toee.OF_INVULNERABLE)
		return

	def pc_goto_square(self, pc_num, abs_side, dist_ft = 5):
		fl = toee.game.party[0].location_full
		assert isinstance(fl, tpdp.LocAndOffsets)
		degr = 135 + 45 * (abs_side - 1)
		if (abs_side % 2 == 0): dist_ft = math.sqrt(dist_ft**2 + dist_ft**2)
		print('dist_ft: {}'.format(dist_ft))
		fl_new = fl.get_offset_loc(math.radians(degr), dist_ft)
		pc = toee.game.party[pc_num]
		pc.anim_goal_push_walk_to_tile(fl_new.loc_xy.x, fl_new.loc_xy.y, fl_new.off_x, fl_new.off_y)
		print(fl_new)
		return

	def pc_goto_square2(self, pc_num, abs_side, dist_ft = 5, run = 0):
		fl = toee.game.party[0].location_full
		assert isinstance(fl, tpdp.LocAndOffsets)
		degr = 45 * abs_side
		if (abs_side % 2 == 0): dist_ft = math.sqrt(dist_ft**2 + dist_ft**2)
		print('dist_ft: {}'.format(dist_ft))
		fl_new = fl.get_offset_loc(math.radians(degr), dist_ft)
		pc = toee.game.party[pc_num]
		if (not run):
			pc.anim_goal_push_walk_to_tile(fl_new.loc_xy.x, fl_new.loc_xy.y, fl_new.off_x, fl_new.off_y)
		else:
			pc.anim_goal_push_run_to_tile(fl_new.loc_xy.x, fl_new.loc_xy.y, fl_new.off_x, fl_new.off_y)
		print(fl_new)
		return

	def pc_goto_square_from_dir_get(self, pc_num, dist_ft = 5):
		fl1 = toee.game.party[0].location_full
		assert isinstance(fl1, tpdp.LocAndOffsets)
		pc = toee.game.party[pc_num]
		fl2 = pc.location_full
		assert isinstance(fl2, tpdp.LocAndOffsets)

		rot = utils_path.rot_from_locs(fl1, fl2)
		rot = utils_path.angle_align_with(rot, 45)
		aloc = fl1.get_offset_loc(rot, utils_path.radius_align_with_side(5, rot, 45))
		return aloc

	def pc_goto_square_from_dir(self, pc_num, dist_ft = 5, go = 1):
		aloc = self.pc_goto_square_from_dir_get(pc_num, dist_ft)
		pc = toee.game.party[pc_num]
		pq = tpai.PathQuery(pc)
		pq.to_loc = aloc
		pqr = pq.find_path()
		print('pqr.is_complete(): {}'.format(pqr.is_complete()))

		if (go):
			utils_npc.npc_anim_goal_push_walk_to_tile(pc, aloc)
		#pc.anim_goal_push_walk_to_tile(aloc.loc_xy.x, aloc.loc_xy.y, aloc.off_x, aloc.off_y)
		print(aloc)
		return pq, pqr
