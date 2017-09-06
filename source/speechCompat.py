# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2017 NV Access Limited, Peter Vágner, Aleksey Sadovoy
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Speech code to support old synthesizers which don't support index and done speaking notifications, etc.
"""

import speech
from synthDriverHandler import getSynth
import tones
import queueHandler
import config
import characterProcessing
from logHandler import log

def getLastSpeechIndex():
	"""Gets the last index passed by the synthesizer. Indexing is used so that its possible to find out when a certain peace of text has been spoken yet. Usually the character position of the text is passed to speak functions as the index.
@returns: the last index encountered
@rtype: int
"""
	return getSynth().lastIndex

_speakSpellingGenerator=None

def speakSpelling(text,locale=None,useCharacterDescriptions=False):
	global _speakSpellingGenerator
	import speechViewer
	if speechViewer.isActive:
		speechViewer.appendText(text)
	if speech.speechMode==speech.speechMode_off:
		return
	elif speech.speechMode==speech.speechMode_beeps:
		tones.beep(config.conf["speech"]["beepSpeechModePitch"],speechMode_beeps_ms)
		return
	if speech.isPaused:
		speech.cancelSpeech()
	speech.beenCanceled=False
	defaultLanguage=speech.getCurrentLanguage()
	if not locale or (not config.conf['speech']['autoDialectSwitching'] and locale.split('_')[0]==defaultLanguage.split('_')[0]):
		locale=defaultLanguage

	if not text:
		# Translators: This is spoken when NVDA moves to an empty line.
		return getSynth().speak((_("blank"),))
	if not text.isspace():
		text=text.rstrip()
	if _speakSpellingGenerator and _speakSpellingGenerator.gi_frame:
		_speakSpellingGenerator.send((text,locale,useCharacterDescriptions))
	else:
		_speakSpellingGenerator=_speakSpellingGen(text,locale,useCharacterDescriptions)
		try:
			# Speak the first character before this function returns.
			next(_speakSpellingGenerator)
		except StopIteration:
			return
		queueHandler.registerGeneratorObject(_speakSpellingGenerator)

def _speakSpellingGen(text,locale,useCharacterDescriptions):
	synth=getSynth()
	synthConfig=config.conf["speech"][synth.name]
	buf=[(text,locale,useCharacterDescriptions)]
	for text,locale,useCharacterDescriptions in buf:
		textLength=len(text)
		count = 0
		localeHasConjuncts = True if locale.split('_',1)[0] in speech.LANGS_WITH_CONJUNCT_CHARS else False
		charDescList = speech.getCharDescListFromText(text,locale) if localeHasConjuncts else text
		for item in charDescList:
			if localeHasConjuncts:
				# item is a tuple containing character and its description
				char = item[0]
				charDesc = item[1]
			else:
				# item is just a character.
				char = item
				if useCharacterDescriptions:
					charDesc=characterProcessing.getCharacterDescription(locale,char.lower())
			uppercase=char.isupper()
			if useCharacterDescriptions and charDesc:
				#Consider changing to multiple synth speech calls
				char=charDesc[0] if textLength>1 else u"\u3001".join(charDesc)
			else:
				char=characterProcessing.processSpeechSymbol(locale,char)
			if uppercase and synthConfig["sayCapForCapitals"]:
				# Translators: cap will be spoken before the given letter when it is capitalized.
				char=_("cap %s")%char
			if uppercase and synth.isSupported("pitch") and synthConfig["capPitchChange"]:
				oldPitch=synthConfig["pitch"]
				synth.pitch=max(0,min(oldPitch+synthConfig["capPitchChange"],100))
			count = len(char)
			index=count+1
			log.io("Speaking character %r"%char)
			speechSequence=[LangChangeCommand(locale)] if config.conf['speech']['autoLanguageSwitching'] else []
			if len(char) == 1 and synthConfig["useSpellingFunctionality"]:
				speechSequence.append(speech.CharacterModeCommand(True))
			if index is not None:
				speechSequence.append(speech.IndexCommand(index))
			speechSequence.append(char)
			synth.speak(speechSequence)
			if uppercase and synth.isSupported("pitch") and synthConfig["capPitchChange"]:
				synth.pitch=oldPitch
			while textLength>1 and (speech.isPaused or getLastSpeechIndex()!=index):
				for x in xrange(2):
					args=yield
					if args: buf.append(args)
			if uppercase and  synthConfig["beepForCapitals"]:
				tones.beep(2000,50)
		args=yield
		if args: buf.append(args)
