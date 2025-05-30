#!/usr/bin/env python

from .scservo_def import *
from .protocol_packet_handler import *
from .group_sync_read import *
from .group_sync_write import *

# Baud Rate Definitions
HLSS_1M = 0
HLSS_0_5M = 1
HLSS_250K = 2
HLSS_128K = 3
HLSS_115200 = 4
HLSS_76800 = 5
HLSS_57600 = 6
HLSS_38400 = 7

# Memory Table Definitions
#-------EPROM (Read Only)--------
HLSS_MODEL_L = 3
HLSS_MODEL_H = 4

#-------EPROM (Read/Write)--------
HLSS_ID = 5
HLSS_BAUD_RATE = 6
HLSS_MIN_ANGLE_LIMIT_L = 9
HLSS_MIN_ANGLE_LIMIT_H = 10
HLSS_MAX_ANGLE_LIMIT_L = 11
HLSS_MAX_ANGLE_LIMIT_H = 12
HLSS_CW_DEAD = 26
HLSS_CCW_DEAD = 27
HLSS_OFS_L = 31
HLSS_OFS_H = 32
HLSS_OPERATION_MODE = 33


#-------SRAM (Read/Write)--------
HLSS_TORQUE_SWITCH = 40        # 0x28: Torque switch (0: off, 1: on, 2: brake)
HLSS_ACCELERATION = 41         # 0x29: Acceleration (1.46 RPM/s units)
HLSS_TARGET_POSITION_L = 42    # 0x2A: Target position low byte (0.087° units)
HLSS_TARGET_POSITION_H = 43    # 0x2B: Target position high byte
HLSS_TARGET_TORQUE_L = 44      # 0x2C: Target torque low byte (6.5mA units in Mode 0)
HLSS_TARGET_TORQUE_H = 45      # 0x2D: Target torque high byte
HLSS_RUNNING_SPEED_L = 46      # 0x2E: Running speed low byte (0.732 RPM units)
HLSS_RUNNING_SPEED_H = 47      # 0x2F: Running speed high byte
HLSS_LOCK = 55                # 0x37: EPROM lock (0: unlocked, 1: locked)

#-------SRAM (Read Only)--------
HLSS_PRESENT_POSITION_L = 56    # Present position low byte (0.087° units)
HLSS_PRESENT_POSITION_H = 57    # Present position high byte
HLSS_PRESENT_SPEED_L = 58       # Present speed low byte (0.732 RPM units)
HLSS_PRESENT_SPEED_H = 59       # Present speed high byte
HLSS_PRESENT_VOLTAGE = 62       # Present voltage (0.1V units)
HLSS_PRESENT_TEMPERATURE = 63   # Present temperature (°C)
HLSS_MOVEMENT_STATE = 66        # Movement state (bit0: moving, bit1: target reached)
HLSS_SERVO_STATUS = 65          # Servo status (errors and warnings)
HLSS_PRESENT_CURRENT_L = 69     # Present current low byte (6.5mA units)
HLSS_PRESENT_CURRENT_H = 70     # Present current high byte

# Additional Memory Table Definitions from Magnetic Encoder HTS-Table
HLSS_FIRMWARE_MAJOR = 0  # Firmware major version number
HLSS_FIRMWARE_MINOR = 1  # Firmware sub version number 
HLSS_END = 2  # END
HLSS_SECONDARY_ID = 7  # Secondary ID
HLSS_RESPONSE_STATUS_LEVEL = 8  # Response status level
HLSS_MAX_TEMPERATURE_LIMIT = 13  # Maximum Temperature Limit
HLSS_MAX_INPUT_VOLTAGE = 14  # Maximum input voltage
HLSS_MIN_INPUT_VOLTAGE = 15  # Minimum input voltage
HLSS_MAX_TORQUE_L = 16  # Maximum torque low byte
HLSS_MAX_TORQUE_H = 17  # Maximum torque high byte
HLSS_PHASE = 18  # Phase
HLSS_UNLOADING_CONDITION = 19  # Unloading condition
HLSS_LED_ALARM_CONDITION = 20  # LED Alarm condition
HLSS_POSITION_LOOP_KP = 21  # Position loop P proportional coefficient
HLSS_POSITION_LOOP_KD = 22  # Position loop D differential coefficient
HLSS_POSITION_LOOP_KI = 23  # Position loop I Integral coefficient
HLSS_MIN_STARTUP_FORCE = 24  # Minimum startup force
HLSS_INTEGRAL_LIMIT = 25  # Integral limit value
HLSS_PROTECTION_CURRENT_L = 28  # Protection current low byte
HLSS_PROTECTION_CURRENT_H = 29  # Protection current high byte
HLSS_ANGULAR_RESOLUTION = 30  # Angular resolution
HLSS_CURRENT_LOOP_KP = 34  # Current loop P proportional coefficient
HLSS_CURRENT_LOOP_KI = 35  # Current loop I integral coefficient
HLSS_SPEED_LOOP_KP = 37  # Speed loop P proportional coefficient
HLSS_OVER_CURRENT_PROTECTION_TIME = 38  # Over current protection time
HLSS_SPEED_LOOP_KI = 39  # Speed loop I integral coefficient
HLSS_KP = 50  # Kp
HLSS_KD = 51  # Kd
HLSS_KI = 52  # Ki
HLSS_KM = 53  # Km
HLSS_LOCK_MARK = 55  # Lock mark
HLSS_CURRENT_LOCATION_L = 56  # Current location low byte
HLSS_CURRENT_LOCATION_H = 57  # Current location high byte
HLSS_CURRENT_LOAD_L = 60  # Current load low byte
HLSS_CURRENT_LOAD_H = 61  # Current load high byte
HLSS_ASYNC_WRITE_FLAG = 64  # Asynchronous write flag

