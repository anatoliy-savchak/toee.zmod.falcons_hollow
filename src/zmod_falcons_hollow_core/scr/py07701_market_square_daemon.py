import toee, debug, utils_toee, utils_storage, utils_obj, utils_item, const_toee, ctrl_daemon, ctrl_daemon2
import ctrl_behaviour, py06122_cormyr_prompter, factions_zmod, utils_npc
import monster_info, module_quests, module_consts, const_proto_sceneries, utils_skirmish

DAEMON_SCRIPT_ID = 7701
DAEMON_GID = "G_8E5D3B06_98EC_4913_85D2_64DA772E5791"
DEBUG = 0
DEBUG_NAMES = 1

def san_new_map(attachee, triggerer):
	return ctrl_daemon2.do_san_new_map(attachee, triggerer, module_consts.MAP_ID_ZMOD_SK_MARKET_SQUARE, CtrlMakretSquare)

def san_first_heartbeat(attachee, triggerer):
	return ctrl_daemon2.do_san_first_heartbeat(attachee, triggerer, module_consts.MAP_ID_ZMOD_SK_MARKET_SQUARE, CtrlMakretSquare)

def san_heartbeat(attachee, triggerer):
	return ctrl_daemon2.do_san_heartbeat(attachee, triggerer, module_consts.MAP_ID_ZMOD_SK_MARKET_SQUARE, cs())

def san_dying(attachee, triggerer):
	return ctrl_daemon2.do_san_dying(attachee, triggerer, module_consts.MAP_ID_ZMOD_SK_MARKET_SQUARE, cs())

def san_use(attachee, triggerer):
	return ctrl_daemon2.do_san_use(attachee, triggerer, module_consts.MAP_ID_ZMOD_SK_MARKET_SQUARE, cs())

def san_bust(attachee, triggerer):
	return ctrl_daemon2.do_san_bust(attachee, triggerer, module_consts.MAP_ID_ZMOD_SK_MARKET_SQUARE, cs())

def cs():
	o = utils_storage.obj_storage_by_id(DAEMON_GID)
	if (not o): 
		return None
	result = o.data.get(CtrlMakretSquare.get_name())
	assert isinstance(result, CtrlMakretSquare)
	return result

class CtrlMakretSquare(ctrl_daemon2.CtrlDaemon2):
	def created(self, npc):
		self.init_daemon2_fields(module_consts.MAP_ID_ZMOD_SK_MARKET_SQUARE, DAEMON_SCRIPT_ID, "sk_market_square")
		super(CtrlMakretSquare, self).created(npc)
		return

	def place_encounters_initial(self):
		self.place_monsters()
		return

	# Sleep interface
	def can_sleep(self):
		return toee.SLEEP_IMPOSSIBLE

	def do_san_use(self, attachee, triggerer):
		assert isinstance(attachee, toee.PyObjHandle)
		print("san_use id: {}, nameid: {}".format(attachee.id, attachee.name))
		return toee.RUN_DEFAULT

	def place_monsters(self):
		critter_classes = utils_skirmish.generate_enemies1(100, toee.ALIGNMENT_LAWFUL_GOOD)
		print(critter_classes)

		i = -1
		for c in critter_classes:
			i += 1
			self.create_npc_at(utils_obj.sec2loc(473, 472), c, const_toee.rotation_0600_oclock, "main", str(i), factions_zmod.FACTION_ENEMY, 0, 0, 1)

		return