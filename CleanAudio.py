import keyboard
import os
from pathlib import Path
import subprocess
import time

# Setup
#   pip install keyboard
#   Change Audacity keyboard preferences:
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
compressor = "ctrl+H"
cursorToTrackEnd = "shift+K"
exportAudio = "ctrl+shift+E"
importAudio = "ctrl+shift+I" # default
labelSounds = "alt+L"
nextLabel = "alt+]"
noiseReduction = "alt+R"
normalize = "alt+N"
removeTracks = "alt+T"
selectAll = "ctrl+A" # default
trackStartToCursor = "L"

# Configure source, destination, and backup
source = Path.cwd() / "Source"
destination = Path.cwd() / "Destination"
backup = Path.cwd() / "Backup"

# Audacity executable path
AudacityPath = Path("C:/Program Files (x86)/Audacity/audacity.exe")

Audacity = subprocess.Popen(AudacityPath)

# Terminate script from anywhere
keyboard.add_hotkey("ctrl+c", lambda: os._exit(0))


def typeCommands(commandList):
    for command in commandList:
        keyboard.send(command)

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
    typeCommands([selectAll, removeTracks, importAudio])

# Changes hotkey behaviour after first press
def newHotkey():
    typeCommands([
        selectAll, noiseReduction, "enter",
        selectAll, normalize, "enter", 
        labelSounds, "enter", nextLabel, 
        noiseReduction, "tab", "tab", "tab", "tab", "enter",
        selectAll, noiseReduction, "enter",
        compressor, "enter", exportAudio
    ])
    keyboard.remove_hotkey(initialHotkey)
    keyboard.add_hotkey("g", typeCommands, args=[[
        selectAll, normalize, "enter", 
        labelSounds, "enter", nextLabel, 
        noiseReduction, "tab", "tab", "tab", "tab", "enter",
        selectAll, noiseReduction, 
        "enter", compressor, "enter", exportAudio
    ]])

# Script Hotkeys
keyboard.add_hotkey("a", importAndBackup)
keyboard.add_hotkey("s", typeCommands, args=[[selectAll, normalize, "enter"]])
keyboard.add_hotkey("d", typeCommands, args=[[trackStartToCursor, "backspace"]])
keyboard.add_hotkey("f", typeCommands, args=[[cursorToTrackEnd, "backspace"]])
keyboard.add_hotkey("h", storeBackup)

# This hotkey needs to do something different the first time,
# so it calls a function that replaces it
initialHotkey = keyboard.add_hotkey("g", newHotkey)

# Keep the script from closing for one hour so that hotkeys work
for i in range(0, 720):
    time.sleep(5)
    # Close Script when Audacity closes
    # Doesn't work in VSCode, but does work when script is started normally
    if Audacity.poll() == 0:
        storeBackup()
        os._exit(0)
        
storeBackup()