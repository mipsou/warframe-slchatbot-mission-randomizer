
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
import codecs
import datetime
import json
import logging
import os
import random
import sqlite3
import sys
import time
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))
import WRMWorldDataParser
import WRMjsonLoader

#	recreate the world-state-parser from here
#	make the ParseArray( ParserClass, dataArray, "deps" )
#	recreate 



class WorldData:
	def __init__(self, settings, worldData, parent, utime):
		self.pParent = parent
		self.jsonLoader = WRMjsonLoader.JsonLoader()
		
		self.buildMissions(settings, worldData, parent, utime)
		return
	
			
	def ShouldUpdate(self):
		now = datetime.datetime.today()
		seconds = (now - self.timeUpdated).total_seconds()
		if seconds > 200:
			return True
		else:
			return False
	
	
	def buildMissions(self, settings, data, parent, utime):
	
		self.timeUpdated = utime
		#WRMWorldDataParser.printMissionList(parent)
		if settings.togRegular == True:
			self.regularMissions = WRMWorldDataParser.CompileMissionsList(settings, parent, self.jsonLoader)
		
		#
		if settings.togAlerts == True:
			self.alerts = WRMWorldDataParser.ExtractAlertMissions(data['Alerts'],settings, parent, self.jsonLoader)
		
		#
		if settings.togRelics == True:
			self.relics = WRMWorldDataParser.ExtractFissureMissions(data['ActiveMissions'],settings, parent, self.jsonLoader)
		
		#
		if settings.togInvasions == True:
			self.invasions = WRMWorldDataParser.ExtractInvasionMissions(data['Invasions'],settings, parent, self.jsonLoader)
		
		#
		if settings.togCetus == True:
			self.cetus = WRMWorldDataParser.ExtractCetusMissions(data['SyndicateMissions'],settings, parent, self.jsonLoader)

		return
	
	def GetMissionsAlerts(self):
		#.Alerts
		if hasattr(self, 'alerts'):
			return self.alerts
		else:
			return []
		
	def GetMissionsFissures(self):
		#.ActiveMissions
		if hasattr(self, 'relics'):
			return self.relics
		else:
			return []
	
	def GetMissionsInvasions(self):
		#.Invasions
		if hasattr(self, 'invasions'):
			return self.invasions
		else:
			return []
		
	def GetMissionsCetus(self):
		#.SyndicateMissions.Tag == "CetusSyndicate" [index]Jobs
		if hasattr(self, 'cetus'):
			return self.cetus
		else:
			return []
	
	#def GetSyndicateMissions():
		#.SyndicateMissions
	#	return

	def GetMissionsRegular(self):
		#.solNodes
		if hasattr(self, 'regularMissions'):
			return self.regularMissions
		else:
			return []
	
	def regularJSON(self):
		jsonDict = {}
		missions = self.GetMissionsRegular()
		for mission in missions:
			jsonDict[mission] = missions[mission].toDict()
		return json.dumps(jsonDict, ensure_ascii=False, encoding="utf-8")
	
	def getRegularDict(self):
		regularDict = {}
		missions = self.GetMissionsRegular()
		for mission in missions:
			
			#printme = json.dumps(missions[mission].toDict(), encoding='utf-8', ensure_ascii=False)
			#self.pParent.Log('missionsTarget', printme)
			
			regularDict[mission] = missions[mission].toDict()
			
		return regularDict
	
	def alertJSON(self):
	
		return
		
	def getAlertDict(self):
		alertDict = {}
		missions = self.GetMissionsAlerts()
		for mission in missions:
			alertDict[mission] = missions[mission].toDict()
			
		return alertDict
		
	def fissureJSON(self):
	
		return
		
	def getFissureDict(self):
		fissureDict = {}
		missions = self.GetMissionsFissures()
		for mission in missions:
			fissureDict[mission] = missions[mission].toDict()
		return fissureDict
		
	def invasionJSON(self):
	
		return
	
	def getInvasionDict(self):
		invasionDict = {}
		missions = self.GetMissionsInvasions()
		for mission in missions:
			invasionDict[mission] = missions[mission].toDict()
		return invasionDict
		
	def cetusJSON(self):
	
		return
		
	def getCetusDict(self):
		cetusDict = {}
		missions = self.GetMissionsCetus()
		for mission in missions:
			cetusDict[mission] = missions[mission].toDict()
		return cetusDict