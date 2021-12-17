from pathlib import Path

# Off by default because this is use-case specific
useMetaData = False

# Audacity Hotkeys
amplifyKey = "alt+A"
compressorKey = "ctrl+J"
cursorToTrackEndKey = "shift+K"
exportAudioKey = "ctrl+shift+E"
importAudioKey = "ctrl+shift+I" # default
labelSoundsKey = "alt+L"
nextLabelKey = "alt+]"
noiseReductionKey = "alt+R"
normalizeKey = "alt+N"
removeTracksKey = "alt+T"
selectAllKey = "ctrl+A" # default
trackStartToCursorKey = "shift+L"

# Script Hotkeys
selectPreviousOptionKey = "ctrl+shift+A"
executeOptionKey = "ctrl+shift+S"
selectNextOptionKey = "ctrl+shift+D"

# Audio folders
source = Path.cwd() / "Source"
destination = Path.cwd() / "Destination"
backup = Path.cwd() / "Backup"

# Audacity executable path
AudacityPath = Path("C:/Program Files (x86)/Audacity/audacity.exe")