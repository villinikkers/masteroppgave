import serial
import time
from pylsl import StreamInfo, StreamOutlet

# create stream info:
# StreamInfo(name, type, channels, sampling rate (0=irregular), datatype, unique ID)
info = StreamInfo('AlarmMarkersTest', 'Markers', 1, 0, 'string', 'arduinoTroll')

# next make an outlet
outlet = StreamOutlet(info)

# To find out which port (COMx) the alarmbox is connected to run the windows
# 'Device manager'.
#
# The following code-block listens for input on the serial port, there are two types
# of events that send markers to the serial port:
#
#   1. Triggering of an alarm sends "alarm"
#   2. The toggle switch is flipped: sends the reaction time in ms as measured
#       by the arduino(e.g. 1400)
#
# The code tries to read data from the serial port continously.
# If it recieves a signal corresponding to a trigger-event, or reaction-event
# it pushes the corresponding marker through the LSL-outlet.

with serial.Serial('COM5', 9600, timeout=0.005) as ser:
  # Make sure iMotions starts to collect markers (press "play" on the sensor in
  # iMotions during the following startup sequence):
  print("Sending startup markers...")
  try:
    for i in range(4):
      outlet.push_sample(['starting'])
      time.sleep(5)
  except:
    print("ERROR: Start sequence failed.")

  # Normal operating mode
  print("running....")
  while True:
    line = ser.readline().decode('ascii')
    try:
        intLine = int(line)
        line += " ms"
        outlet.push_sample([line])
    except:
        if(line=='alarm'):
            outlet.push_sample([line])
    ser.reset_input_buffer()
