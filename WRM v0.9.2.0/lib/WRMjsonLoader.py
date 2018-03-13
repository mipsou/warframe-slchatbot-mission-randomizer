
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

	
def GetFactionNames():
	factionNamesJSON = os.path.join(os.path.dirname(__file__), "../lib/jsons/factionNames.json")
	if factionNamesJSON and os.path.isfile(factionNamesJSON):
		with codecs.open(factionNamesJSON) as f:
			factionNames = json.load(f)
	sys.path.append(os.path.join(os.path.dirname(__file__), "../lib/classes"))
	return factionNames

def GetBossLocations():
	bossesJSON = os.path.join(os.path.dirname(__file__), "../lib/jsons/assassinationTargets.json")
	if bossesJSON and os.path.isfile(bossesJSON):
		with codecs.open(bossesJSON) as f:
			bosses = json.load(f)
	sys.path.append(os.path.join(os.path.dirname(__file__), "../lib/classes"))
	return bosses
	
def GetMissionType():
	missionTypesJSON = os.path.join(os.path.dirname(__file__), "../lib/jsons/missionTypes.json")
	if missionTypesJSON and os.path.isfile(missionTypesJSON):
		with codecs.open(missionTypesJSON) as f:
			missionTypes = json.load(f)
	sys.path.append(os.path.join(os.path.dirname(__file__), "../lib/classes"))
	return missionTypes

def GetNavMissionNodes():
	navMissionsJSON = os.path.join(os.path.dirname(__file__), "../lib/jsons/navMissions.json")
	if navMissionsJSON and os.path.isfile(navMissionsJSON):
		with codecs.open(navMissionsJSON) as f:
			navMissions = json.load(f)
	sys.path.append(os.path.join(os.path.dirname(__file__), "../lib/classes"))
	return navMissions
	
def GetRelics():
	relicNamesJSON = os.path.join(os.path.dirname(__file__), "../lib/jsons/relicNames.json")
	if relicNamesJSON and os.path.isfile(relicNamesJSON):
		with codecs.open(relicNamesJSON) as f:
			relicNames = json.load(f)
	sys.path.append(os.path.join(os.path.dirname(__file__), "../lib/classes"))
	return relicNames

	
def GetSolNodes():
	solNodesJSON = os.path.join(os.path.dirname(__file__), "../lib/jsons/solNodes.json")
	if solNodesJSON and os.path.isfile(solNodesJSON):
		with codecs.open(solNodesJSON) as f:
			solNodes = json.load(f)
	sys.path.append(os.path.join(os.path.dirname(__file__), "../lib/classes"))
	return solNodes


# TODO only fetch language.json once ?
def GetLanguageFile():
	languageJSON = os.path.join(os.path.dirname(__file__), "../lib/jsons/languages.json")
	if languageJSON and os.path.isfile(languageJSON):
		with codecs.open(languageJSON) as f:
			languageDict = json.load(f)
	sys.path.append(os.path.join(os.path.dirname(__file__), "../lib/classes"))
	return languageDict


	
class JsonLoader:
	def __init__(self):
	
		self.factionNames = GetFactionNames()
		self.language = GetLanguageFile()
		self.missionTypes = GetMissionType()
		self.relicNames = GetRelics()
		self.solNodes = GetSolNodes()
		self.bosses = GetBossLocations()
		self.navMissions = GetNavMissionNodes()
		#self.syndicateNames = 
		#self.warframes = 
		#self.weapons = 
		#self.factionNames = os.path.join(os.path.dirname(__file__), "/lib/jsons/factionNames.json")
		#self.missionTypes = os.path.join(os.path.dirname(__file__), "/lib/jsons/missionTypes.json")
		#self.relicNames = os.path.join(os.path.dirname(__file__), "/lib/jsons/relicNames.json")
		#self.solNodes = os.path.join(os.path.dirname(__file__), "/lib/jsons/solNodes.json")
		#self.syndicateNames = os.path.join(os.path.dirname(__file__), "/lib/jsons/syndicateNames.json")
		#self.warframes = os.path.join(os.path.dirname(__file__), "/lib/jsons/warframes.json")
		#self.weapons = os.path.join(os.path.dirname(__file__), "/lib/jsons/weapons.json")
		
	def getBossNames(self):
		return self.bosses
		
	def getFactionNames(self):
		return self.factionNames
		
	def getLanguageFile(self):
		return self.language
		
	def getMissionTypes(self):
		return self.missionTypes
		
	def getNavMissions(self):
		return self.navMissions
		
	def getRelicNames(self):
		return self.relicNames
	
	def getSolNodes(self):
		return self.solNodes
		
	def getSyndicatenames(self):
		return self.syndicateNames
		
	def getWarframes(self):
		return self.warframes
		
	def getWeapons(self):
		return self.weapons