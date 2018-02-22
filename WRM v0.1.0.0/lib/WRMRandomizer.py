#---------------------------------------
#   Import Libraries
#---------------------------------------

import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
import os
import random
import sqlite3
import sys
import time
import json

sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

#	Take worlddata state
#	Filter with toggles from settings
#	Apply weights
#	Randomize

#	Manager
#		-data (WorldData)
#			-regularMissions (WorldData.regularMissions)
#
class Manager:
	
	def __init__(self, worldData, settings, parent, utime):
		self.activeSettings = settings
		self.parent = parent
		self.timeUpdated = utime
		self.data = worldData
		return
	
	def UpdateSettings(self):
		return
	
	def SelectMission(self):
		selectedMission = ''
		return 
		