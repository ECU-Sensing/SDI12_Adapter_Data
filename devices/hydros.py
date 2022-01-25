# Main class for the Hydros 21 / Decagon CDT-10 water sensors
#   Intended to be used with the LoRa transmission driver code
# Author: Colby Sawyer 1-5-2022
import serial.tools.list_ports
import serial
import time
import re


def parse_reading(val):
    """Takes string of values from sensor and parses them into String list

    Args:
        val (String): [Unparsed string containing multiple reading from sensor ex. "0+40+24.4-140"]

    Returns:
        [String]: [Parsed list of strings each corresponding to a returned measurement]
    """
    res = re.findall(r'[-+][0-9.]+|\D', val)
    return res

class Hydros:
    water_depth = 0
    temperature = 0
    electrical_conductivity = 0
    port_device = None

    def __init__(self, water_depth=0, temperature=0, conductivity=0, port_device=None):
        self.water_depth = water_depth
        self.temperature = temperature
        self.electrical_conductivity = conductivity
        self.port_device = port_device

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
        print(
            'Designed for Dr. Liu\'s family of SDI-12 USB adapters (standard,analog,GPS)\n\tDr. John Liu Saint Cloud MN USA',
            rev_date, '\n\t\tFree software GNU GPL V3.0')
        print('\nCompatible with PCs running Win 7/10, GNU/Linux, Mac OSX, Raspberry PI, Beagle Bone Black')
        print('\nThis program requires Python 3.4, Pyserial 3.0')
        print('\nFor assistance with customization, telemetry etc., contact Dr. Liu.')
        print('\nhttps://liudr.wordpress.com/gadget/sdi-12-usb-adapter/')
        print('+-' * 40)

        port_names=[]
        a = serial.tools.list_ports.comports()
        print('\nDetected the following serial ports:')
        i=0
        for w in a:
            vidn=w.vid if (type(w.vid) is int) else 0
            print('%d)\t%s\t(USB VID=%04X)' % (i, w.device, vidn))
            i=i+1
        user_port_selection = input('\nSelect port from list (0,1,2...). SDI-12 adapter has USB VID=0403:')
        # Store the device name to open port with later in the script.
        self.port_device=a[int(user_port_selection)].device

        ser=serial.Serial(port=self.port_device,baudrate=9600,timeout=10)
        time.sleep(2.5) # delay for arduino bootloader and the 1 second delay of the adapter.

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

        parsed_values = parse_reading(value)
        if len(parsed_values) > 3:
            self.depth = float(parsed_values[1])
            self.temperature = float(parsed_values[2])
            self.electrical_conductivity = float(parsed_values[3])
        else:
            raise ValueError('SENSOR ERROR: Reading from sensor doesnt match explicitly defined format.')

        print('Sensor reading:', parsed_values)
        
        sensor_data = bytearray(7)
        FEATHER_ID = 1

        depth_val = self.water_depth
        print("Water Depth: %0.1f %%" % depth_val)

        temp_val = self.temperature
        print("Temperature: %0.1f %%" % temp_val)

        conduc_val = self.electrical_conductivity
        print("Conductivity: %0.1f %%" % conduc_val)

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

