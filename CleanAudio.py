from pathlib import Path, PosixPath, PurePosixPath
from pyo import *


# Configure source and destination
source = Path.cwd() / "Source"
destination = Path.cwd() / "Destination"

audioServer = Server(audio="offline")

print("source: ", source)
print("destination: ", destination)


for file in source.iterdir():
    if file.name[-3:] == "wav":
        print(file.name)
        
        # Retrieve info about the sound from its header.
        info = sndinfo(file.__str__())
        dur, sr, chnls = info[1], info[2], info[3]
        fformat = ["WAVE", "AIFF", "AU", "RAW", "SD2", "FLAC", "CAF", "OGG"].index(info[4])
        samptype = [
            "16 bit int",
            "24 bit int",
            "32 bit int",
            "32 bit float",
            "64 bits float",
            "U-Law encoded",
            "A-Law encoded",
        ].index(info[5])

        # Set server parameters according to the current sound info.
        audioServer.setSamplingRate(sr)
        audioServer.setNchnls(chnls)
        audioServer.boot()
        audioServer.recordOptions(
            dur=dur,
            filename=(destination / file.name).__str__(),
            fileformat=fformat,
            sampletype=samptype,
        )

        # Simple processing applied to the sound.
        source = SfPlayer(file.__str__())
        bandpass = ButBP(source, 1000, 5)
        disto = Disto(bandpass, drive=0.9, slope=0.8)
        output = WGVerb(source + disto, feedback=0.8, cutoff=5000, bal=0.25, mul=0.5).out()

        # Start the rendering.
        audioServer.start()

        # Cleanup for the next pass.
        audioServer.shutdown()