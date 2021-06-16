from pathlib import Path
import keyboard
import time

# Setup:
#   pip install keyboard
#   Change Audacity keyboard preferences:
#       Remove "repeat amplify" binding
#       Set "ampllify" to Ctrl+R


# Configure source and destination
source = Path.cwd() / "Source"
destination = Path.cwd() / "Destination"

print("source: ", source)
print("destination: ", destination)


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