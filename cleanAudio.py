import keyboard
import os
from pathlib import Path
import subprocess
import time
from win32gui import GetForegroundWindow, GetWindowText, GetClassName

import populateMetaData

# Off by default because this is use-case specific
useMetaData = False

# Setup
#   pip install (modules that are imported above)
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

# Audacity Hotkeys
compressorKey = "ctrl+J"
cursorToTrackEndKey = "shift+K"
exportAudioKey = "ctrl+shift+E"
importAudioKey = "ctrl+shift+I" # default
labelSoundsKey = "alt+L"
nextLabelKey = "alt+]"
noiseReductionKey = "alt+R"
normalizeKey = "alt+N"
removeTracksKey = "alt+T"
selectAllKey = "ctrl+A" # default
trackStartToCursorKey = "shift+L"

# Script Hotkeys
selectPreviousOptionKey = "ctrl+G"
executeOptionKey = "ctrl+F"
selectNextOptionKey = "ctrl+H"

# Configure
source = Path.cwd() / "Source"
destination = Path.cwd() / "Destination"
backup = Path.cwd() / "Backup"

# Audacity executable path
AudacityPath = Path("C:/Program Files (x86)/Audacity/audacity.exe")

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

def typeCommands(commandList):
    while keyboard.is_pressed('ctrl'):
        time.sleep(0.1)
    for command in commandList:
        time.sleep(0.25)
        keyboard.send(command)
        if(command == "enter"):
            while True:
                time.sleep(0.25)
                if (GetForegroundWindow() == mainAudacityWindow):
                    break

# Used to remove junk files from source without deleting them to avoid data loss
def storeBackup():
    set1 = set()
    set2 = set()
    for file in source.iterdir():
        set1.add(file.name)
    for file in destination.iterdir():
        set2.add(file.name)
    fileNameList = list(set1 & set2)
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
        for j in range (0, 8):
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
        compressorKey, "enter", exportAudioKey
    ])
    if useMetaData:
        populateMetaData.addDBEntry(GetWindowText(mainAudacityWindow))

macroOptions = [importAndBackup,
                normalizeAudio,
                deleteBeginning,
                deleteEnd,
                cleanAudio,
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