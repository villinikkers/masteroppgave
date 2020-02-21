import serial
import time
from pylsl import StreamInfo, StreamOutlet
from sys import argv

# Check if port number was given, if not: try with open the default port:
if len(argv)<2:
  port = "COM4"
  print(f"""=======WARNING=======
Pass the port number as an input argument when running the script. E.g.:
  >python send_serial_read_LSL.py COM4
=====================
Trying with the default port {port}...""")

  port = "COM4"
else:
  port = argv[1]
  print(f"Opening port {port}.")

# create stream info:
# StreamInfo(name, type, channels, sampling rate (0=irregular), datatype, unique ID)
info = StreamInfo('AlarmMarkersTest', 'Markers', 1, 0, 'string', 'arduinoTroll')

# next make an outlet
outlet = StreamOutlet(info)

# To find out which port (COMx) the alarmbox is connected to run the windows
# 'Device manager'.
#
# This code-block listenes for input on the serial port, there are two types
# of events that send markers to the serial port:
#
#   1. Triggering of an alarm sends "alarm"
#   2. The toggle switch is flipped: sends the reaction time in ms (e.g. 1400)
#
# The code tries to read data from the serial port continously.
# If it recieves a signal corresponding to a trigger-event or reaction-event
# it pushes the corresponding marker through the LSL-outlet.

try:
    with serial.Serial(port, 9600, timeout=0.005) as ser:
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
except serial.serialutil.SerialException:
    print(f"""Could not open port {port}, make sure you have entered correct port number and try again.""")
finally:
    print("Program aborted.")
