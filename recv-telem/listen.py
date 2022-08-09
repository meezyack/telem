#!/usr/bin/env python3

from pymavlink import mavutil
from time import sleep
import sys
# Start a connection listening on a UDP port
conn = mavutil.mavlink_connection(device='udp:localhost:14552',
source_system=1,source_component=158,autoreconnect=True,baud=115200)
print("Heartbeat from system (system %u component %u)" % 
(conn.source_system, conn.source_component))

# wait for the heartbeat msg to find the system ID
while True:
    if conn.wait_heartbeat(timeout=0.5) != None:
        # Got a heartbeat from remote MAVLink device, good to continue
        print("No heartbeat")
        break

    msg = conn.recv_match(type='STATUSTEXT',blocking=True)

    if msg.get_type() == "Bad Data":
        if mavutil.all_printable(msg.data):
            sys.stdout.write(msg.data)
            sys.stdout.flush()

    print(msg)