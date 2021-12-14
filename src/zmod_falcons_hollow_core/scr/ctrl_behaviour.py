import toee, debug, utils_storage, utils_npc_spells, const_toee, utils_tactics, const_proto_weapon, utils_item, const_proto_armor, const_proto_scrolls
import utils_target_list, utils_npc, tpdp, tpactions, copy
import logging

def get_ctrl(id):
	assert isinstance(id, str)
	ctrl = None
	storage = utils_storage.obj_storage_by_id(id)
	if (storage):
		print(storage.data)
		for t in storage.data.iteritems():
			if (issubclass(type(t[1]), CtrlBehaviour)):
				ctrl = t[1]
				break
	return ctrl

def san_start_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = CtrlBehaviour.get_from_obj(attachee)
	print("san_start_combat {}, {}".format(attachee, ctrl))
	if (ctrl):
		return ctrl.start_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_enter_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = CtrlBehaviour.get_from_obj(attachee)
	if (ctrl):
		return ctrl.on_enter_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_end_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = CtrlBehaviour.get_from_obj(attachee)
	if (ctrl):
		return ctrl.on_end_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_exit_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = CtrlBehaviour.get_from_obj(attachee)
	if (ctrl):
		return ctrl.exit_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_will_kos(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	#print("will_kos({}, {})".format(attachee, triggerer))
	ctrl = CtrlBehaviour.get_from_obj(attachee)
	if (ctrl):
		return ctrl.will_kos(attachee, triggerer)
	else: print("san_will_kos ctrl not found")
	return toee.RUN_DEFAULT

def san_dialog(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = CtrlBehaviour.get_from_obj(attachee)
	if (ctrl):
		return ctrl.dialog(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = CtrlBehaviour.get_from_obj(attachee)
	if (ctrl):
		return ctrl.heartbeat(attachee, triggerer)

	# RUN_DEFAULT means
	# If not toee.game.combat_is_active() than AiProcess will be called else nothing
	# If toee.game.combat_is_active() and SKIP_DEFAULT then skip turn completely

	return toee.RUN_DEFAULT

def san_wield_off(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = CtrlBehaviour.get_from_obj(attachee)
	if (ctrl and "wield_off" in dir(ctrl)):
		return ctrl.wield_off(attachee, triggerer)
	return toee.RUN_DEFAULT


class CtrlBehaviour(object):
	def __init__(self):
		self.id = None
		self.spells = utils_npc_spells.NPCSpells()
		self.vars = dict()
		#self.items = dict()
		return

	def created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		# assign scripts
		#npc.scripts[const_toee.sn_start_combat] = 6213
		# create inventory
		self.id = npc.id
		self.after_created(npc)
		return

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		return

	@classmethod
	def get_proto_id(cls):
		return 0

	@classmethod
	def get_alias(self):
		return

	@classmethod
	def create_obj_and_class(cls, loc, call_created=1, register=1):
		protoid = cls.get_proto_id()
		if (protoid <= 0):
			debug.breakp("protoId cannot be zero!")
			raise Exception("protoId cannot be zero!")
		npc = toee.game.obj_create(protoid, loc)
		if (not npc):
			debug.breakp("obj created cannot be null!")
			raise Exception("Failed to create obj by proto: {}!".format(protoid))
		print("obj_create({}, {}) = {}".format(protoid, loc, npc))
		ctrl = cls()
		if (register):
			o = utils_storage.obj_storage(npc)
			o.data["ctrl"] = ctrl
			o.alias = cls.get_alias()
			o.origin = npc.origin
			print(o.data)
		if (call_created):
			ctrl.created(npc)
		return npc, ctrl

	@classmethod
	def create_obj(cls, loc):
		npc, ctrl = cls.create_obj_and_class(loc)
		return npc

	@classmethod
	def get_name(cls):
		return type(cls).__name__

	@classmethod
	def ensure(cls, npc):
		data = utils_storage.obj_storage(npc).data
		ctrl = None
		if (cls.get_name() in data):
			ctrl = data["ctrl"]
		else:
			ctrl = cls()
			ctrl.created(npc)
			utils_storage.obj_storage(npc).data["ctrl"] = ctrl
		return ctrl

	@classmethod
	def get_from_obj(cls, npc):
		data = utils_storage.obj_storage(npc).data
		if (["ctrl"] in data):
			ctrl = data["ctrl"]
			assert isinstance(ctrl, CtrlBehaviour)
			return ctrl
		return

	def npc_get(self):
		npc = None
		if (self.id):
			npc = toee.game.get_obj_by_id(self.id)
		if (not npc):
			print("Failed to get NPC ctrl: {}, id: {}".format(type(self).__name__, self.id))
		return npc

	def start_combat(self, attachee, triggerer):
		print("")
		print("{}::{} (round: {})".format(type(self).__name__, "start_combat", toee.game.combat_turn))
		print("------------------------")
		#debugg.breakp("start_combat")
		if (utils_npc.npc_hp_current(attachee) >= 0):
			tac = self.create_tactics(attachee)
			if (not tac):
				tac = self.create_tactics_default(attachee)

			if (tac and tac.count > 0):
				tac.set_strategy(attachee)
		return toee.RUN_DEFAULT

	def exit_combat(self, attachee, triggerer):
		return toee.RUN_DEFAULT

	def on_enter_combat(self, attachee, triggerer):
		result = self.enter_combat(attachee, triggerer)
		return result

	def enter_combat(self, attachee, triggerer):
		return toee.RUN_DEFAULT

	def on_end_combat(self, attachee, triggerer):
		self.end_combat(attachee, triggerer)
		return toee.RUN_DEFAULT

	def end_combat(self, attachee, triggerer):
		return toee.RUN_DEFAULT

	def will_kos(self, attachee, triggerer):
		return toee.RUN_DEFAULT

	def dying(self, attachee, triggerer):
		return toee.RUN_DEFAULT

	def dialog(self, attachee, triggerer):
		return toee.RUN_DEFAULT

	def join(self, npc, follower):
		return toee.RUN_DEFAULT

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		return None

	def create_tactics_default(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		tac = utils_tactics.TacticsHelper(self.get_name())
		tac.add_clear_target()
		tac.add_target_closest()
		tac.add_sniper()
		tac.add_use_potion()
		tac.add_attack()
		tac.add_approach()
		tac.add_attack()
		return tac

	def revealed(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		return

	def revealing(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		return

	def activated(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		return

	def activating(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		return

	def trigger_step(self, npc, step):
		assert isinstance(npc, toee.PyObjHandle)
		assert isinstance(step, int)
		return

	def get_var(self, name, default_value = None):
		if (self.vars and name in self.vars):
			return self.vars[name]
		self.vars[name] = default_value
		return default_value

	def tactic_coup_de_grace(self, npc, foes = None):
		assert isinstance(npc, toee.PyObjHandle)
		if (foes is None):
			foes = utils_target_list.AITargetList(npc, 1, 0, utils_target_list.AITargetMeasure.by_all()).rescan()
		coup_de_grace_targets = foes.get_coup_de_grace_targets()
		if (coup_de_grace_targets): 
			#debug.breakp("coup_de_grace_targets")
			tac = utils_tactics.TacticsHelper(self.get_name())
			tac.add_target_closest()
			tac.add_target_obj(coup_de_grace_targets[0].target.id)
			tac.add_approach_single()
			tac.add_d20_action(toee.D20A_COUP_DE_GRACE, 0)
			tac.add_attack_threatened()
			tac.add_total_defence()
			return tac
		return

	def heartbeat(self, attachee, triggerer):
		assert isinstance(attachee, toee.PyObjHandle)
		assert isinstance(triggerer, toee.PyObjHandle)
		return toee.RUN_DEFAULT

	def cooldown(self, var_name):
		if (var_name is None): return
		var_value = self.get_var(var_name, 0)
		if (var_value > 0):
			var_value -=1
			self.vars[var_name] = var_value
		return var_value

	def cooldown_all(self):
		for key in self.vars.iterkeys():
			assert isinstance(key, str)
			if ("cooldown" in key):
				self.cooldown(key)
		return

	def on_execute_strategy(self, npc, target):
		return


class CtrlBehaviourAI(CtrlBehaviour):
	def __init__(self):
		super(CtrlBehaviourAI, self).__init__()
		self._vars = dict()
		self._vars_tactics = dict()
		return

	def start_combat(self, attachee, triggerer):
		assert isinstance(attachee, toee.PyObjHandle)
		print("")
		print("{}::{} (round: {})".format(type(self).__name__, "start_combat", toee.game.combat_turn))
		print("------------------------")

		self._vars_tactics = dict()

		hp_current = attachee.stat_level_get(toee.stat_hp_current)
		self._vars_tactics["hp_current"] = hp_current
		
		if (hp_current <= -10):
			print("Tactics: Skip - Is Dead for {}".format(attachee))
			return toee.SKIP_DEFAULT

		if (hp_current < 0):
			print("Tactics: Skip - Is Dying for {}".format(attachee))
			return toee.SKIP_DEFAULT

		if (attachee.d20_query(toee.Q_Unconscious)):
			print("Tactics: Skip - Is Unconscious for {}".format(attachee))
			return toee.SKIP_DEFAULT

		if (attachee.d20_query(toee.Q_Helpless)):
			print("Tactics: Skip - Is Helpless for {}".format(attachee))
			return toee.SKIP_DEFAULT

		if (attachee.d20_query(toee.Q_Critter_Is_Stunned)):
			print("Tactics: Skip - Is Stunned for {}".format(attachee))
			return toee.SKIP_DEFAULT

		if (attachee.d20_query(toee.Q_Critter_Is_Held)):
			print("Tactics: Skip - Is Held for {}".format(attachee))
			return toee.SKIP_DEFAULT

		seq = tpactions.get_cur_seq()
		if (seq and seq.tb_status):
			if (not seq.tb_status.hourglass_state):
				print("Tactics: Skip - hourglass_state == no actions for {}".format(attachee))
				#attachee.condition_add("Fighting_Defensively_Monster")
				return toee.SKIP_DEFAULT

		tac = utils_tactics.TacticsHelper(self.get_name())
		self.tactics_recon(attachee)
		while (True):
			if (self.tactics_process_critical(attachee, tac)):
				break
			tac = self.create_tactics(attachee)
			if (tac): break

			tac = self.create_tactics_default(attachee)
			break

		self._vars_tactics = None
		if (tac):
			tac.set_strategy(attachee)

		return toee.RUN_DEFAULT

	def on_end_combat(self, attachee, triggerer):
		self.vars["exec_strategy_counter"] = 0
		self.end_combat(attachee, triggerer)
		return toee.RUN_DEFAULT

	def tactics_process_critical(self, npc, tac):
		assert isinstance(npc, toee.PyObjHandle)
		assert isinstance(tac, utils_tactics.TacticsHelper)

		#foes_adjacent = self._vars_tactics["foes_adjacent"] if "foes_adjacent" in self._vars_tactics else list()

		prefer_offense = self.tactics_prefer_offense(npc)

		# is entangled
		spell_id_breakfree = npc.d20_query(toee.Q_Is_BreakFree_Possible)
		if (spell_id_breakfree):
			if (not prefer_offense):
				tac.add_d20_action(toee.D20A_BREAK_FREE, spell_id_breakfree)
				tac.add_stop()

		hp = npc.stat_level_get(toee.stat_hp_current)
		if (hp == 0):
			if (not prefer_offense):
				item = self.tactics_get_heal_item(npc, True)
				if (item):
					tac.add_five_foot_step()
					tac.add_use_item(item.id)
					tac.add_stop()
					return True

		foes_could_be_approached = self._vars_tactics.get("foes_could_be_approached")
		assert isinstance(foes_could_be_approached, list)

		# coup de grace
		if (foes_could_be_approached):
			foes_can_be_graced = list(o for o in foes_could_be_approached if o.d20_query(toee.Q_Helpless))
			if (foes_can_be_graced):
				tac.add_target_obj(foes_can_be_graced[0].id)
				tac.add_approach()
				tac.add_d20_action(toee.D20A_COUP_DE_GRACE, 0)
				return True

		return False

	def tactics_recon(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		print("tactics_recon {}".format(npc))

		foes_adjacent = list()
		foes_threatening = list()
		foes = list()

		npc_can_melee = utils_npc.npc_can_melee(npc, None)
		npc_radius = utils_npc.npc_get_radius_ft(npc)
		npc_reach = utils_npc.npc_get_reach(npc)

		for obj in toee.game.obj_list_vicinity(npc.location, toee.OLC_CRITTERS):
			if obj == npc: continue
			#print("tactics_recon obj check {}".format(obj))
			if (npc.is_friendly(obj)): 
				#print("\t tactics_recon is friendly {}".format(obj))
				continue

			if (not utils_npc.npc_could_be_attacked(obj, 0)): 
				#print("\t tactics_recon not npc_could_be_attacked {}".format(obj))
				continue

			if (not npc.can_sense(obj)): 
				#print("\t tactics_recon cannot sense {}".format(obj))
				continue

			foes.append(obj)

			if (utils_npc.npc_is_within_reach_ext(npc, obj, npc_radius, npc_reach)):
				#print("\t tactics_recon is npc_is_within_reach_ext, foes_adjacent.append {}".format(obj))
				foes_adjacent.append(obj)
			else:
				pass
				#print("\t tactics_recon not npc_is_within_reach_ext {}".format(obj))

			if (utils_npc.npc_can_melee(obj, npc) and utils_npc.npc_is_within_reach(obj, npc)):
				#print("\t tactics_recon is npc_can_melee, foes_threatening.append {}".format(obj))
				foes_threatening.append(obj)
			else:
				pass
				#print("\t tactics_recon not npc_can_melee {}".format(obj))

		foes = sorted(foes, key = lambda o: npc.distance_to(o))
		foes_can_sense = list(o for o in foes if npc.can_sense(o))
		#foes_could_be_approached = list(o for o in foes_can_sense if npc.can_find_path_to_obj(o))

		foes_could_be_approached = []
		for o in foes_can_sense:
			can_path = npc.can_find_path_to_obj(o)
			if (can_path):
				foes_could_be_approached.append(o)
			print('can_path {} to {} from {}'.format(can_path, o, npc))
			

		print("foes: {}".format(foes))
		print("foes_threatening: {}".format(foes_threatening))
		print("foes_adjacent: {}".format(foes_adjacent))
		print("foes_can_sense: {}".format(foes_can_sense))
		print("foes_could_be_approached: {}".format(foes_could_be_approached))

		self._vars_tactics["npc_radius"] = npc_radius
		self._vars_tactics["npc_reach"] = npc_reach
		self._vars_tactics["npc_can_melee"] = npc_can_melee

		self._vars_tactics["foes_adjacent"] = foes_adjacent
		self._vars_tactics["foes_threatening"] = foes_threatening
		self._vars_tactics["foes_can_sense"] = foes_can_sense
		self._vars_tactics["foes_could_be_approached"] = foes_could_be_approached
		self._vars_tactics["foes"] = foes
		return

	def tactics_prefer_offense(self, npc):
		assert isinstance(npc, toee.PyObjHandle)

		return 0

	def tactics_get_heal_item(self, npc, best = False):
		assert isinstance(npc, toee.PyObjHandle)
		return self.tactics_get_heal_item_default(npc, best)

	def tactics_get_heal_item_default(self, npc, best = False):
		def _get_item(npc, best, item_protos):
			assert isinstance(npc, toee.PyObjHandle)
			if (best): 
				assert isinstance(item_protos, list)
				item_protos = copy.copy(item_protos)
				item_protos.reverse()
			for proto in item_protos:
				item = npc.item_find_by_proto(proto)
				if (item): return item

		item = None
		#item = _get_item(npc, best, const_proto_list_potions.PROTOS_POTIONS_HEALING)
		#if (item): return item

		#if (self.tactics_can_cast_divine_scrolls(npc)):
		#	item = _get_item(npc, best, const_proto_list_scrolls.PROTOS_SCROLLS_HEALING)
		return item

	def tactics_can_cast_divine_scrolls(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		divine_level = npc.highest_divine_caster_level()
		return divine_level

	def tactics_is_hp_critical_for_heal(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		hp = npc.stat_level_get(toee.stat_hp_current)
		return

	def create_tactics_default(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		tac = utils_tactics.TacticsHelper(self.get_name())

		current_primary_ranged = utils_npc.npc_get_weapon(npc, 1)
		target = self.tactics_determine_target(npc, True if (current_primary_ranged) else False)

		if (target):
			# set focus, otherwise targeting might decide to ignore it
			npc.obj_set_obj(toee.obj_f_npc_combat_focus, target)

			tac.add_target_obj(target.id)
			tac.add_sniper()
			tac.add_use_potion()
			tac.add_charge()
			tac.add_approach_single()
			tac.add_attack()
			tac.add_ready_vs_approach()
			tac.add_stop()
		else:
			npc.obj_set_obj(toee.obj_f_npc_combat_focus, toee.OBJ_HANDLE_NULL)
			print("No target, Total Defense")
			npc.float_text_line('Total Defense', toee.tf_yellow)
			tac.add_total_defence()
			tac.add_stop()
		return tac

	def tactics_determine_target(self, npc, for_ranged):
		assert isinstance(npc, toee.PyObjHandle)
		#print("tactics_determine_target {} {}".format(type(self).__name__, npc))

		foes_adjacent = self._vars_tactics.get("foes_adjacent")
		assert isinstance(foes_adjacent, list)
		foes_threatening = self._vars_tactics.get("foes_threatening")
		assert isinstance(foes_threatening, list)
		foes = self.tactics_get_foes()

		foes_can_sense = self._vars_tactics["foes_can_sense"]
		assert isinstance(foes_can_sense, list)
		foes_could_be_approached = self._vars_tactics["foes_could_be_approached"]
		assert isinstance(foes_could_be_approached, list)

		target = toee.OBJ_HANDLE_NULL
		while (not target):
			if (foes_adjacent): 
				target = foes_adjacent[0]
				if (target): break

			if (foes_threatening): 
				target = foes_threatening[0]
				if (target): break

			if (foes_could_be_approached):
				target = foes_could_be_approached[0]
				if (target): break

			if (foes_can_sense):
				target = foes_can_sense[0]
				if (target): break

			break
		print("tactics_determine_target self: {} npc: {} target: {}".format(type(self).__name__, npc, target))
		return target

	def on_enter_combat(self, attachee, triggerer):
		self.alert_comrades(attachee, triggerer)
		result = self.enter_combat(attachee, triggerer)
		return result

	def alert_comrades(self, npc, target):
		# todo: it should be handled in T+
		# add others by leader
		result = 0
		leader = npc.leader_get()
		if (leader):
			#print("add others for leader: {}".format(leader))
			critters = utils_npc.critters_vicinity(npc)
			#print(critters)
			if (critters):
				for o in critters:
					assert isinstance(o, toee.PyObjHandle)
					if (not o.is_active_combatant() and (o == leader or o.leader_get() == leader)):
						o.add_to_initiative()
						o.attack(target)
						result += 1
		return result

	def setup(self, npc):
		# todo
		self.setup_scripts()
		self.setup_appearance()
		self.setup_char()
		self.setup_gear()
		self.setup_loot()
		self.setup_end()
		return

	def generate_hp(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		pts, hp_lines = utils_npc.npc_generate_hp_random_first(npc)
		self.vars["hp_lines"] = hp_lines
		return

	def tactics_get_foes(self):
		foes = self._vars_tactics["foes"]
		assert isinstance(foes, list)
		if (foes is None): foes = []
		return foes