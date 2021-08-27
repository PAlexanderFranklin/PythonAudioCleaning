import keyboard
import os
from pathlib import Path
import subprocess
import time
from win32gui import GetForegroundWindow, GetWindowText

import populateMetaData

# Off by default because this is use-case specific
useMetaData = False

# Setup
#   pip install (modules that are imported above)
#   Change Audacity preferences:
#       Set audacity keyboard preferences to the keys in the "Hotkeys" section below
#   Set effect defaults in Audacity:
#       "Label Sounds"
#           Regions between sounds 
#           Threshold level:          (-22.0 db seems to work)
#           Minimum silence duration: 2 seconds
#           Label type:               Region between sounds
#       "Compressor"
#           Set attack and release times to their minimum value

# Audacity Hotkeys
compressorKey = "ctrl+H"
cursorToTrackEndKey = "shift+K"
exportAudioKey = "ctrl+shift+E"
importAudioKey = "ctrl+shift+I" # default
labelSoundsKey = "alt+L"
nextLabelKey = "alt+]"
noiseReductionKey = "alt+R"
normalizeKey = "alt+N"
removeTracksKey = "alt+T"
selectAllKey = "ctrl+A" # default
trackStartToCursorKey = "L"

# Configure
source = Path.cwd() / "Source"
destination = Path.cwd() / "Destination"
backup = Path.cwd() / "Backup"

# Audacity executable path
AudacityPath = Path("C:/Program Files (x86)/Audacity/audacity.exe")

Audacity = subprocess.Popen(AudacityPath)

# Store Audacity Window for checking when effects are finished processing
while (GetWindowText(GetForegroundWindow()) != "Audacity"):
    time.sleep(0.5)
mainAudacityWindow = GetForegroundWindow()

# Terminate script from anywhere
keyboard.add_hotkey("ctrl+c", lambda: os._exit(0))


def typeCommands(commandList):
    for command in commandList:
        time.sleep(0.25)
        keyboard.send(command)
        if(command == "enter"):
            while True:
                time.sleep(2)
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

def cleanAudio():
    typeCommands([
        selectAllKey, normalizeKey, "enter", 
        labelSoundsKey, "enter", nextLabelKey, 
        noiseReductionKey, "tab", "tab", "tab", "tab", "enter",
        selectAllKey, noiseReductionKey, 
        "enter", compressorKey, "enter", exportAudioKey
    ])
    if useMetaData:
        populateMetaData.foo(GetWindowText(mainAudacityWindow))

# Changes hotkey behaviour after first press
def initialClean():
    typeCommands([
        selectAllKey, noiseReductionKey, "enter",
        selectAllKey, normalizeKey, "enter", 
        labelSoundsKey, "enter", nextLabelKey, 
        noiseReductionKey, "tab", "tab", "tab", "tab", "enter",
        selectAllKey, noiseReductionKey, "enter",
        compressorKey, "enter", exportAudioKey
    ])
    if useMetaData:
        populateMetaData.foo(GetWindowText(mainAudacityWindow))
    keyboard.remove_hotkey(initialHotkey)
    keyboard.add_hotkey("g", cleanAudio)

# Script Hotkeys
keyboard.add_hotkey("a", importAndBackup)
keyboard.add_hotkey("s", typeCommands, args=[[selectAllKey, normalizeKey, "enter"]])
keyboard.add_hotkey("d", typeCommands, args=[[trackStartToCursorKey, "backspace"]])
keyboard.add_hotkey("f", typeCommands, args=[[cursorToTrackEndKey, "backspace"]])
keyboard.add_hotkey("h", storeBackup)

# This hotkey needs to do something different the first time,
# so it calls a function that replaces it
initialHotkey = keyboard.add_hotkey("g", initialClean)

# Keep the script from closing for one hour so that hotkeys work
for i in range(0, 720):
    time.sleep(5)
    # Close Script when Audacity closes
    # Doesn't work in VSCode, but does work when script is started normally
    if Audacity.poll() == 0:
        storeBackup()
        os._exit(0)
        
storeBackup()