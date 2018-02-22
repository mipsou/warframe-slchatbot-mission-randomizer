
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

sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))
import WRMWorldDataParser

#	recreate the world-state-parser from here
#	make the ParseArray( ParserClass, dataArray, "deps" )
#	recreate 



class WorldData:
	def __init__(self, settings, worldData, parent):
		self.buildMissions(settings, worldData, parent)
		return
	
	def buildMissions(self, settings, data, parent):
		#WRMWorldDataParser.printMissionList(parent)
		self.regularMissions = WRMWorldDataParser.CompileMissionsList(settings, parent)
		
		#Alert missions on?
		if settings.togAlerts == True:
			self.alerts= WRMWorldDataParser.ExtractAlertMissions(data['Alerts'], settings, parent)
			parent.Log('WRMWD bm', 'Alerts done')
		else:
			self.alerts= []
			
		#Fissures on?
		if settings.togRelics == True:
			self.fissures= WRMWorldDataParser.ExtractFissureMissions(data['ActiveMissions'], settings, parent)
			
			parent.Log('WRMWD bm', 'Fissures done')
		else:
			self.fissures= []
			
		#Invasions on?
		if settings.togInvasions == True:
			self.invasions= WRMWorldDataParser.ExtractInvasionMissions(data['Invasions'], settings, parent)
			
			parent.Log('WRMWD bm', 'Invasions done')
		else:
			self.invasions= []
			
		#Bounties on?
		if settings.togCetus == True:
			self.cetus= WRMWorldDataParser.ExtractCetusMissions(data['SyndicateMissions'], settings, parent)
			
			parent.Log('WRMWD bm', 'Bounties done')
		else:
			self.cetus= []
			
		return
	
	def GetAlertMissions(self):
		#.Alerts
		return self.alerts
		
	def GetFissureMissions(self):
		#.ActiveMissions
		return self.fissures
	
	def GetInvasionMissions(self):
		#.Invasions
		return self.invasions
		
	def GetCetusMissions(self):
		#.SyndicateMissions.Tag == "CetusSyndicate" [index]Jobs
		return self.cetus
	
	#def GetSyndicateMissions():
		#.SyndicateMissions
	#	return

	def RegularMissionsList(self):
		#.solNodes
		return self.regularMissions
	
	def regularJSON(self):
		jsonDict = {}
		for mission in self.regularMissions:
			jsonDict[mission] = self.regularMissions[mission].toDict()
		return json.dumps(jsonDict, ensure_ascii=False, encoding="utf-8")
	
	def getRegularDict(self):
		regularDict = {}
		for mission in self.regularMissions:
			regularDict[mission] = self.regularMissions[mission].toDict()
			
		return regularDict
	
	def alertJSON(self):
	
		return
		
	def getAlertDict(self):
		alertDict = {}
		for mission in self.alerts:
			alertDict[mission] = self.alerts[mission].toDict()
			
		return alertDict
		
	def fissureJSON(self):
	
		return
		
	def getFissureDict(self):
		fissureDict = {}
		for mission in self.fissures:
			fissureDict[mission] = self.fissures[mission].toDict()
		return fissureDict
		
	def invasionJSON(self):
	
		return
	
	def getInvasionDict(self):
		invasionDict = {}
		for mission in self.invasions:
			invasionDict[mission] = self.invasions[mission].toDict()
		return invasionDict
		
	def cetusJSON(self):
	
		return
		
	def getCetusDict(self):
		cetusDict = {}
		for mission in self.cetus:
			cetusDict[mission] = self.cetus[mission].toDict()
		return cetusDict