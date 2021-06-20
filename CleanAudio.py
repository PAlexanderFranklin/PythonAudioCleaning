import keyboard
from pathlib import Path
import subprocess
import time

# Setup
#   pip install keyboard
#   Change Audacity keyboard preferences:
#       Remove "repeat amplify" binding
#       Set "Ampllify" and other settings to the keys in the "Hotkeys" section below
#   Set effect defaults in Audacity:
#       "Label Sounds"
#           Regions between sounds 
#           Threshold level:          (-22.0 db seems to work)
#           Minimum silence duration: 2 seconds
#           Label type:               Region between sounds


# Hotkeys
amplify = "ctrl+R"
labelSounds = "alt+L"
selectAll = "ctrl+A"
nextLabel = "alt+]"
noiseReduction = "alt+R"

# Audacity executable path
Audacity = Path("C:/Program Files (x86)/Audacity/audacity.exe")

# Configure source and destination
source = Path.cwd() / "Source"
destination = Path.cwd() / "Destination"


# Start of Script
print("source: ", source)
print("destination: ", destination)

subprocess.Popen([Audacity])

for file in source.iterdir():
    if file.name[-3:] == "wav":
        print(file.name)

def cleanAudio():
    commandList = [
        selectAll, amplify, "enter", 
        labelSounds, "enter", nextLabel, 
        noiseReduction, "enter", selectAll, noiseReduction, 
        "enter"
    ]
    for command in commandList:
        time.sleep(1)
        keyboard.send(command)
#   Compressor

while True:
    keyboard.wait(";")
    cleanAudio()