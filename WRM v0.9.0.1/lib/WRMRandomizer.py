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
import math
import random
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

#	Take worlddata state
#	Filter with toggles from settings
#	Apply weights
#	Randomize

#	227 regular missions, ~250 with specials
#	Manager
#		-data (WorldData)
#			-regularMissions (WorldData.regularMissions)
#
#	["togSpecialIgnoreType","togSpecialIgnoreZone",
#"togAlerts","alertWeight","togArchwing","archwingWeight",
#"togBosses","bossWeight","togNightmare","nightmareWeight",
#"togRelics","relicWeight","togCetus","cetusWeight",
#"togInvasions","invasionWeight","togKuvaFarm","kuvafarmWeight",
#"togSyndicate","togSyndicateWeight",
#"togRegular","togMercury","togVenus","togEarth","togMars","togPhobos",
#"togCeres","togJupiter","togEuropa","togSaturn","togUranus","togNeptune",
#"togPluto","togEris","togSedna","togVoid1","togVoid2","togVoid3",
#"togVoid4","togDerelict","togLua","togKuvaFortress","togCapture",
#"togDefection","togDefense","togExcavation","togExterminate","togHijack",
#"togInfestedsalvage","togInterception","togMobiledefense","togSpy",
#"togSurvival","togArena","togSabotage","togDeceptionS","togHiveS",
#"togOrokinS","togSealabS"]
#
#	If specialType
#		loop missions
#			runFilters
#
#
#

