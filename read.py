#!/usr/local/opt/python-3.5.1/bin/python3.5
# Simple SDI-12 Sensor Reader Copyright Dr. John Liu
import serial.tools.list_ports
import serial
import time
import re

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
port_device=a[int(user_port_selection)].device

ser=serial.Serial(port=port_device,baudrate=9600,timeout=10)
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
print('Sensor reading:',sdi_12_line.decode('utf-8'))
print('\nFor complete data logging solution, download the free Python data logger under "data logger programs"\nhttps://liudr.wordpress.com/gadget/sdi-12-usb-adapter/')
ser.close()

