"""Created by Christian - January 2020

Script for sending EEG-data over lab streaming layer.

"""
from sys import argv
from pyOpenBCI import OpenBCICyton
from pylsl import StreamInfo, StreamOutlet
import numpy as np

# Check if port is given:
if len(argv)<2:
  # Script does not run
  print("Port not given as input argument. Run the script with:\n\n\t>>python openBCI-LSL-EEG.py COMX\n\n\
replace 'X' with the port where the USB-dongle is plugged in.\n\n\n")
else:
  # Run script

  # Scaling factor for conversion between raw data (counts) and voltage potentials:
  SCALE_FACTOR_EEG = (4500000)/24/(2**23-1) #uV/count

  # Defining stream info:
  name = 'OpenBCIEEG'
  ID = 'OpenBCItestEEG'
  port = argv[1]
  channels = 8
  sample_rate = 250
  datatype = 'float32'
  streamType = 'EEG'

  print(f"Creating LSL stream for EEG. \nName: {name}\nID: {ID}\n")

  info_eeg = StreamInfo(name, streamType, channels, sample_rate, datatype, ID)
  outlet_eeg = StreamOutlet(info_eeg)

  def lsl_streamer(sample):
      """
      Convert the sample data from it's raw format (counts) to uV and push it
      to the LSL-stream.
      """
    outlet_eeg.push_sample(np.array(sample.channels_data)*SCALE_FACTOR_EEG)


  # Start the stream:
  board = OpenBCICyton(port=port, daisy=False)
  board.start_stream(lsl_streamer)
