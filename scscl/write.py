#!/usr/bin/env python
#
# *********     Gen Write Example      *********
#
#
# Available SCServo model on this example : All models using Protocol SCS
# This example is tested with a SCServo(SCS), and an URT
#

import sys
import time
import os

# Get the absolute path to the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# sys.path.append("..")
from scservo_sdk import *                      # Uses FTServo SDK library


# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
# portHandler = PortHandler('/dev/cu.usbmodem1201')# ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"
portHandler = PortHandler('ws://192.168.2.61:8080')


# Initialize PacketHandler instance
# Get methods and members of Protocol
packetHandler = scscl(portHandler)
    
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

try:
    while 1:
        # Servo (ID1) runs at a maximum speed of V=1500*0.059=88.5rpm until it reaches position P1=1000
        scs_comm_result, scs_error = packetHandler.WritePos(1, 1000, 0, 1500)
        if scs_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(scs_comm_result))
        if scs_error != 0:
            print("%s" % packetHandler.getRxPacketError(scs_error))

        time.sleep(((1000-20)/(1500) + 0.05))#[(P1-P0)/(V)] + 0.1

        # Servo (ID1) runs at a maximum speed of V=1500*0.059=88.5rpm until it reaches position P0=20
        scs_comm_result, scs_error = packetHandler.WritePos(1, 20, 0, 1500)
        if scs_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(scs_comm_result))
        if scs_error != 0:
            print("%s" % packetHandler.getRxPacketError(scs_error))

        time.sleep(((1000-20)/(1500) + 0.05))#[(P1-P0)/(V)] + 0.1
        
except KeyboardInterrupt:
    print("\nKeyboardInterrupt received. Stopping servo and closing port...")
finally:
    # Stop the servo immediately by disabling torque
    scs_comm_result, scs_error = packetHandler.write1ByteTxRx(1, SCSCL_TORQUE_ENABLE, 0)
    if scs_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(scs_comm_result))
    if scs_error != 0:
        print("%s" % packetHandler.getRxPacketError(scs_error))
    # Close port
    portHandler.closePort()
