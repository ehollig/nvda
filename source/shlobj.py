# -*- coding: UTF-8 -*-
#shlobj.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2017 NV Access Limited, Babbage B.V.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""
This module wraps the SHGetKnownFolderPath function in shell32.dll and defines the necessary contstants.
The KNOWNFOLDERID constants represent GUIDs that identify standard folders registered with the system as Known Folders.
These folders are installed with Windows Vista and later operating systems,
and a computer will have only folders appropriate to it installed.
"""

from ctypes import *
from ctypes.wintypes import *
from comtypes import GUID

shell32 = windll.shell32

MAX_PATH = 260

#: The file system directory that serves as a common repository for application-specific data.
#: A typical path is C:\Users\username\AppData\Roaming
CSIDL_APPDATA = 0x001a
FOLDERID_RoamingAppData = GUID("{3EB685DB-65F9-4CF6-A03A-E3EF65729F3D}")

#: The file system directory that serves as a data repository for local (nonroaming) applications.
#: A typical path is C:\Documents and Settings\username\Local Settings\Application Data.
CSIDL_LOCAL_APPDATA = 0x001c
FOLDERID_LocalAppData = GUID("{F1B32785-6FBA-4FCF-9D55-7B8E7F157091}")

#: The file system directory that contains application data for all users.
#: A typical path is C:\ProgramData.
#: This folder is used for application data that is not user specific.
CSIDL_COMMON_APPDATA = 0x0023
FOLDERID_ProgramData = GUID("{62AB5D82-FDC1-4DC3-A9DD-070D1D495D97}")

def SHGetFolderPath(owner, folder, token=0, flags=0):
	path = create_unicode_buffer(MAX_PATH)
	# Note  As of Windows Vista, this function is merely a wrapper for SHGetKnownFolderPath
	if shell32.SHGetFolderPathW(owner, folder, token, flags, byref(path)) != 0:
		raise WinError()
	return path.value

def SHGetKnownFolderPath(rfid, flags=0, token=0):
	path = create_unicode_buffer(MAX_PATH)
	if shell32.SHGetKnownFolderPath(rfid, flags, token, byref(path)) != 0:
		raise WinError()
	return path.value
