import keyboard
from pathlib import Path
import subprocess
import time

# Setup:
#   pip install keyboard
#   Change Audacity keyboard preferences:
#       Remove "repeat amplify" binding
#       Set "ampllify" to Ctrl+R

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
    time.sleep(0.05)
    keyboard.send("ctrl+a") # select all
    time.sleep(0.05)
    keyboard.send("ctrl+r") # amplify
    time.sleep(0.05)
    keyboard.send("enter") # confirm
    time.sleep(0.05)
#       Noise Reduction
#       Compressor

while True:
    keyboard.wait(";")
    cleanAudio()