class hls_scs(protocol_packet_handler):
    def __init__(self, portHandler):
        protocol_packet_handler.__init__(self, portHandler, 0)
        self.groupSyncWrite = GroupSyncWrite(self, HLSS_ACCELERATION, 7)

    def WritePosEx(self, scs_id, position, speed, acc):
        txpacket = [acc, self.scs_lobyte(position), self.scs_hibyte(position), 0, 0, self.scs_lobyte(speed), self.scs_hibyte(speed)]
        return self.writeTxRx(scs_id, HLSS_ACCELERATION, len(txpacket), txpacket)

    def ReadPos(self, scs_id):
        scs_present_position, scs_comm_result, scs_error = self.read2ByteTxRx(scs_id, HLSS_PRESENT_POSITION_L)
        return self.scs_tohost(scs_present_position, 15), scs_comm_result, scs_error

    def ReadSpeed(self, scs_id):
        scs_present_speed, scs_comm_result, scs_error = self.read2ByteTxRx(scs_id, HLSS_PRESENT_SPEED_L)
        return self.scs_tohost(scs_present_speed, 15), scs_comm_result, scs_error

    def ReadPosSpeed(self, scs_id):
        scs_present_position_speed, scs_comm_result, scs_error = self.read4ByteTxRx(scs_id, HLSS_PRESENT_POSITION_L)
        scs_present_position = self.scs_loword(scs_present_position_speed)
        scs_present_speed = self.scs_hiword(scs_present_position_speed)
        return self.scs_tohost(scs_present_position, 15), self.scs_tohost(scs_present_speed, 15), scs_comm_result, scs_error

    def ReadMoving(self, scs_id):
        moving, scs_comm_result, scs_error = self.read1ByteTxRx(scs_id, HLSS_MOVEMENT_STATE)
        return moving, scs_comm_result, scs_error

    def SyncWritePosEx(self, scs_id, position, speed, acc):
        txpacket = [acc, self.scs_lobyte(position), self.scs_hibyte(position), 0, 0, self.scs_lobyte(speed), self.scs_hibyte(speed)]
        return self.groupSyncWrite.addParam(scs_id, txpacket)

    def RegWritePosEx(self, scs_id, position, speed, acc):
        txpacket = [acc, self.scs_lobyte(position), self.scs_hibyte(position), 0, 0, self.scs_lobyte(speed), self.scs_hibyte(speed)]
        return self.regWriteTxRx(scs_id, HLSS_ACCELERATION, len(txpacket), txpacket)

    def RegAction(self):
        return self.action(BROADCAST_ID)

    def WheelMode(self, scs_id):
        return self.write1ByteTxRx(scs_id, HLSS_OPERATION_MODE, 1)

    def WriteSpec(self, scs_id, speed, acc):
        speed = self.scs_toscs(speed, 15)
        txpacket = [acc, 0, 0, 0, 0, self.scs_lobyte(speed), self.scs_hibyte(speed)]
        return self.writeTxRx(scs_id, HLSS_ACCELERATION, len(txpacket), txpacket)

    def LockEprom(self, scs_id):
        return self.write1ByteTxRx(scs_id, HLSS_LOCK, 1)

    def unLockEprom(self, scs_id):
        return self.write1ByteTxRx(scs_id, HLSS_LOCK, 0)

