import keyboard
import os
from pathlib import Path
import subprocess
import time

# Setup
#   pip install keyboard
#   Change Audacity keyboard preferences:
#       Set "Normalize" and other settings to the keys in the "Hotkeys" section below
#   Set effect defaults in Audacity:
#       "Label Sounds"
#           Regions between sounds 
#           Threshold level:          (-22.0 db seems to work)
#           Minimum silence duration: 2 seconds
#           Label type:               Region between sounds
#       "Compressor"
#           Set attack and release times to their minimum value

# Hotkeys
normalize = "alt+N"
labelSounds = "alt+L"
selectAll = "ctrl+A" # default
nextLabel = "alt+]"
noiseReduction = "alt+R"
cursorShortJumpRight = "." # default
trackStartToCursor = "ctrl+J"

# Audacity executable path
Audacity = Path("C:/Program Files (x86)/Audacity/audacity.exe")

# Configure source and destination
source = Path.cwd() / "Source"
destination = Path.cwd() / "Destination"

# Terminate script from anywhere
keyboard.add_hotkey("ctrl+c", lambda: os._exit(0))


# Start of Script
print("source: ", source)
print("destination: ", destination)

# subprocess.Popen([Audacity])

# for file in source.iterdir():
#     if file.name[-3:] == "wav":
#         print(file.name)

def cleanAudio():
    commandList = [
        selectAll, normalize, "enter", 
        labelSounds, "enter", nextLabel, 
        noiseReduction, "tab", "tab", "tab", "tab", "enter",
        selectAll, noiseReduction, 
        "enter"
    ]
    for command in commandList:
        time.sleep(1)
        keyboard.send(command)

while True:
    # Macro start button
    keyboard.wait(";")

    # Get a default noise profile so the
    # noise reduction menu is the same
    # for all subsequent noise reductions
    keyboard.send(selectAll)
    time.sleep(1)
    keyboard.send(noiseReduction)
    time.sleep(1)
    keyboard.send("enter")

    cleanAudio()