# FTServo_Python_Websockets

FEETECH BUS Servo Python library fork with support for Websockets

This is a fork of the [official feetech repository](https://github.com/ftservo/FTServo_Python) that adds websocket support.

## Structure

```
root directory
     |---scservo_sdk
     |---sms_sts
     |---scscl
```

The 'scscl' 'sms_sts' directories contain examples of using the library.

The source code of the library is located in the `scservo_sdk` directory.

## Websocket Support

This fork adds support for using a websocket client as a port in place of a serial port. This makes it possible to use WiFi to control your FEETECH servos. It requires the servos to be connected over half-duplex serial to a WiFi-enabled control board (such as an ESP32) that uses a websocket server to relay the comms to and from connected motors. I am developing such a board and will link to it here when it is available. This library has been tested with the HLS3930 servos.

The Arduino sketch that works as the websocket server is available here:\
https://github.com/nsted/websocketServerForSmartServos

## Installation

### Method 1. Install via pip

```bash
pip install ftservo-python-websockets
```

### Method 2. Clone repository

```bash
$ cd /usr/src/
$ sudo git clone https://github.com/nsted/ftservo-python-websockets.git
$ sudo chown -R pi ftservo-python-websockets
$ cd ftservo-python-websockets/sms_sts
$ python3 ping.py
```

## Usage

Tested on macOS 24.3.0.
Python version 3.12.1

### Basic Usage

To use websocket define your port as:\
&nbsp; &nbsp; &nbsp; &nbsp; `portHandler = PortHandler("ws://yourServerURL:portnum")`\
e.g.:\
&nbsp; &nbsp; &nbsp; &nbsp; `portHandler = PortHandler("ws://192.168.1.22:80")`

Send binary with:\
&nbsp; &nbsp; &nbsp; &nbsp; `portHandler.writePort([byte1,byte2,...,byteN])`

This feature is used by the FTServo SDK with calls such as:\
&nbsp; &nbsp; &nbsp; &nbsp; `packetHandler.write1ByteTxRx(portHandler, id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)`

You can also send text with:\
&nbsp; &nbsp; &nbsp; &nbsp; `portHandler.writePort("my message here")`\
This is useful if you want to handle other commands on the server such as requests for sensor data.

### Example

```python
Succeeded to open the port
Succeeded to change the baudrate
[ID:001] ping Succeeded. SCServo model number : 1540
```
