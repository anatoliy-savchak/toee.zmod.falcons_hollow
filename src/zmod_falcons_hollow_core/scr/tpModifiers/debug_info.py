import toee, templeplus.pymod, sys, tpdp, math, traceback, debug

###################################################
def Debug_Location_GetConditionName():
	return "Debug_Location"

print("Registering " + Debug_Location_GetConditionName())
###################################################

def Debug_Location_OnGetTooltip(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjTooltip)

	loc = attachee.location_full
	evt_obj.append(str(loc))
	return 0

oDebug_Location = templeplus.pymod.PythonModifier(Debug_Location_GetConditionName(), 3) # reserved
oDebug_Location.AddHook(toee.ET_OnGetTooltip, toee.EK_NONE, Debug_Location_OnGetTooltip, ())

###################################################
def Debug_Rotation_GetConditionName():
	return "Debug_Rotation"

print("Registering " + Debug_Rotation_GetConditionName())
###################################################

def Debug_Rotation_OnGetTooltip(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjTooltip)

	rot = attachee.rotation
	rot_degr = math.degrees(rot)
	evt_obj.append("Rot: {:.1f} ({:.3f})".format(rot_degr, rot))
	return 0

oDebug_Rotation = templeplus.pymod.PythonModifier(Debug_Rotation_GetConditionName(), 3) # reserved
oDebug_Rotation.AddHook(toee.ET_OnGetTooltip, toee.EK_NONE, Debug_Rotation_OnGetTooltip, ())