class Manager:
	
	def __init__(self, worldData, settings, parent):
		self.parent = parent
		
		self.void1 = ['Teshub','Hepit','Taranis']
		self.void2 = ['Tiwaz','Stribog','Ani']
		self.void3 = ['Ukko','Oxomoco','Belenus']
		self.void4 = ['Aten','Marduk','Mithra','Mot']
		self.relicTypes = {'Lith': settings.togLith, 'Meso': settings.togMeso,
		'Neo': settings.togNeo, 'Axi': settings.togAxi}
		
		self.LoadManager(worldData, settings)
		return
	
	def UpdateManager(self, worldData, settings):
		self.LoadManager(worldData, settings)
		return
	
	def LoadManager(self, worldData, settings):
			
		self.settings = settings
		self.world = worldData
		self.selectionPool = []
		self.BuildZoneSettings()
		self.BuildTypeSettings()
		self.RunFilters()
		return

	def SelectMission(self):
		selecting = True
		self.parent.Log('Default: ', '230 - 240')
		self.parent.Log('M count: ', str(len(self.selectionPool)))
		while selecting:
			selectNumber = random.randrange(1, len(self.selectionPool))
			selectedMission = self.selectionPool[selectNumber]
			if selectedMission.startswith('Invasion'):
				twoD = random.randrange(1,2)
				if twoD == 2:
					selecting = False
			else:
				selecting = False
		
		return selectedMission
		
	def RunFilters(self):
		if self.settings.togRegular == True:
			self.ApplyFilters(self.world.GetMissionsRegular(), False)
		if self.settings.togAlerts == True:
			self.ApplyFilters(self.world.GetMissionsAlerts(), 'alert')
		if self.settings.togRelics == True:
			self.ApplyFilters(self.world.GetMissionsFissures(), 'fissure')
		if self.settings.togInvasions == True:
			self.ApplyFilters(self.world.GetMissionsInvasions(), 'invasion')
		if self.settings.togCetus == True:
			self.ApplyFilters(self.world.GetMissionsCetus(), 'bounty')
		return
		
	def AddRegular(self, mission):
		
		missionString = mission.getType() + ' on ' + mission.getName() + ', ' + mission.getZone()
		
		cS = 0
		cW = 0
		asWeight = 1
		arWeight = 1
		if mission.getType() == 'Assassination':
			asWeight = int(math.floor(self.settings.bossWeight))
			if asWeight > 1:
				for i in range(1, asWeight):
					cW += 1
					self.selectionPool.append(missionString)
		elif mission.getGear() == 'Archwing':
			missionString = 'Archwing ' + missionString
			arWeight = int(math.floor(self.settings.archwingWeight))
			if arWeight > 1:
				for i in range(1, arWeight):
					cS += 1
					self.selectionPool.append(missionString)
		else:
			self.selectionPool.append(missionString)
		
		#self.parent.Log('Counts CS: ', str(cS))
		#self.parent.Log('Counts CW: ', str(cW))
		#self.parent.Log('Added regular: ', missionString)
		return
		
	def AddAlert(self, mission):
		missionString = mission.getType() + ' on ' + mission.getName() + ', ' + mission.getZone()
		if mission.getGear() == 'Archwing':
			missionString = 'Archwing ' + missionString
		missionString = 'Alert ' + missionString
		
		alWeight = int(math.floor(self.settings.alertWeight))
		if alWeight > 1:
			for i in range(1, alWeight):
				self.selectionPool.append(missionString)
		else:
			self.selectionPool.append(missionString)
		
		#self.parent.Log('Added alert: ', missionString)
		return
		
	def AddFissure(self, mission):
		missionString = mission.getType() + ' on ' + mission.getName() + ', ' + mission.getZone()
		
		tW = 0
		tier = mission.getRelicTier()
		missionString = tier + ' Fissure ' + missionString
		
		reWeight = int(math.floor(self.settings.relicWeight))
		if reWeight > 1:
			for i in range(1, reWeight):
				tW += 1
				self.selectionPool.append(missionString)
		else:
			self.selectionPool.append(missionString)
		
		#self.parent.Log('Added fissure: ', missionString)
		self.parent.Log('tW ', str(tW))
		return
		
	# When rolling selection, add a 1d2 roll on invasions as mitigation for running thrice	
	
	def AddInvasion(self, mission):
		missionString = 'Invasion on ' + mission.getName() + ', ' + mission.getZone()
		
		inWeight = int(math.floor(self.settings.invasionWeight))
		if inWeight > 1:
			for i in range(1, inWeight):
				self.selectionPool.append(missionString)
		else:
			self.selectionPool.append(missionString)
		
		#self.parent.Log('Added invasion: ', missionString)
		return
		
	def AddBounty(self, mission):
		#jsonMis = json.dumps(mission.getJobType(), encoding='utf-8', ensure_ascii=False)
		#self.parent.Log('cetusstruct', jsonMis)
		missionString = 'Bounty from Cetus: ' + mission.getJobType()
		
		csWeight = int(math.floor(self.settings.cetusWeight))
		if csWeight > 1:
			for i in range(1, csWeight):
				self.selectionPool.append(missionString)
		else:
			self.selectionPool.append(missionString)
		
		#self.parent.Log('Added bounty: ', missionString)
		return
	
	
	def ApplyFilters(self, missionList, spType):
		#FilterSpecial, apply weight if true
		#	filter relic level
		#Filter Archwing
		#Check specialIgnores
		#Filter type
		#	if Sabotage: Filter subtypes
		#Filter zone
		#Filter boss
			
		# Load missions into
		try:
			iterData = iter(missionList)
			isIter = True
		except TypeError, te:
			isIter = False
			self.parent.Log('WRMR failed iter', '<nil>')
		if isIter:
			for missionInfo in iterData:
				#printme = json.dumps(missionList[missionInfo].toDict(), ensure_ascii=False, encoding="utf-8")
				#self.parent.Log('checkMission', printme)
				if missionList[missionInfo].isBasic() == True:
					if missionList[missionInfo].getZone() != 'hori':
						if self.FilterZone(missionList[missionInfo]) == True:
							if self.FilterType(missionList[missionInfo]) == True:
								self.AddRegular(missionList[missionInfo])
				elif spType == 'alert':
					if self.FilterZone(missionList[missionInfo]) == True:
						if self.FilterType(missionList[missionInfo]) == True:
							self.AddAlert(missionList[missionInfo])
				elif spType == 'fissure':
					if self.FilterZone(missionList[missionInfo]) == True:
						if self.FilterType(missionList[missionInfo]) == True:
							if self.FilterRelics(missionList[missionInfo]) == True:
								self.AddFissure(missionList[missionInfo])
				elif spType == 'invasion':
					if self.FilterZone(missionList[missionInfo]) == True:
						self.AddInvasion(missionList[missionInfo])
				elif spType == 'bounty':
					if self.FilterZone(missionList[missionInfo]) == True:
						self.AddBounty(missionList[missionInfo])
		return
	
	def FilterZone(self, mission):
		if not mission.isBasic() and self.settings.togSpecialIgnoreZone:
			return True
		zone = mission.getZone()
		if zone == 'Void':
			zone = self.EstablishVoid(mission.getName())
		toggles = self.GetZones()
		
		if zone == '':
			return True
		else:
			return toggles[zone]
		
	def FilterType(self, mission):
		if not mission.isBasic() and self.settings.togSpecialIgnoreType:
			return True
		if mission.getGear() == 'Archwing' and not self.settings.togArchwing:
			return False
		type = mission.getType()
		if type == 'Free Roam':
			return True
		
		toggles = self.GetTypes()
	
		#self.parent.Log('Type Control: ', str(toggles[type]))
		return toggles[type]
		
	def FilterRelics(self, mission):
		tier = mission.getRelicTier()
		rType = self.relicTypes
		return rType[tier]
		
	def EstablishVoid(self, void):
		if void in self.void1:
			return 'Void1'
		if void in self.void2:
			return 'Void2'
		if void in self.void3:
			return 'Void3'
		if void in self.void4:
			return 'Void4'

