from pathlib import Path


# Configure source and destination
source = Path.cwd() / "Source"
destination = Path.cwd() / "Destination"

print("source: ", source)
print("destination: ", destination)


for file in source.iterdir():
    if file.name[-3:] == "wav":
        print(file.name)