from pathlib import Path

# Setup:
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

# Pseudo:
#   Clean audio:
#       Ctrl+A (select all)
#       Ctrl+R (amplify)
#       Enter (confirm)
#       Ctrl+A (select all)
#       Ctrl+A (select all)
#       Ctrl+A (select all)