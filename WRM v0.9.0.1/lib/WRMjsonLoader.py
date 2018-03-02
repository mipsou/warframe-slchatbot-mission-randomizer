
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

class JsonLoader:
	factionNames = os.path.join(os.path.dirname(__file__), "/lib/jsons/factionNames.json")
	missionTypes = os.path.join(os.path.dirname(__file__), "/lib/jsons/missionTypes.json")
	relicNames = os.path.join(os.path.dirname(__file__), "/lib/jsons/relicNames.json")
	solNodes = os.path.join(os.path.dirname(__file__), "/lib/jsons/solNodes.json")
	syndicateNames = os.path.join(os.path.dirname(__file__), "/lib/jsons/syndicateNames.json")
	warframes = os.path.join(os.path.dirname(__file__), "/lib/jsons/warframes.json")
	weapons = os.path.join(os.path.dirname(__file__), "/lib/jsons/weapons.json")