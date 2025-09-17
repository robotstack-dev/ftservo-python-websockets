#!/usr/bin/env python
#
# *********     Ping Example      *********
#
#
# Available SCServo model on this example : All models using Protocol SCS
# This example is tested with a SCServo(STS/SMS), and an URT
#

import sys
import os

# Get the absolute path to the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# sys.path.append("..")
from scservo_sdk import *                   # Uses FTServo SDK library

# Use the actual port assigned to the smart servo controller.
# ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
# DEVICENAME                  = '/dev/cu.usbmodem11201'
# DEVICENAME                  = '/dev/cu.usbserial-1120'
DEVICENAME                  = 'ws://192.168.2.68:8080'
SERVO_ID                  = 2

# Initialize PortHandler instance
portHandler = PortHandler(DEVICENAME) 

# Initialize PacketHandler instance
# Get methods and members of Protocol
packetHandler = sms_sts(portHandler)
# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    quit()

# Set port baudrate 1000000
if portHandler.setBaudRate(1000000):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    quit()

# Try to ping the ID:1 FTServo
# Get SCServo model number
scs_model_number, scs_comm_result, scs_error = packetHandler.ping(SERVO_ID)
if scs_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(scs_comm_result))
else:
    print("[ID:%03d] ping Succeeded. SCServo model number : %d" % (SERVO_ID, scs_model_number))
if scs_error != 0:
    print("%s" % packetHandler.getRxPacketError(scs_error))

# Close port
portHandler.closePort()
