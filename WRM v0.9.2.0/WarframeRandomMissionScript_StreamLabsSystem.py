#---------------------------------------
#   Import Libraries
#---------------------------------------

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

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
import WRMRandomizer
import WRMWorldDataMissions
# Reference by filename import <filename>.function

#---------------------------------------
#   [Required]  Script Information
#---------------------------------------
ScriptName = "Warframe Random Mission Script"
Website = "http://www.twitch.tv/rickie26k"
Description = "!wrmmission"
Creator = "Rickie26k"
Version = "0.9.2.0"

#---------------------------------------
#   Set Variables
#---------------------------------------

SettingsFile = os.path.join(os.path.dirname(__file__), "WRMConfig.json")
# TODO POPULATE settingsOptions
#	nightmare, kuvafarm and 
#
settingsOptions = ["togSpecialIgnoreType","togSpecialIgnoreZone",
"togAlerts","alertWeight","togArchwing","archwingWeight",
"togBosses","bossWeight","togNightmare","nightmareWeight",
"togSyndicate", "togSyndicateWeight",
"togRelics","relicWeight","togLith","togMeso","togNeo","togAxi",
"togCetus","cetusWeight",
"togInvasions","invasionWeight","togKuvaFarm","kuvafarmWeight",
"togRegular","togMercury","togVenus","togEarth","togMars","togPhobos",
"togCeres","togJupiter","togEuropa","togSaturn","togUranus","togNeptune",
"togPluto","togEris","togSedna","togVoid1","togVoid2","togVoid3",
"togVoid4","togDerelict","togLua","togKuvaFortress","togCapture",
"togDefection","togDefense","togExcavation","togExterminate","togHijack",
"togInfestedsalvage","togInterception","togMobileDefense","self.togRescue"
"togSpy",
"togSurvival","togArena","togSabotage","togDeceptionS","togHiveS",
"togOrokinS","togSealabS"]
weightActions = []

#---------------------------------------
#	Functions
#---------------------------------------
def sendMessage(a, b):
	global MySettings, SettingsFile
	
	# a = Person, b = String
	
	# Checks to see if WHISPER is ENABLED
	if MySettings.togWhisper :
		Parent.SendTwitchMessage(b)
		# Parent.SendTwitchWhisper(a, b)
	else:
		Parent.SendTwitchMessage(b)

def RunUpdateAndRespond():
	global Manager, MySettings, WorldDataMissions
	
	freshWorld = UpdateWorldState(True)
	updated = Manager.UpdateManager(WorldDataMissions, MySettings)
	if updated == True:
		selectedMission = Manager.SelectMission()
		Parent.SendTwitchMessage("{0}".format(selectedMission))
	return

def ShouldUpdateData():
	global WorldDataMissions
	
	if not 'WorldDataMissions' in globals():
		return True
	else:
		return WorldDataMissions.ShouldUpdate()
	
def RequestWorldData():
	worldStateResponse = Parent.GetRequest("http://content.warframe.com/dynamic/worldState.php",{})
	responseObject = json.loads(worldStateResponse)
	worldDataObject = json.loads(responseObject['response'])
	
	#PrintWorldData(worldDataObject)
	return worldDataObject
	
def UpdateWorldState(worldDataExists):
	global MySettings, WorldDataMissions
	unix = datetime.datetime.today()
	#Check if worldData already exists
	
	if not worldDataExists:
		fetchedWorldData = RequestWorldData()
		worldDataObject = WRMWorldDataMissions.WorldData(MySettings, fetchedWorldData, Parent, unix)
		return worldDataObject
	else:
		if ShouldUpdateData():
			fetchedWorldData = RequestWorldData()
			WorldDataMissions.buildMissions(MySettings, fetchedWorldData, Parent, unix)
		return
