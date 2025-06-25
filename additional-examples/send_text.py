#!/usr/bin/env python

import sys
import os
import tty
import termios
import time

# Add the parent directory to the Python path so we can import the scservo_sdk
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scservo_sdk import *  # Uses SCServo SDK library

# Default setting
BAUDRATE = 1000000  # Default baudrate of SCServo
# DEVICENAME = '/dev/cu.usbmodem1201'
DEVICENAME = 'ws://192.168.2.61:8080'

POLL_SECONDS = 5  # How long to poll for a response after sending
POLL_INTERVAL = 0.1  # Polling interval in seconds

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def send_text_message(portHandler, message):
    # Try to get the port name or websocket url
    port_name = getattr(portHandler, 'port_name', None) or getattr(portHandler, 'websocket_url', None)
    if port_name and (port_name.startswith('ws://') or port_name.startswith('wss://')):
        # WebSocket: send as text
        print(f"Sending text message over WebSocket: {message}")
        portHandler.writePort(message)
    else:
        # Serial: send as bytes
        print(f"Sending text message over Serial (as bytes): {message}")
        portHandler.writePort(message.encode('utf-8'))

def poll_for_response(portHandler, seconds=POLL_SECONDS, interval=POLL_INTERVAL):
    print(f"Polling for response for {seconds} seconds...")
    end_time = time.time() + seconds
    found = False
    while time.time() < end_time:
        if portHandler.getBytesAvailable() > 0:
            data = portHandler.readPort(portHandler.getBytesAvailable())
            if data:
                print(f"Received response: {data}")
                found = True
        time.sleep(interval)
    if not found:
        print("No response received.")

def main():
    # Initialize PortHandler instance
    # Set the port path
    # Get methods and members of PortHandlerLinux or PortHandlerWindows
    portHandler = PortHandler(DEVICENAME)

    # Initialize PacketHandler instance
    packetHandler = protocol_packet_handler(portHandler, 1)

    # Open port
    if portHandler.openPort():
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        print("Press any key to terminate...")
        getch()
        quit()

    # Set port baudrate
    if portHandler.setBaudRate(BAUDRATE):
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        print("Press any key to terminate...")
        getch()
        quit()

    # Try to send a text message
    try:
        message = "ping"
        send_text_message(portHandler, message)
        print("Message sent successfully!")
        poll_for_response(portHandler)
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Close port
        portHandler.closePort()
        print("Port closed")

if __name__ == '__main__':
    main() 