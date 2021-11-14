import toee, utils_npc, utils_npc_spells, utils_tactics, tpdp

# returns error code !!!!!!

EDOT_OK = 0
EDOT_NO_SPELLS_LEFT = 1
EDOT_TARGET_TOO_FAR = 2
EDOT_CANNOT_BE_AFFECTED = 3

class SpellTactic(object):
	def __init__(self, npc, spells, tacs, target = toee.OBJ_HANDLE_NULL, options = None):
		assert isinstance(npc, toee.PyObjHandle)
		assert isinstance(spells, utils_npc_spells.NPCSpells)
		assert isinstance(tacs, utils_tactics.TacticsHelper)
		assert isinstance(target, toee.PyObjHandle)
		self.npc = npc
		self.spells = spells
		self.tacs = tacs
		self.target = target
		self.options = options
		return

	@staticmethod
	def _get_spell_num():
		raise Exception("Not implemented!")
		return 0

	def _is_personal(self):
		se = tpdp.SpellEntry(self._get_spell_num())
		if ("get_spell_range_exact" in dir(se)):
			print("{} ({}) se.spellRange: {}".format(type(self).__name__, toee.game.get_spell_mesline(se.spell_enum), se.spellRange))
			if (se.spellRange == tpdp.SpellRangeType.SRT_Personal):
				return 1
		return 0

	def _check_distance(self):
		if (self._is_personal()): return EDOT_OK
		se = tpdp.SpellEntry(self._get_spell_num())
		if ("get_spell_range_exact" in dir(se)):
			#if (se.spellRange == tpdp.SpellRangeType.SRT_Personal): return EDOT_OK
			spell_rec = self.spells.get_spell(self._get_spell_num())
			caster_level = spell_rec.spell_level
			range = se.get_spell_range_exact(caster_level, self.npc)
			dist = self.npc.distance_to(self.target)
			if (dist > range):
				print("{} ({}) EDOT_TARGET_TOO_FAR (range: {}, dist: {}) by {} on {}".format(type(self).__name__, toee.game.get_spell_mesline(self._get_spell_num()), range, dist, self.npc, self.target))
				return EDOT_TARGET_TOO_FAR
		return EDOT_OK

	def _subject(self):
		return self.npc if (self._is_personal()) else self.target

	def _except_q(self):
		return 0

	def _check_already(self):
		q = self._except_q()
		if (not q): return EDOT_OK

		obj = self._subject()
		if (not obj): return EDOT_OK

		if (obj.d20_query(q)):
			return EDOT_CANNOT_BE_AFFECTED

		return EDOT_OK

	def _add_spell_exec(self):
		self.tacs.add_cast_single_code(self.spells.prep_spell(self.npc, self._get_spell_num()))
		return EDOT_OK

	def execute(self):
		print("{} ({}) execute by {} on {}".format(type(self).__name__, toee.game.get_spell_mesline(self._get_spell_num()), self.npc, self.target))
		if (self.spells.get_spell_count(self._get_spell_num()) == 0): 
			print("{} EDOT_NO_SPELLS_LEFT for {} by {}".format(type(self).__name__, toee.game.get_spell_mesline(self._get_spell_num()), self.npc))
			return EDOT_NO_SPELLS_LEFT

		result = self._check_already()
		if (result): 
			return result

		is_personal = self._is_personal()
		if (not is_personal):
			result = self._check_distance()
			if (result):
				return result

		if (self.options and self.options.get("skip_five_foot_step")):
			pass
		else:
			self.tacs.add_five_foot_step()

		if (self.options and self.options.get("add_halt_before")):
			self.tacs.add_halt()

		if (is_personal):
			self.tacs.add_target_self()
		else:
			if (self.target):
				self.tacs.add_target_obj(self.target.id)
			else:
				self.tacs.add_target_closest()
		
		result = self._add_spell_exec()
		if (result): 
			return result

		return EDOT_OK

class STDivineFavor(SpellTactic):
	@staticmethod
	def _get_spell_num(): return toee.spell_divine_favor

class STHoldPerson(SpellTactic):
	@staticmethod
	def _get_spell_num(): return toee.spell_hold_person

	def _except_q(self): return toee.Q_Critter_Is_Held

class STCauseFear(SpellTactic):
	@staticmethod
	def _get_spell_num(): return toee.spell_cause_fear

	def _except_q(self): return toee.Q_Critter_Is_Afraid

	def _is_personal(self): return 0 # bug currently 2021-10-04

class STShieldOfFaith(SpellTactic):
	@staticmethod
	def _get_spell_num(): return toee.spell_shield_of_faith
