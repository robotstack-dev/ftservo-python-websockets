# ftservo-python-websockets

This is a fork of the [official feetech repository](https://github.com/ftservo/FTServo_Python) that adds WebSocket support, enabling wireless control of FEETECH servos.

## WebSocket Support

This fork adds support for using a WebSocket client as a port in place of a serial port. This makes it possible to wirelessly control your robot!

It requires the servos to be connected over half-duplex serial to a WiFi-enabled microcontroller (e.g. ESP32) that uses a WebSocket server to relay the comms to and from connected motors. The **[RobotStack Smart Servo Add-On Board](https://www.tindie.com/products/robotstack/smart-servo-addon-board/)** is a ready-to-use solution that provides this functionality.

## Structure

```
root directory
     |---scservo_sdk
     |---sms_sts
     |---scscl
     |---additional-examples
```

The source code of the library is located in the `scservo_sdk` directory.

The 'scscl' and 'sms_sts' directories contain examples of using the library.

The `additional-examples` directory contains examples demonstrating additional features:

- `send_text.py`: Shows how to send text messages to the server
- `ping_and_poll.py`: Demonstrates how to ping a servo and poll for incoming messages

## Usage

Tested with:

- macOS 24.3.0.
- Python version 3.12.1
- Seeed Xiao ESP32-S3 Microcontroller
- [smart-servo-addon-board](https://github.com/robotstack-dev/smart-servo-addon-board)
- [smart-servo-bridge firmware](https://github.com/robotstack-dev/smart-servo-bridge)
- Feetech HLS3930 smart servos

### Method 1. Clone repository

```bash
$ cd /usr/src/
$ sudo git clone https://github.com/robotstack-dev/ftservo-python-websockets.git
$ sudo chown -R pi ftservo-python-websockets
$ cd ftservo-python-websockets/sms_sts
$ python3 ping.py
Succeeded to open the port
Succeeded to change the baudrate
[ID:001] ping Succeeded. SCServo model number : 1540
```

### Method 2. Install via pip

```bash
Copy the sample file to any location convenient for you. In the example I use '/home/pi/FeetechTestFiles'

$ pip install ftservo-python-websockets
$ cd /home/pi/FeetechTestFiles/sms_sts
$ python3 ping.py
Succeeded to open the port
Succeeded to change the baudrate
[ID:001] ping Succeeded. SCServo model number : 1540
```

### Basic Usage

To use WebSocket define your port as:\
&nbsp; &nbsp; &nbsp; &nbsp; `portHandler = PortHandler("ws://yourServerURL:portnum")`\
e.g.:\
&nbsp; &nbsp; &nbsp; &nbsp; `portHandler = PortHandler("ws://192.168.1.22:80")`

You'll need to find the IP address of the server. If using the smart-servo-bridge firmware, you can print its IP address to the serial monitor when it starts up.

Send binary with:\
&nbsp; &nbsp; &nbsp; &nbsp; `portHandler.writePort([byte1,byte2,...,byteN])`

This feature is used by the FTServo SDK with calls such as:\
&nbsp; &nbsp; &nbsp; &nbsp; `packetHandler.write1ByteTxRx(portHandler, id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)`

You can also send text with:\
&nbsp; &nbsp; &nbsp; &nbsp; `portHandler.writePort("my message here")`
