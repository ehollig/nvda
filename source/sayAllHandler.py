#sayAllHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2012 NVDA Contributors
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import speech
import synthDriverHandler
from logHandler import log
import config

CURSOR_CARET=0
CURSOR_REVIEW=1

lastSayAllMode=None

def stop():
	"""Stop say all if a say all is in progress.
	"""
	synth = synthDriverHandler.getSynth()
	if synthDriverHandler.synthIndexReached not in synth.supportedNotifications:
		log.debugWarning("Compat: Using speechCompat.sayAll_stop")
		# Import late to avoid circular import.
		import speechCompat
		return speechCompat.sayAll_stop()

def isRunning():
	"""Determine whether say all is currently running.
	@return: C{True} if say all is currently running, C{False} if not.
	@rtype: bool
	@note: If say all completes and there is no call to L{stop} (which is called from L{speech.cancelSpeech}), this will incorrectly return C{True}.
		This should not matter, but is worth noting nevertheless.
	"""
	synth = synthDriverHandler.getSynth()
	if synthDriverHandler.synthIndexReached not in synth.supportedNotifications:
		log.debugWarning("Compat: Using speechCompat.sayAll_isRunning")
		# Import late to avoid circular import.
		import speechCompat
		return speechCompat.sayAll_isRunning()

def readObjects(obj):
	synth = synthDriverHandler.getSynth()
	if synthDriverHandler.synthIndexReached not in synth.supportedNotifications:
		log.debugWarning("Compat: Using speechCompat.sayAll_readObjects")
		# Import late to avoid circular import.
		import speechCompat
		return speechCompat.sayAll_readObjects()

def readText(cursor):
	global lastSayAllMode
	lastSayAllMode=cursor
	synth = synthDriverHandler.getSynth()
	if synthDriverHandler.synthIndexReached not in synth.supportedNotifications:
		log.debugWarning("Compat: Using speechCompat.sayAll_readText")
		# Import late to avoid circular import.
		import speechCompat
		return speechCompat.sayAll_readText(cursor)

class SayAllProfileTrigger(config.ProfileTrigger):
	"""A configuration profile trigger for when say all is in progress.
	"""
	spec = "sayAll"
