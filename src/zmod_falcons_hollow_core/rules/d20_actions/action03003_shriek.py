import toee
import tpactions

def GetActionName():
	return "Lethal Shriek"

def GetActionDefinitionFlags():
	return toee.D20ADF_None | toee.D20ADF_Breaks_Concentration | D20ADF_TriggersCombat
	
def GetTargetingClassification():
	return toee.D20TC_Target0

def GetActionCostType():
	return toee.D20ACT_Full_Round_Action

def AddToSequence(d20action, action_seq, tb_status):
	action_seq.add_action(d20action)
	return toee.AEC_OK