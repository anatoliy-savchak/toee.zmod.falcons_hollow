import toee, tpdp

def add_from_pattern(historyMesline, handle, handle2):
	assert isinstance(historyMesline, int)
	assert isinstance(handle, toee.PyObjHandle)
	assert isinstance(handle2, toee.PyObjHandle)
	return

def add_damage_roll(attacker, tgt, dmg):
	assert isinstance(attacker, toee.PyObjHandle)
	assert isinstance(tgt, toee.PyObjHandle)
	assert isinstance(dmg, tpdp.DamagePacket)
	history_id = 1
	return history_id

def add_percent_chance_roll(performer, tgt, failChance, combatMesTitle, rollResult, combatMeslineResultText, combatMeslineCheckType):
	assert isinstance(performer, toee.PyObjHandle)
	assert isinstance(tgt, toee.PyObjHandle)
	assert isinstance(failChance, int)
	assert isinstance(combatMesTitle, int)
	assert isinstance(rollResult, int)
	assert isinstance(combatMeslineResultText, int)
	assert isinstance(combatMeslineCheckType, int)
	history_id = 1
	return history_id

