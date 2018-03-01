
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
import math

sys.path.append(os.path.join(os.path.dirname(__file__), "../lib/classes"))
import Node
sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))
import timeDate



def GetRelicsDict():
	relicNamesJSON = os.path.join(os.path.dirname(__file__), "../../lib/jsons/relicNames.json")
	if relicNamesJSON and os.path.isfile(relicNamesJSON):
		with codecs.open(relicNamesJSON) as f:
			relicNames = json.load(f)
	sys.path.append(os.path.join(os.path.dirname(__file__), "../lib/classes"))
	return relicNames
	
def GetFactionNames():
	factionNamesJSON = os.path.join(os.path.dirname(__file__), "../../lib/jsons/factionNames.json")
	if factionNamesJSON and os.path.isfile(factionNamesJSON):
		with codecs.open(factionNamesJSON) as f:
			factionNames = json.load(f)
	sys.path.append(os.path.join(os.path.dirname(__file__), "../lib/classes"))
	return factionNames

# TODO only fetch language.json once ?
def GetLanguageFile():
	languageJSON = os.path.join(os.path.dirname(__file__), "../../lib/jsons/languages.json")
	if languageJSON and os.path.isfile(languageJSON):
		with codecs.open(languageJSON) as f:
			languageDict = json.load(f)
	sys.path.append(os.path.join(os.path.dirname(__file__), "../lib/classes"))
	return languageDict
#--------------------------------------------
#
#Alert MissionInfo:
#	MissionReward
#		countedItems
#			[ItemType: type, ItemCount: int]
#			credits: int credits
#	difficulty: float
#	maxWaveNum: int
#	missionType: type
#	levelOverride: tileset
#	minEnemyLevel: int
#	maxEnemyLevel: int
#	enemySpec: tileset
#	seed: int
#	faction: faction
#	location: solNode
#	_id
#		$oid: string
#	Activation
#		$date
#			$numberLong: int
#	Expiry
#		$date
#			$numberLong: int
#	solNode:
#		value: name (<zone>),
#   	enemy: enemy,
#    	type : missionType
#
#Fissure MissionInfo:
#	Region: <zone>
#	Modifier: <VoidTier>
#	MissionType: <MissionType>
#	Activation: 
#		$date
#			$numberLong: LongInt
#	Expiry:
#		$date
#			$numberLong: LongInt
#	_id:
#		$oid: <idString>
#	Seed: <SeedInt>
#	Node: <SolNode>
#
#Invasion MissionInfo:
#	Node: solNode
#	_id:
#		$oid: <idString>
#	Faction: FactionString
#	Completed: Boolean
#	Count: Int
#	LocTag: LanguageString
#	Goal: Int
#	Activation:
#		$date:
#			$numberLong: LongInt
#	Expiry
#		$date
#			$numberLong: LongInt
#	AttackReward:
#		[] OR
#		countedItems: [
#			ItemType: LanguageString
#			ItemCount: int ]
#	DefenderReward:
#		[] OR
#		countedItems: [
#			ItemType: LanguageString
#			ItemCount: int ]
#	AttackerMissionInfo:
#		seed: Int
#		faction: FactionString
#	DefenderMissionInfo:
#		seed: Int
#		faction: FactionString
#
#Cetus MissionInfo:
#	Tag: "CetusSyndicate"
#	_id:
#		$oid: <idString>
#	Nodes: [null]
#	Seed: int
#	Jobs: [
#		jobType: <BountyString>
#		minEnemyLevel: int
#		maxEnemyLevel:	int
#		masteryReq: int
#		rewards: <TierXTableRewards>
#		xpAmounts: [
#			<int>]]
#	Activation:
#		$date:
#			$numberLong: LongInt
#	Expiry
#		$date
#			$numberLong: LongInt
#--------------------------------------------
#