#---------------------------------------
# Classes
#---------------------------------------
class Settings:
	
	# Tries to load settings from file if given else set defaults
	# The 'default' variable names need to match UI_Config
	def __init__(self, SettingsFile = None):
		if SettingsFile and os.path.isfile(SettingsFile):
			with codecs.open(SettingsFile, encoding="utf-8-sig", mode="r") as f:
				self.__dict__ = json.load(f, encoding="utf-8")
		else:
			self.togLive = True
			self.permission = "Subscriber"
			self.command = "!wrmrandom"
			self.cmdHelp = "!wrmhelp"
			self.cmdVersion = "!wrmversion"
			self.togCooldown = True
			self.togCooldownCaster = False
			self.timerCooldown = 60
			self.togSpecialIgnoreType = False
			self.togSpecialIgnoreZone = False
			self.togSpecialOverwrite = False
			self.togBosses = True
			self.bossWeight = 1
			self.togArchwing = True
			self.archwingWeight = 1
			self.togAlerts = True
			self.alertWeight = 1
			self.togRelics = True
			self.relicWeight = 1
			self.togLith = True
			self.togMeso = True
			self.togNeo = True
			self.togAxi = True
			self.togCetus = True
			self.cetusWeight = 1
			self.togInvasions = True
			self.invasionWeight = 1
			self.togRegular = True
			self.togMercury = True
			self.togVenus = True
			self.togEarth = True
			self.togMars = True
			self.togPhobos = True
			self.togCeres = True
			self.togJupiter = True
			self.togEuropa = True
			self.togSaturn = True
			self.togUranus = True
			self.togNeptune = True
			self.togPluto = True
			self.togEris = True
			self.togSedna = True
			self.togVoid1 = True
			self.togVoid2 = True
			self.togVoid3 = True
			self.togVoid4 = True
			self.togDerelict = True
			self.togLua = True
			self.togKuvaFortress = True
			self.togCapture = True
			self.togDefection = True
			self.togDefense = True
			self.togExcavation = True
			self.togExterminate = True
			self.togHijack = True
			self.togInfestedsalvage = True
			self.togInterception = True
			self.togMobileDefense = True
			self.togRescue = True
			self.togSpy = True
			self.togSurvival = True
			self.togArena = True
			self.togSabotage = True
			self.togDeceptionS = True
			self.togHiveS = True
			self.togOrokinS = True
			self.togSealabS = True			
			self.settingsConfig = "!wrmsettings"
			self.settingsConfigList = "!wrmsettingslist"
			self.settingsPermission = "Caster"
			self.respSettingsEmpty = "{0} config Syntax: {1} [Check commands with {2}] <0 to 100>. Do not enter a number amount if you want to learn more about each option."
			self.respSettingsInvalidAmount = "{0}, sorry but the amount that you entered must be a numeric value 1 to 100."
			self.respSettingsInvalidAction = "{0}, sorry but {1} is an invalid setting. Please use !wrmsettingslist to see list of settings to change."
			self.respNotLive = "Sorry {0}, but the stream must be live in order to use that command."
	
	# Reload settings on save through UI
	def ReloadSettings(self, data):
		self.__dict__ = json.loads(data, encoding="utf-8")
		Parent.Log('Settings', 'Reloaded.')
		return

	# Save settings to files (json and js)
	def SaveSettings(self, settingsFile):
		with codecs.open(SettingsFile, encoding="utf-8-sig", mode="w+") as f:
			json.dump(self.__dict__, f, encoding="utf-8")
		with codecs.open(SettingsFile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
			f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8')))
		Parent.Log('Settings', 'Saved.')
		return

#---------------------------------------
#   [Required] Intialize Data (Only called on Load)
# SSR SPR---------------------------------------
def Init():
	global MySettings, Manager, WorldDataMissions, unix
	unix = time.time()
	MySettings = Settings(SettingsFile)
	WorldDataMissions = UpdateWorldState(False)
	Manager = WRMRandomizer.Manager(WorldDataMissions,MySettings,Parent)
	
	#PrintTheBunch(WorldDataMissions)
	return

#---------------------------------------
#   [Required] Execute Data / Process Messages
# SSR---------------------------------------
def Execute(data):
	global MySettings, Manager, WorldDataMissions, unix
	user = data.User
	
	if data.IsChatMessage():
		if data.GetParam(0).lower() == MySettings.command and Parent.HasPermission(user, MySettings.permission, ""):
			
			# Checks to see if the stream needs to be LIVE and IS LIVE 
			if not MySettings.togLive or Parent.IsLive():
				timerCooldown = Parent.GetUserCooldownDuration(ScriptName, MySettings.command, user)
						
					# Checks to see if USER is on COOLDOWN
				if (MySettings.togCooldown and Parent.IsOnUserCooldown(ScriptName, MySettings.command, user)):
					# Checks to see if USER is the CASTER and CASTER COOLDOWN is ENABLED
					if not Parent.HasPermission(user, "Caster", "") :
						Parent.SendTwitchMessage(MySettings.respCooldownUser.format(user, timerCooldownUser))
					elif MySettings.togCooldownCaster and Parent.HasPermission(user, "Caster", "") :
						Parent.SendTwitchMessage(MySettings.respCooldownUser.format(user, timerCooldownUser))
				else:
					if ShouldUpdateData():
						RunUpdateAndRespond()
					else:
						selectedMission = Manager.SelectMission()
						Parent.SendTwitchMessage("{0}".format(selectedMission))
			else:
				Parent.SendTwitchMessage(MySettings.respNotLive.format(user))
				
		# SETTINGS COMMANDS
		elif data.GetParam(0).lower() == MySettings.settingsConfig and Parent.HasPermission(user, MySettings.settingsPermission, ""):
		
			
			if data.GetParamCount() == 1 :
				Parent.SendTwitchMessage(MySettings.respConfigEmpty.format(user, MySettings.settingsConfig, MySettings.settingsConfigList))

			else:
				configAction = data.GetParam(1).lower()
						
				# Checks to see if a proper ACTION was inputted
				
				if configAction in settingsOptions:
					# Checks to see if an AMOUNT was inputted
						# Checks to see if amount is a valid amount
						try:
							configAmount = int(data.GetParam(2))
						except:
							configAmount = -1
						
						# Checks if weight settings is attempted to be changed
						if configAction in weightActions:
							# Checks to see if AMOUNT is between 0 and 100
							if configAmount < 1 or configAmount > 100 :
								Parent.SendTwitchMessage(MySettings.respSettingsInvalidAmount.format(user))
							else:
								#TODO change setting and send response of changed settings value
								Parent.SendTwitchMessage()
						else:
							jazz = 0
							#TODO ensure value is 0 or 1
							#TODO change a setting
				else:
					Parent.SendTwitchMessage(MySettings.respSettingsInvalidAction.format(user, configAction.upper()))
						
		# SCRIPT VERSION
		elif data.GetParam(0).lower() == MySettings.cmdVersion and (Parent.HasPermission(user, "Caster", "") or user == "zerro0713"):
			Parent.SendTwitchMessage("{0} v{1} Created By: {2} at {3}".format(ScriptName, Version, Creator, Website))
	return

#---------------------------------------
#   [Optional] Parse Function
#	Parse whatever to whatever
# SSO SPO---------------------------------------
def Parse(parseString,user,target,message):
	if "$protocol26" in parseString:
		return parseString.replace("$protocol26","You will comply or you will be assimilated.")
	return parseString

#---------------------------------------
#   [Optional] ReloadSettings Function
#	The ReloadSettings function is an optional function that you can add that will
#	automatically be called once a user clicks on the Save Settings button in the scripts tab.
#	The entire Json object will be passed to the function so you can load that back into your
#	settings	
# wipe use settings prior to reload. In Unload()
# SSO SPO---------------------------------------
def ReloadSettings(jsonData):
	global MySettings, Manager, WorldDataMissions
	MySettings.ReloadSettings(jsonData)
	
	UpdateWorldState(True)
	Manager.UpdateManager(WorldDataMissions, MySettings)
	
	return

#---------------------------------------
#   [Optional] Unload Function
# SSO SPO---------------------------------------
def Unload():
	#Triggers when the bot closes / script is reloaded
	global MySettings
	MySettings.SaveSettings(SettingsFile)
	return

#---------------------------------------
#   [Optional] Script Toggle Function
# SSO ---------------------------------------

def ScriptToggled(state):
	global MySettings
	if not state:
		MySettings.SaveSettings(SettingsFile)
	return

	
#---------------------------------------
#   [Required] Tick Function
#	This is the Tick function and will be executed every time the program progresses. As you
#	can see there is no data variable here. So use this function when you don't require data
#	but want to do something while there is no data.
#	make a timer thing?
# SSR---------------------------------------
def Tick():
	return
	
def PrintTheBunch():
	global WorldDataMissions
	rMissions = WorldDataMissions.getRegularDict()
	Parent.Log('regMisLen', str(len(rMissions)))
	PrintMissions('rMis', rMissions)
	aMissions = WorldDataMissions.getAlertDict()
	PrintMissions('aMis', aMissions)
	fMissions = WorldDataMissions.getFissureDict()
	PrintMissions('fMis', fMissions)
	iMissions = WorldDataMissions.getInvasionDict()
	PrintMissions('iMis', iMissions)
	cMissions = WorldDataMissions.getCetusDict()
	PrintMissions('cMis', cMissions)
	return

def PrintMissions(origin, missionDict):
	try:
		iterData = iter(missionDict)
		isIter = True
	except TypeError, te:
		isIter = False
		Parent.Log('WRM failed iter', '<nil>')
	if isIter:
		for subsection in iterData:
			printme = json.dumps(missionDict[subsection], encoding='utf-8', ensure_ascii=False)
			Parent.Log(origin,printme)
	
def PrintWorldData(worldData):
	for section in worldData:
		printme = json.dumps(section, encoding='utf-8', ensure_ascii=False)
		Parent.Log('WRMSs', printme)
	isIter = False
	iterData = {}
	try:
		iterData = iter(worldData[section])
		isIter = True
	except TypeError, te:
		isIter = False
	if isIter:
		for subsection in iterData:
			printme = json.dumps(subsection, encoding='utf-8', ensure_ascii=False)
			if len(printme) > 3:
				Parent.Log('WRMSu', printme)
			if type(subsection) is list:
				if 'Tags' in iterData[subsection]:
					printbe = json.dumps(subsection['jobs'], encoding='utf-8', ensure_ascii=False)
					Parent.Log('WRMSs', printbe)
	else:
		printme = json.dumps(worldData.data[section], ensure_ascii=False)
		Parent.Log('WRMSi', printme)
	
	for section in worldData['Alerts']:
		printme = json.dumps(section, encoding='utf-8', ensure_ascii=False)
		Parent.Log('WRMSn', printme)
	return