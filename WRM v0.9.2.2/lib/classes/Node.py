
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

def splitLocationValue(value):
	splitValue = value.split(" ")
	if splitValue[1] == 'Index':
		name = value
		zone = 'Neptune'
	elif len(splitValue) == 3:
		if splitValue[2][0:-1] == 'Fortress':
			name = splitValue[0]
			zone = splitValue[1][1:] + ' ' + splitValue[2][0:-1]
		else:
			name = splitValue[0] + ' ' + splitValue[1]
			zone = splitValue[2][1:-1]
	else:
		name = splitValue[0]
		zone = splitValue[1][1:-1]
	return [name, zone]

def getMissionType(value):
	splitValue = value.split(" ")
	if splitValue[0] == 'Dark':
		if len(splitValue) == 4:
			return [splitValue[2] + splitValue[3]]
		else:
			return splitValue[2]
	elif splitValue[-1] == '(Archwing)':
		if len(splitValue) == 3:
			return [splitValue[0] + ' ' + splitValue[1], 'Archwing']
		else:
			return [splitValue[0], 'Archwing']
	else:
		return value
	
class Node:
	def __init__(self, data, node, basic, jsonLoader):
	
		if basic == True:
			self.id = node
			location = splitLocationValue(data['value'])
			self.name = location[0]
			self.zone = location[1]
			
			if 'enemy' in data:
				self.faction = data['enemy']
			
			self.setTypeBySol(data['type'])
			if self.type == 'Assassination':
				bossNames = jsonLoader.getBossNames()
				enemyTxt = bossNames[self.name] + ', ' + self.faction
				self.faction = enemyTxt
		else:
			if '_id' in data:
				self.id = data['_id']['$oid']
			else:
				self.id = node
			
			location = splitLocationValue(data['solNode']['value'])
			self.name = location[0]
			self.zone = location[1]
			
			factionNames = jsonLoader.getFactionNames()
			if 'faction' in data:
				self.faction = factionNames[data['faction']]['value']
			elif data['solNode']['enemy'] in factionNames:
				self.faction = factionNames[data['solNode']['enemy']]['value']
			else:
				self.faction = data['solNode']['enemy']
				
			self.setTypeBySpecial(data, jsonLoader)
		return

	def __iter__(self):
		return self.__dict__
	
	def toDict(self):
		return self.__dict__
	
	def toJSON(self):
		return json.dumps(self, cls=NodeEncoder)
	
	def getId(self):
		return self.id
	
	def getName(self):
		return self.name
			
	def getZone(self):
		return self.zone
		
	def getFaction(self):
		return self.faction
	
	def getType(self):
		return self.type
		
	def getGear(self):
		return self.gear
		
	def setTypeBySol(self, data):
		mType = getMissionType(data)
		if type(mType) is list:
			if len(mType) > 1:
				self.type = mType[0]
				self.gear = mType[1]
		else:
			self.type = mType
			self.gear = 'Warframe'
		return
	
	def setTypeBySpecial(self, data, jsonLoader):
		if 'missionType' in data:
			mDict = jsonLoader.getMissionTypes()
			self.type = (mDict[data['missionType']])['value']
		
		if 'MissionType' in data:
			mDict = jsonLoader.getMissionTypes()
			self.type = (mDict[data['MissionType']])['value']
		if 'archwingRequired' in data:
			self.gear = 'Archwing'
		else:
			self.gear = 'Warframe'
		return