
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

sys.path.append(os.path.join(os.path.dirname(__file__), "../lib/classes"))
import Mission


def GetSolDict():
	solNodesJSON = os.path.join(os.path.dirname(__file__), "../lib/jsons/solNodes.json")
	if solNodesJSON and os.path.isfile(solNodesJSON):
		with codecs.open(solNodesJSON) as f:
			solNodes = json.load(f)
	sys.path.append(os.path.join(os.path.dirname(__file__), "../lib/classes"))
	return solNodes

#--------------------------------------------
#
#JSON Alert MissionInfo:
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
#			$numberLong: LongInt
#	Expiry
#		$date
#			$numberLong: LongInt
#--------------------------------------------
#	MissionInfo is found on any special mission JSON point

def ExtractAlertMissions(data, settings, parent):
	missionDict = {}
	solNodes = GetSolDict()
	#.Alerts
	for mission in data:
			
		node = mission['MissionInfo']['location']
		solNodeInfo = solNodes[node]
		mission['MissionInfo']['solNode'] = solNodeInfo
		mission['spType'] = 'alert'
		
		missionDict[node] = Mission.Mission(False, node, mission)
	
	return missionDict
	
#----------------------------------------------
#
#JSON Fissure info:
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
#----------------------------------------------

def ExtractFissureMissions(data, settings, parent):
	missionDict = {}
	solNodes = GetSolDict()
	#.ActiveMissions
	
	for mission in data:
		
		#jsonMis = json.dumps(mission, encoding='utf-8', ensure_ascii=False)
		#parent.Log('Fissurestruct', jsonMis)
		node = mission['Node']
		solNodeInfo = solNodes[node]
		mission['solNode'] = solNodeInfo
		mission['spType'] = 'fissure'
		
		missionDict[node] = Mission.Mission(False, node, mission)
	
	return missionDict

#-----------------------------------------------
#
#JSON Invasion info:
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
#-----------------------------------------------

def ExtractInvasionMissions(data, settings, parent):
	missionDict = {}
	solNodes = GetSolDict()
	#.Invasions
	
	for mission in data:
		
		#jsonMis = json.dumps(mission, encoding='utf-8', ensure_ascii=False)
		#parent.Log('invasionstruct', jsonMis)
		node = mission['Node']
		solNodeInfo = solNodes[node]
		mission['solNode'] = solNodeInfo
		mission['spType'] = 'invasion'
		
		missionDict[node] = Mission.Mission(False, node, mission)
	
	return missionDict

#-----------------------------------------------
#
#JSON Cetus Info:
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
#
#-----------------------------------------------
def ExtractCetusMissions(data, settings, parent):
	
	missionDict = {}
	cetusInfo = {}
	#cetusInfo['Jobs'] == [bountyMissions]
	
	for syndicate in data:
		if syndicate['Tag'] == 'CetusSyndicate':
			cetusInfo = syndicate
	
	#jsonMis = json.dumps(cetusInfo, encoding='utf-8', ensure_ascii=False)
	#parent.Log('cetusstruct', jsonMis)
	
	for mission in cetusInfo['Jobs']:
		node = cetusInfo['_id']['$oid'] + str(mission['masteryReq'])
		mission['_id']= {'$oid': node}
		
		solNodeInfo = {'value': 'Plains (Earth)','enemy': 'FC_GRINEER','type': mission['jobType']}
		mission['solNode'] = solNodeInfo
		mission['spType'] = 'bounty'
		mission['Activation'] = cetusInfo['Activation']
		mission['Expiry'] = cetusInfo['Expiry']
		mission['Seed'] = cetusInfo['Seed']
		missionDict[node] = Mission.Mission(False, node, mission)
	return missionDict

# Create a dict from solNodes to establish an interfacable data structure
# where each node is of class Mission.

def CompileMissionsList(settings, parent):
	#.solNodes
	missionDict = {}
	solNodes = GetSolDict()
			
	for node in solNodes:
		
		nodeface = json.dumps(node, encoding='utf-8', ensure_ascii=False)
		
		snode = solNodes[node]
		# Ensure type field is present
		if 'type' in snode:
			typeS = snode["type"]
		else:
			typeS = ''
		
		# Filter out Relays, placeholders and conclave missions
		if 'type' in snode and typeS != 'Ancient Retribution' and typeS != 'Conclave' and typeS != 'Relay':
	
			
			faceData = json.dumps(solNodes[node], encoding='utf-8', ensure_ascii=False)
			
			missionDict[node] = Mission.Mission(solNodes[node], node, False)
		
	return missionDict
	
def printMissionList(parent):
	solNodes = GetSolDict()
			
	for node in solNodes:
		
		nodeface = json.dumps(node, encoding='utf-8', ensure_ascii=False)
		parent.Log('Wrf', nodeface)
		
		snode = solNodes[node]
		if 'type' in snode:
			typeS = snode["type"]
		else:
			typeS = ''
		
		if 'type' in snode and typeS != 'Ancient Retribution' and typeS != 'Conclave':
	
			
			faceData = json.dumps(solNodes[node], encoding='utf-8', ensure_ascii=False)
			parent.Log('Wrf2', faceData)
			
	return