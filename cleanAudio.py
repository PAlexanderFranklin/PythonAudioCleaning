import keyboard
import os
from pathlib import Path
import subprocess
import time
from win32gui import GetForegroundWindow, GetWindowText, GetClassName

from config import *
import populateMetaData

# Setup
#   pip install keyboard, pywin32
#   Written for Audacity 3.0.0
#   Probably broken for other versions due to menu changes
#   Change Audacity preferences:
#       Set audacity keyboard preferences to the keys in the "Hotkeys" section below
#       Remove Ctrl+F binding (Track Size - Fit to Width)
#   Set effect defaults in Audacity:
#       "Label Sounds"
#           Minimum silence duration: 2 seconds
#           Label type:               Region between sounds
#       "Compressor"
#           Set attack and release times to their minimum value

Audacity = subprocess.Popen(AudacityPath)

# When opened, Audacity has a different menu structure than after a noise profile is obtained.
getNoiseProfile = False

# Store Audacity Window for checking when effects are finished processing
while True:
    theWindow = GetForegroundWindow()
    if GetClassName(theWindow) == "wxWindowNR":
        if GetWindowText(theWindow) != "Audacity is starting up...":
            break
        else:
            getNoiseProfile = True
    time.sleep(0.25)
mainAudacityWindow = GetForegroundWindow()

# Terminate script from anywhere
keyboard.add_hotkey("ctrl+c", lambda: os._exit(0))

# Send multiple keys to keyboard
def typeCommands(commandList):
    while keyboard.is_pressed('ctrl'):
        time.sleep(0.1)
    while keyboard.is_pressed('shift'):
        time.sleep(0.1)
    for command in commandList:
        time.sleep(0.25)
        keyboard.send(command)
        if(command == "enter"):
            while (GetForegroundWindow() != mainAudacityWindow):
                time.sleep(0.25)

# Used to remove junk files from source without deleting them to avoid data loss
def storeBackup():
    set1 = set()
    set2 = set()

    # Get file names in source
    for file in source.iterdir():
        set1.add(file.name)

    # Get file names in destination
    for file in destination.iterdir():
        # Output should be in mp3, so filenames are converted to wav for pattern matching
        set2.add(file.name[:-4] + ".wav")
        set2.add(file.name[:-4] + ".WAV")
    
    fileNameList = list(set1 & set2) # Find the intersection of the two sets
    fileList = []
    for name in fileNameList:
        fileList.append(source / name)
    
    for file in fileList:
        try:
            with (backup / file.name).open(mode="xb") as fid:
                fid.write(file.read_bytes())
        except:
            print(file.name + " failed to copy")
        else:
            Path.unlink(file)
    
def importAndBackup():
    storeBackup()
    typeCommands([selectAllKey, removeTracksKey, importAudioKey])

def normalizeAudio():
    typeCommands([selectAllKey, normalizeKey, "enter"])

def deleteBeginning():
    typeCommands([trackStartToCursorKey, "backspace"])

def deleteEnd():
    typeCommands([cursorToTrackEndKey, "backspace"])

def labelSounds():
    for i in range (-28, -18):
        keyboard.send(selectAllKey)
        time.sleep(0.05)
        keyboard.send(labelSoundsKey)
        time.sleep(0.2)
        keyboard.write(str(i))
        keyboard.send("enter")
        time.sleep(0.2)
        for j in range (0, 15):
            LSWindow = GetForegroundWindow()
            time.sleep(1)
            newLSWindow = GetForegroundWindow()
            if newLSWindow == mainAudacityWindow:
                return
            if newLSWindow != LSWindow:
                keyboard.send("enter")
                break

def cleanAudio():
    # This "if" block is used to determine menu structure
    global getNoiseProfile
    if getNoiseProfile:
        typeCommands([selectAllKey, noiseReductionKey, "enter"])
        getNoiseProfile = False
    
    normalizeAudio()

    labelSounds()

    typeCommands([
        nextLabelKey, 
        noiseReductionKey, "tab", "tab", "tab", "tab", "enter",
        selectAllKey, noiseReductionKey, "enter",
        compressorKey, "enter"
    ])

def exportAudio():
    typeCommands([exportAudioKey])
    if useMetaData:
        populateMetaData.addDBEntry(GetWindowText(mainAudacityWindow))

macroOptions = [importAndBackup,
                normalizeAudio,
                deleteBeginning,
                deleteEnd,
                cleanAudio,
                exportAudio,
                storeBackup
                ]

optionCursor = 0

def selectPreviousOption():
    global optionCursor
    if optionCursor == 0:
        optionCursor = len(macroOptions) - 1
    else:
        optionCursor -= 1
    print(macroOptions[optionCursor].__name__)

def selectNextOption():
    global optionCursor
    if optionCursor == len(macroOptions) - 1:
        optionCursor = 0
    else:
        optionCursor += 1
    print(macroOptions[optionCursor].__name__)

def executeOption():
    global optionCursor
    macroOptions[optionCursor]()
    if optionCursor == len(macroOptions) - 1:
        optionCursor = 0
    else:
        optionCursor += 1
    print(macroOptions[optionCursor].__name__)

print(macroOptions[optionCursor].__name__)

# Script Hotkeys
keyboard.add_hotkey(selectPreviousOptionKey, selectPreviousOption)
keyboard.add_hotkey(selectNextOptionKey, selectNextOption)
keyboard.add_hotkey(executeOptionKey, executeOption)

# Keep the script from closing for one hour so that hotkeys work
for i in range(0, 720):
    time.sleep(5)
    # Terminate Script when Audacity closes
    if GetWindowText(mainAudacityWindow) == "":
        storeBackup()
        os._exit(0)
        
storeBackup()