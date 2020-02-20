import serial
import time
from pylsl import StreamInfo, StreamOutlet

# create stream info:
# StreamInfo(name, type, channels, sampling rate (0=irregular), datatype, unique ID)
info = StreamInfo('AlarmMarkersTest', 'Markers', 1, 0, 'string', 'arduinoTroll')

# next make an outlet
outlet = StreamOutlet(info)

print("running....")

# To find out which port (COMx) the alarmbox is connected to run the windows
# 'Device manager'.
# This code-block listenes.
with serial.Serial('COM5', 9600, timeout=0.005) as ser:
    while True:
        line = ser.readline().decode('ascii')
        try:
            intLine = int(line)
            outlet.push_sample([line])
        except:
            if(line=='alarm'):
                outlet.push_sample([line])
        ser.reset_input_buffer()
