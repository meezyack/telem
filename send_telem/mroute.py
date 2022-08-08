
#!/usr/bin/env python3
#The script does the following.
import time
import serial
import datetime
from os.path import exists
from pymavlink import mavutil

########Naming and creating file for Sensor Log################
dt =  str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
filename = 'SENSOR_SAMPLE' + dt +'.txt'
f = open('/home/pi/logs/'+filename , 'w')

#Set Up Serial Port for the sensor
#Ensure you are using the correct header name in '/dev' which the component is plugged in to. If the ETHUSB Hub Hat is attached, the ttyUSB number sometimes changes between zero and one.
ser = serial.Serial(
        '/dev/ttyUSB0',
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

# Setup MAVLink to connect on udp 127.0.0.1:14550
conn = mavutil.mavlink_connection("udp:127.0.0.1:14550", autoreconnect=True, source_system=1, force_connected=False, source_component=mavutil.mavlink.MAV_COMP_ID_PERIPHERAL)

# wait for the heartbeat msg to find the system ID
while True:
    if conn.wait_heartbeat(timeout=0.5) != None:
        # Got a heartbeat from remote MAVLink device, good to continue
        break

#The program will continue to write into the file until it is terminated.
while 1:
    # convert from bytes to string then strip any whitespace
    data = ser.read(100).decode("utf-8").strip()
    if data != '':
        #debugs printer
        #print(data)
        #writes to MAVLink as a STATUSTEXT message, encoded as ASCII
        conn.mav.statustext_send(mavutil.mavlink.MAV_SEVERITY_INFO, data.encode())


