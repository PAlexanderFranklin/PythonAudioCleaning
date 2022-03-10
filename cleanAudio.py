import keyboard
import os
from pathlib import Path
from shutil import move
import subprocess
import time
from win32gui import GetForegroundWindow, GetWindowText, GetClassName

from config import *
import populateMetaData

Audacity = subprocess.Popen(AudacityPath)

# When opened, Audacity has a different menu structure than after a noise profile is obtained.
noNoiseProfile = False

# Store Audacity Window for checking when effects are finished processing
while True:
    time.sleep(0.25)
    theWindow = GetForegroundWindow()
    if GetClassName(theWindow) == "wxWindowNR":
        if GetWindowText(theWindow) != "Audacity is starting up...":
            break
        else:
            noNoiseProfile = True
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
        keyboard.send(command)
        time.sleep(0.25)
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
            move(file, backup / file.name)
        except:
            print(file.name + " failed to copy")
    
def importAndBackup():
    storeBackup()
    typeCommands([selectAllKey, removeTracksKey, importAudioKey])

def normalizeAudio():
    typeCommands([selectAllKey, normalizeKey, "enter"])

def amplifyAudio():
    typeCommands([selectAllKey, limiterKey, "enter"])

def compressAudio():
    typeCommands([selectAllKey, compressorKey, "enter"])

def deleteBeginning():
    typeCommands([trackStartToCursorKey, "backspace"])

def deleteEnd():
    typeCommands([cursorToTrackEndKey, "backspace"])

def labelSounds():
    for i in range (-28, -18):
        typeCommands([selectAllKey, labelSoundsKey])
        time.sleep(0.2)
        keyboard.write(str(i))
        keyboard.send("enter")
        time.sleep(0.2)
        for j in range (0, 10):
            LSWindow = GetForegroundWindow()
            time.sleep(1)
            newLSWindow = GetForegroundWindow()
            if newLSWindow == mainAudacityWindow:
                return
            if newLSWindow != LSWindow:
                break
        keyboard.send("enter")
        time.sleep(0.2)

def reduceNoise():
    labelSounds()

    typeCommands([
        nextLabelKey, 
        noiseReductionKey,
    ])
    
    global noNoiseProfile
    if noNoiseProfile:
        noNoiseProfile = False
    else:
        typeCommands(["tab", "tab", "tab", "tab",])

    typeCommands([
        "enter",
        selectAllKey, noiseReductionKey, "enter",
    ])

def exportAudio():
    typeCommands([exportAudioKey])
    if useMetaData:
        populateMetaData.addDBEntry(GetWindowText(mainAudacityWindow))

macroOptions = [importAndBackup,
                normalizeAudio,
                deleteBeginning,
                deleteEnd,
                reduceNoise,
                amplifyAudio,
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
    print("Selected: " + macroOptions[optionCursor].__name__)

def selectNextOption():
    global optionCursor
    if optionCursor == len(macroOptions) - 1:
        optionCursor = 0
    else:
        optionCursor += 1
    print("Selected: " + macroOptions[optionCursor].__name__)

def executeOption():
    global optionCursor
    print("Let go of Control and Shift to run command.")
    macroOptions[optionCursor]()
    print("Finished execution.")
    if optionCursor == len(macroOptions) - 1:
        optionCursor = 0
    else:
        optionCursor += 1
    print("Selected: " + macroOptions[optionCursor].__name__)

print("Press " + executeOptionKey + " to run the selected command. Press " +
    selectPreviousOptionKey + " or " + selectNextOptionKey +
    " to select a different command.")
print("Selected: " + macroOptions[optionCursor].__name__)

# Script Hotkeys
keyboard.add_hotkey(selectPreviousOptionKey, selectPreviousOption)
keyboard.add_hotkey(selectNextOptionKey, selectNextOption)
keyboard.add_hotkey(executeOptionKey, executeOption)

# Keep the script from closing so that hotkeys work
while (True):
    time.sleep(5)
    # Terminate Script when Audacity closes
    if GetWindowText(mainAudacityWindow) == "":
        storeBackup()
        os._exit(0)