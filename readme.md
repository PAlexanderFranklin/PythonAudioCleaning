This script is written for Audacity 3.0.0, and is probably broken for other versions due to menu structure changes.
### Setup
Install the Python modules "keyboard" and "pywin32" using "pip install keyboard, pywin32". Change Audacity keyboard shortcuts and/or the constants in config.py to make them match. Run functions once without the script to set their options for the script. Of particular note are the options "minimum silence duration" and "label type" in the "Label Sounds" analysis tool, as well as Compressor settings.