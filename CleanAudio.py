import keyboard
import os
from pathlib import Path
import subprocess

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
Audacity = Path("C:/Program Files (x86)/Audacity/audacity.exe")

# Terminate script from anywhere
keyboard.add_hotkey("ctrl+c", lambda: os._exit(0))


def typeCommands(commandList):
    for command in commandList:
        keyboard.send(command)

def cleanAudio():
    typeCommands([
        selectAll, normalize, "enter", 
        labelSounds, "enter", nextLabel, 
        noiseReduction, "tab", "tab", "tab", "tab", "enter",
        selectAll, noiseReduction, 
        "enter", compressor, "enter"
    ])

def storeBackup():
    list1 = []
    list2 = []
    for file in source.iterdir():
        list1.append(file.name)
    for file in destination.iterdir():
        list2.append(file.name)
    set1 = set(list1)
    set2 = set(list2)
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

# Script Hotkeys
keyboard.add_hotkey("a", typeCommands, args=[[selectAll, removeTracks, importAudio]])
keyboard.add_hotkey("s", typeCommands, args=[[selectAll, normalize, "enter"]])
keyboard.add_hotkey("d", typeCommands, args=[[trackStartToCursor, "backspace"]])
keyboard.add_hotkey("f", typeCommands, args=[[cursorToTrackEnd, "backspace"]])

subprocess.Popen([Audacity])

keyboard.wait("g")

# Get a default noise profile so the
# noise reduction menu is the same
# for all subsequent noise reductions
keyboard.send(selectAll)
keyboard.send(noiseReduction)
keyboard.send("enter")

while True:
    cleanAudio()
    storeBackup()
    keyboard.wait("g")