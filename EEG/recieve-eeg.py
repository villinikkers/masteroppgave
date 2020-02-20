"""Example program to show how to read a multi-channel time series from LSL.

Modified to save EEG-recordings from the OpenBCI cython board in a csv-file.

"""
from time import strftime, localtime
from pylsl import StreamInlet, resolve_stream

# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')

# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])

# save data to file:
start_time = strftime("%Y-%m-%d_%H-%M-%S", localtime())
filename = f"{start_time}.csv"
with open(filename, 'a', encoding ="utf-8") as f:
  print("collecting...")
  while True:
    # get a new sample (you can also omit the timestamp part if you're not
    # interested in it)
    # Timestamp are in seconds, with less than ms resolution
    sample, timestamp = inlet.pull_sample()
    sample = str(sample)
    # Write sample and timestamp to the logg-file.
    f.write(f"{sample[1:-1]}, {timestamp}\n")
