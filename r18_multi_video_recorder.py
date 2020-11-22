import obspython as obs
import time
from datetime import datetime  
from datetime import timedelta 

Debug_Mode = False
INTERVAL_LIST = []
RECORDING = False
CUR = 0

def script_defaults(settings):
	global Debug_Mode
	if Debug_Mode: print("Calling defaults")
	

def script_description():
	global Debug_Mode
	if Debug_Mode: print("Calling description")

	return "<b>OBS Recording Manager</b>" + \
		"<hr>" + \
		"Split Recording video into user define timed clips." + \
		"<br/>" + \
		"Set Start and Stop times for both recording / streaming." + \
		"<br/>" + \
		"Simple Debug Mode to watch how scripts work in OBS." + \
		"<br/><br/>" + \
		"Made by Jeff Mathewson, © 2018" + \
		"<hr>"

def script_load(settings):
	global Debug_Mode
	if Debug_Mode: print("Calling Load")

	obs.obs_data_set_bool(settings, "enabled", False)

def script_properties():
	global Debug_Mode
	if Debug_Mode: print("Calling properties")	

	props = obs.obs_properties_create()
	obs.obs_properties_add_bool(props, "enabled", "Enabled")
	obs.obs_properties_add_path(props, "interval_path", "Interval Path Txt")

	return props

def script_save(settings):
	global Debug_Mode
	if Debug_Mode: print("Calling Save")

	script_update(settings)

def script_unload():
	global Debug_Mode
	if Debug_Mode: print("Calling unload")

def script_update(settings):
	global INTERVAL_LIST

	if obs.obs_data_get_bool(settings, "enabled"):
		obs.obs_hotkey_register_frontend("Space", "enable_space_to_start_script", space_callback)
	
	elif not obs.obs_data_get_bool(settings, "enabled"):
		obs.obs_hotkey_unregister(space_callback)

	path = obs.obs_data_get_string("interval_path")

	if path != "" and path.endswith(".txt"):
		with open(path, "r") as f:
			line = f.readline()
			while line != "":
				raw = line.split(":")
				if (len(raw) == 3):
					hour = int(raw[0])
					minute = int(raw[1])
					second = int(raw[2])
					milisec = (hour *3600 + minute * 60 + second) * 1000
					INTERVAL_LIST.append(milisec)
				line = f.readline()

def space_callback(pressed):
	if (pressed):
		start_recording()

def stop_recording():
	if obs.obs_frontend_recording_active():
		obs.obs_frontend_recording_stop()
		obs.timer_remove(stop_recording)
	start_recording()

def start_recording():
	global CUR, INTERVAL_LIST
	if CUR < len(INTERVAL_LIST):
		obs.obs_frontend_recording_start()
		obs.timer_add(stop_recording, INTERVAL_LIST[CUR])
		CUR += 1

