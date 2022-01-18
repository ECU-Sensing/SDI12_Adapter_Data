    """SDI12 - USB Adapter by Liudr data collection script. Intended to be used with Raspberry Pi LoRa Driving code (https://github.com/ECU-Sensing/Raspi_Zero_Node)

        Author: Colby Sawyer 1-5-2022
    """
#TODO Add support for more devices
from devices.hydros import Hydros
import serial.tools.list_ports
import serial
import time
import re

#TODO Add data connection testing (multiple device support)
#TODO Add device specific classes (allow for specific data representation)

#//=========================================
def get_data():
    """Main driver to fetch most recent data and return in the form of a bytearray for transmitting over LoRA

    Returns:
        bytearray: bytearray containing encoded data from the logger (intended for LoRa usage)
    """
    sensor = Hydros()
    #sensor_data = sensor.get_data()
    sensor_data = sensor.get_data_from_adapter()
    
    return sensor_data
#//=========================================