class Mission:
	def __init__(self, nData, node, spData):
		#using nData, normally directly from solNodes
		if nData != False:
			if type(node) is str:
				self.node = Node.Node(nData, node, True)
				self.basic = True
				self.spType = 'Nope'
			else: # REDUNDANT?
				self.activation = nData.Activation
				self.expiry = nData.Expiry
				self.basic = False
		elif spData != False:
			if type(node) is str:
				if 'spType' in spData:
					self.spType = spData['spType']
					if self.spType == 'alert':
						self.node = Node.Node(spData['MissionInfo'], node, False)
					else:
						self.node = Node.Node(spData, node, False)
					self.basic = False
					self.specialDataInserts(spData)
				else:
					self.spType = 'LOST'
		
		return
		
	# TODO rewards
		
	def specialDataInserts(self, data):
		self.activation = timeDate.parseDate(data['Activation'])
		if self.spType == 'alert':
			self.expiry = timeDate.parseDate(data['Expiry'])
			self.eta = self.getETAString()
			self.expired = self.getExpired()
		elif self.spType == 'fissure':
			self.expiry = timeDate.parseDate(data['Expiry'])
			self.eta = self.getETAString()
			self.expired = self.getExpired()
			tierTypes = GetRelicsDict()
			self.tier = (tierTypes[data['Modifier']])['value']
		elif self.spType == 'invasion':
			self.defenderFaction = (GetFactionNames())[data['DefenderMissionInfo']['faction']]
			self.attackerFaction = (GetFactionNames())[data['AttackerMissionInfo']['faction']]
				
			self.completed = data['Completed']
			self.count = data['Count']
			self.requiredRuns = data['Goal']
			
			if self.attackerFaction != 'Infested':
				self.vsInfestation = False
				self.completion = (1+(self.count / self.requiredRuns)) * 50
			else:
				self.vsInfestation = True
				self.completion = (1+(self.count / self.requiredRuns)) * 100
			
			self.eta = self.getETAInvasion()
			
		elif self.spType == 'bounty':
			self.masteryReq = data['masteryReq']
			self.jobType = ((GetLanguageFile())[(data['jobType']).lower()])['value']
		else:
			return
		
		
		return
	
	def toDict(self):
		node = self.getNode()
		id = self.getNodeId()
		dictNode = node.toDict()
		return {'id': id,'node': dictNode,'isBasic': self.isBasic(),'spType': self.getSpType()}
	
	def toJson(self):
		node = self.getNode()
		id = self.getNodeId()
		jsonNode = node.toDict()
		jsonMission = {'id': id,'node': jsonNode,'isBasic': self.isBasic(), 'spType': self.getSpType()}
		return json.dumps(jsonMission, ensure_ascii=False, encoding="utf-8")
	
	def getNode(self):
		return self.node
		
	def getNodeId(self):
		return self.node.id
		
	def getName(self):
		return self.node.name
	
	def getZone(self):
		return self.node.zone
		
	def getFaction(self):
		return self.node.faction
	
	def getType(self):
		return self.node.type
		
	def isBasic(self):
		return self.basic
	
	def getGear(self):
		return self.node.getGear()
	
	def getSpType(self):
		return self.spType
		
	def getActivation(self):
		if type(self.activation) is str:
			return self.Activation
		else:
			return ''
	
	def getExpiration(self):
		if type(self.expiry) is str:
			return self.Expiry
		else:
			return ''
			
	def getRemainingTime(self):
		completedRuns = abs(self.count);
		if completedRuns == 0:
			completedRuns = 1
		elapsedMillis = timeDate.toNow(self.activation);
		remainingRuns = self.requiredRuns - completedRuns;
		return remainingRuns * (elapsedMillis / completedRuns);
	
	def getETAString(self):
		return timeDate.timeDeltaToString(timeDate.fromNow(self.expiry))
		
	def getETAInvasion(self):
		return timeDate.timeDeltaToString(self.getRemainingTime())
			
	def getExpired(self):
		return timeDate.fromNow(self.expiry) < 0;
	
	def getRelicTier(self):
		if hasattr(self,'tier'):
			return self.tier
		else:
			return False
	
	def getJobType(self):
		if hasattr(self,'jobType'):
			return self.jobType
		else:
			return False
		
	def getMasteryReq(self):
		return self.masteryReq