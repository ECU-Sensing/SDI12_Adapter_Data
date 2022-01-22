# Main class for the Hydros 21 / Decagon CDT-10 water sensors
#   Intended to be used with the LoRa transmission driver code
# Author: Colby Sawyer 1-5-2022
import serial.tools.list_ports
import serial
import time
import re

class Hydros:
    water_depth = 0
    temperature = 0
    electrical_conductivity = 0

    def __init__(self, water_depth=0, temperature=0, conductivity=0):
        self.water_depth = water_depth
        self.temperature = temperature
        self.electrical_conductivity = conductivity

    def get_data(self):
        sensor_data = bytearray(7)
        FEATHER_ID = 1

        depth_val = int(self.water_depth)
        print("Water Depth: %0.1f %%" % depth_val)

        temp_val = int(self.temperature)
        print("Temperature: %0.1f %%" % depth_val)

        conduc_val = int(self.electrical_conductivity)
        print("Conductivity: %0.1f %%" % depth_val)

        sensor_data[0] = FEATHER_ID
        # Water Depth
        sensor_data[1] = (depth_val >> 8) & 0xff
        sensor_data[2]= depth_val & 0xff
        # Temperature
        sensor_data[3] = (temp_val >> 8) & 0xff
        sensor_data[4] = temp_val & 0xff
        #Conductivity
        sensor_data[5] = (conduc_val >> 8) & 0xff
        sensor_data[6] = conduc_val & 0xff

        return sensor_data

    def get_data_from_adapter(self):
        # Simple SDI-12 Sensor Reader Copyright Dr. John Liu
        rev_date = '2018-12-03'
        version = '1.0'

        print('+-' * 40)
        print('Simple SDI-12 Sensor Reader', version)
        print('+-' * 40)

        port_names=[]
        ports = serial.tools.list_ports.comports()
        user_port_selection=0
        i=0
        
        ser=serial.Serial(port=ports[int(user_port_selection)].device,baudrate=9600,timeout=10)
        time.sleep(2.5) # delay for arduino bootloader and the 1 second delay of the adapter.

        print('Connecting to sensor ...')
        
        ser.write(b'?!')
        sdi_12_line=ser.readline()
        sdi_12_line=sdi_12_line[:-2] # remove \r and \n since [0-9]$ has trouble with \r
        m=re.search(b'[0-9a-zA-Z]$',sdi_12_line) # having trouble with the \r
        sdi_12_address=m.group(0) # find address
        print('\nSensor address:', sdi_12_address.decode('utf-8'))

        ser.write(sdi_12_address+b'I!')
        sdi_12_line=ser.readline()
        sdi_12_line=sdi_12_line[:-2] # remove \r and \n
        print('Sensor info:',sdi_12_line.decode('utf-8'))

        ser.write(sdi_12_address+b'M!')
        sdi_12_line=ser.readline()
        sdi_12_line=ser.readline()
        ser.write(sdi_12_address+b'D0!')
        sdi_12_line=ser.readline()
        sdi_12_line=sdi_12_line[:-2] # remove \r and \n

        value = sdi_12_line.decode('utf-8')

        print('Sensor reading:', value)

        FEATHER_ID = '1'
        data = (FEATHER_ID + value).encode()

        sensor_data = bytearray(data)
        ser.close()

        return sensor_data

