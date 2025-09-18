import time
import sys
import websocket
import logging
# from .port_handler import PortHandler

# Configure logging - disabled by default
logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)  # Only show critical errors by default

LATENCY_TIMER = 16
# default to native baudrate to prevent errors at init
DEFAULT_BAUDRATE = 115200

class WebSocketHandler(object):
    def __init__(self, websocket_url):
        self.is_open = False
        self.baudrate = DEFAULT_BAUDRATE
        self.packet_start_time = 0.0
        self.packet_timeout = 0.0
        self.tx_time_per_byte = 0.0

        self.is_using = False
        self.websocket_url = websocket_url
        self.websocket = None
        self.buffer = b""  # Buffer to store excess data from previous reads
    
    @classmethod
    def enable_debug_logging(cls, level=logging.DEBUG):
        """Enable debug logging for WebSocket operations"""
        logger.setLevel(level)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
    
    @classmethod
    def disable_logging(cls):
        """Disable all logging except critical errors"""
        logger.setLevel(logging.CRITICAL)

    def openPort(self):
        # Opens a connection to the WebSocket server
        return self.setBaudRate(self.baudrate)

    def closePort(self):
        # Closes the WebSocket connection
        if self.websocket:
            try:
                self.websocket.close()
            except Exception as e:
                logger.error(f"Error closing WebSocket: {e}")
            finally:
                self.websocket = None
                self.is_open = False
                self.buffer = b""

    def clearPort(self):
        # Clear any buffer or state, WebSockets don't use buffers in the same way as serial
        pass

    def setPortName(self, websocket_url):
        # If URL changes and port is open, reconnect
        if self.websocket_url != websocket_url and self.is_open:
            self.closePort()
        
        self.websocket_url = websocket_url
        if self.is_open:
            self.openPort()

    def getPortName(self):
        return self.websocket_url

    def setBaudRate(self, baudrate):
        baud = self.getCFlagBaud(baudrate)
        if baud <= 0:
            return False
        else:
            self.baudrate = baudrate
            return self.setupPort()

    def getBaudRate(self):
        return self.baudrate

    def getBytesAvailable(self):
        # Return the number of bytes available in the buffer
        return len(self.buffer)

    def readPort(self, length):
        try:
            # Check if buffer has enough data to fulfill the request
            if len(self.buffer) >= length:
                data, self.buffer = self.buffer[:length], self.buffer[length:]
                return data

            # If buffer doesn't have enough data, attempt to receive more from WebSocket
            if self.websocket and self.websocket.sock:
                try:
                    received_data = self.websocket.recv()
                    self.buffer += received_data

                    if len(self.buffer) >= length:
                        data, self.buffer = self.buffer[:length], self.buffer[length:]
                        return data
                    else:
                        # Not enough data even after recv, return what we have
                        data, self.buffer = self.buffer, b""
                        return data
                except websocket.WebSocketConnectionClosedException:
                    logger.warning("WebSocket connection closed")
                    self.is_open = False
                    return b""  # Return empty bytes instead of None
                except websocket.WebSocketTimeoutException:
                    logger.debug("WebSocket receive timeout")
                    return b""  # Return empty bytes instead of None
                except Exception as e:
                    logger.error(f"WebSocket receive error: {e}")
                    return b""  # Return empty bytes instead of None
            return b""  # Return empty bytes instead of None
        except Exception as e:
            logger.error(f"Read error: {e}")
            return b""  # Return empty bytes instead of None

    def writePort(self, packet):
        try:
            # Check if WebSocket is connected using the 'sock' attribute
            if not self.websocket or not self.websocket.sock:
                logger.error("Write error: WebSocket is not connected.")
                return 0

            # Convert list to bytes if packet is a list of integers
            if isinstance(packet, list):
                # Convert the list of integers to a bytearray (assuming each list element is an integer)
                packet = bytearray(packet)
                # print(f"Converted list to bytearray: {packet}")

            # Send the packet depending on its type
            if isinstance(packet, (bytes, bytearray)):
                self.websocket.send_binary(packet)  # Send binary data using send_binary
            elif isinstance(packet, str):
                self.websocket.send(packet)  # Send as text
            else:
                logger.error(f"Write error: Invalid packet type {type(packet)}")
                return 0

            # print(f"Packet sent: {packet}")
            return len(packet)
        except Exception as e:
            logger.error(f"Write error: {e}")
            return 0
    
    def setPacketTimeout(self, packet_length):
        self.packet_start_time = self.getCurrentTime()
        self.packet_timeout = (self.tx_time_per_byte * packet_length) + (LATENCY_TIMER * 2.0) + 2.0

    def setPacketTimeoutMillis(self, msec):
        self.packet_start_time = self.getCurrentTime()
        self.packet_timeout = msec

    def isPacketTimeout(self):
        if self.getTimeSinceStart() > self.packet_timeout:
            self.packet_timeout = 0
            return True
        return False

    def getCurrentTime(self):
        return round(time.time() * 1000000000) / 1000000.0

    def getTimeSinceStart(self):
        time_since = self.getCurrentTime() - self.packet_start_time
        if time_since < 0.0:
            self.packet_start_time = self.getCurrentTime()
        return time_since

    def setupPort(self, max_retries=3, retry_delay=2):
        if self.is_open:
            self.closePort()

        for attempt in range(max_retries):
            try:
                logger.info(f"Attempting to connect to WebSocket: {self.websocket_url} (attempt {attempt + 1}/{max_retries})")
                
                # Add connection timeout and other websocket options
                self.websocket = websocket.create_connection(
                    self.websocket_url,
                    timeout=10,  # Increased to 10 second timeout
                    enable_multithread=True,
                    skip_utf8_validation=True  # Performance optimization for binary data
                )
                self.is_open = True
                self.tx_time_per_byte = (1000.0 / self.baudrate) * 10.0
                logger.info("WebSocket connection established successfully")
                return True
                
            except websocket.WebSocketTimeoutException:
                logger.warning(f"Connection timeout (attempt {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    logger.error("All connection attempts failed due to timeout")
                    self.is_open = False
                    return False
                    
            except websocket.WebSocketAddressException as e:
                logger.error(f"WebSocket address error: {e}")
                logger.error("Please check if the WebSocket server is running and the URL is correct")
                self.is_open = False
                return False
                
            except Exception as e:
                logger.error(f"Failed to connect to WebSocket (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    logger.error("All connection attempts failed")
                    self.is_open = False
                    return False
        
        return False

    def getCFlagBaud(self, baudrate):
        # Keep baudrate method for compatibility, though not needed in WebSockets
        if baudrate in [
            9600, 19200, 38400, 57600, 115200, 230400, 460800, 500000, 
            576000, 921600, 1000000, 1152000, 2000000, 2500000, 3000000, 
            3500000, 4000000
        ]:
            return baudrate
        else:
            return -1
        
    # use for debugging packets...don't use by default
    def hexdump(self, src, length):
        logger.debug(f"[HEXDUMP] {len(src)} bytes:")
        logger.debug(f"bytes expected: {length}, received: {len(src)}")
        for i in range(len(src)):
            logger.debug(hex(src[i]), extra={"end": " "})
        logger.debug("")
    
