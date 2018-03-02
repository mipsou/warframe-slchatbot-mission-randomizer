


import sys
import os
import math
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "../lib/classes"))

def timeDeltaToString(millis):
	
	if type(millis) != int:
		return '0'
	
	timePieces = []
	prefix = ''
	if millis < 0:
		prefix = '-'
	seconds = abs(millis / 1000)
		
	#build days
	if seconds >= 86400:
		days = math.floor(seconds / 86400)
		timePieces.append( days + 'd' )
		seconds = math.floor(seconds) % 86400
	
	#build hours
	if seconds >= 3600:
		hours = math.floor(seconds / 3600)
		timePieces.append( hours + 'h' )
		seconds = math.floor(seconds) % 3600
	
	#build minutes
	if seconds >= 60:
		minutes = math.floor(seconds / 60)
		timePieces.append( minutes + 'm' )
		seconds = math.floor(seconds) % 60
	
	#add remaining seconds
	
	if seconds >= 0:
		timePieces.append(math.floor(seconds))
	timeString = ''
	
	for i in timePieces:
		timeString =+ i
	
	return timeString

#* Returns the number of milliseconds between now and a given date
def fromNow(d, now = datetime.datetime.today()):
	#d - now 
	return (d - now).total_seconds() * 1000
	
#* Returns the number of milliseconds between a given date and now
def toNow(d, now = datetime.datetime.today()):
	#now - d 
	return (now - d).total_seconds() * 1000
	
#* Returns a new datetime constructed from a worldState date object
def parseDate(d):
	
	# dateObject = Date(d.$date ? Number(d.$date.$numberLong) : 1000 * d.sec);
	if '$date' in d:
		tdt = int(d['$date']['$numberLong']) / 1000
		
		#raise ValueError('A very specific bad thing happened.' + str(tdt))
	else:
		tdt = d.sec
		
	return datetime.datetime.utcfromtimestamp(tdt)