#			self.togMercury = True
#			self.togVenus = True
#			self.togEarth = True
#			self.togMars = True
#			self.togPhobos = True
#			self.togCeres = True
#			self.togJupiter = True
#			self.togEuropa = True
#			self.togSaturn = True
#			self.togUranus = True
#			self.togNeptune = True
#			self.togPluto = True
#			self.togEris = True
#			self.togSedna = True
#			self.togVoid1 = True
#			self.togVoid2 = True
#			self.togVoid3 = True
#			self.togVoid4 = True
#			self.togDerelict = True
#			self.togLua = True
#			self.togKuvaFortress = True	
	
	def BuildZoneSettings(self):
		self.zoneToggle = {}
		self.zoneToggle['Mercury'] = self.settings.togMercury
		self.zoneToggle['Venus'] = self.settings.togVenus
		self.zoneToggle['Earth'] = self.settings.togEarth
		self.zoneToggle['Mars'] = self.settings.togMars
		self.zoneToggle['Phobos'] = self.settings.togPhobos
		self.zoneToggle['Ceres'] = self.settings.togCeres
		self.zoneToggle['Jupiter'] = self.settings.togJupiter
		self.zoneToggle['Europa'] = self.settings.togEuropa
		self.zoneToggle['Saturn'] = self.settings.togSaturn
		self.zoneToggle['Uranus'] = self.settings.togUranus
		self.zoneToggle['Neptune'] = self.settings.togNeptune
		self.zoneToggle['Pluto'] = self.settings.togPluto
		self.zoneToggle['Eris'] = self.settings.togEris
		self.zoneToggle['Sedna'] = self.settings.togSedna
		self.zoneToggle['Void1'] = self.settings.togVoid1
		self.zoneToggle['Void2'] = self.settings.togVoid2
		self.zoneToggle['Void3'] = self.settings.togVoid3
		self.zoneToggle['Void4'] = self.settings.togVoid4
		self.zoneToggle['Derelict'] = self.settings.togDerelict
		self.zoneToggle['Lua'] = self.settings.togLua
		self.zoneToggle['Kuva Fortress'] = self.settings.togKuvaFortress
		return
		
	def GetZones(self):
		return self.zoneToggle
	
	def BuildTypeSettings(self):
		self.typeToggle = {}
		self.typeToggle['Capture'] = self.settings.togCapture
		self.typeToggle['Defection'] = self.settings.togDefection
		self.typeToggle['Defense'] = self.settings.togDefense
		self.typeToggle['Excavation'] = self.settings.togExcavation
		self.typeToggle['Exterminate'] = self.settings.togExterminate
		self.typeToggle['Assault'] = self.settings.togExterminate
		self.typeToggle['Hijack'] = self.settings.togHijack
		self.typeToggle['Infested Salvage'] = self.settings.togInfestedsalvage
		self.typeToggle['Interception'] = self.settings.togInterception
		self.typeToggle['Mobile Defense'] = self.settings.togMobileDefense
		self.typeToggle['Rescue'] = self.settings.togRescue
		self.typeToggle['Spy'] = self.settings.togSpy
		self.typeToggle['Survival'] = self.settings.togSurvival
		self.typeToggle['Arena'] = self.settings.togArena
		self.typeToggle['Sabotage'] = self.settings.togSabotage
		if self.settings.togSabotage:
			self.typeToggle['Deception'] = self.settings.togDeceptionS
			self.typeToggle['Hive'] = self.settings.togHiveS
			self.typeToggle['Orokin Sabotage'] = self.settings.togOrokinS
			self.typeToggle['Sealab'] = self.settings.togSealabS
		else:
			self.typeToggle['Deception'] = False
			self.typeToggle['Hive'] = False
			self.typeToggle['Orokin Sabotage'] = False
			self.typeToggle['Sealab'] = False
		self.typeToggle['Assassination'] = self.settings.togBosses
		self.typeToggle['Pursuit'] = self.settings.togArchwing
		self.typeToggle['Rush'] = self.settings.togArchwing
		
	def GetTypes(self):
		return self.typeToggle