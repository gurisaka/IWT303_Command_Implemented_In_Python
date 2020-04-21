'''
iwt303 host controller

Copyright (c) 2020 S.K. Technology Firm

Released under the MIT License
'''

import sys
import time
import usb
import usb.core
import usb.util

ID_VENDOR	= 0x16c0
ID_PRODUCT	= 0x05df

#basic functions
def get_device_handle(id_vender, id_product, serial_number = None):
	for bus in usb.busses():
		for device in bus.devices:
			if device.idVendor == id_vender and device.idProduct == id_product:
				if serial_number != None and serial_number == device.dev.serial_number:
					return device.dev
				elif serial_number == None:
					return device.dev

	raise ValueError('Device not found')

def hid_set_report(device_handle, data_stage):
	bmRequestType	= 0b00100000
	bRequest		= 0x09
	wValue			= (0x03 << 8) #[0x03,0x00]
	wIndex			= 0x00
	device_handle.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, data_stage)

#device functions
def list_devices():
	for bus in usb.busses():
		for device in bus.devices:
			if device.idVendor == ID_VENDOR and device.idProduct == ID_PRODUCT:
				print(device.dev.serial_number)

def device_control(serial_number, value):
	data_stage = [0]*16
	data_stage[0] = 0x81
	data_stage[1] = value

	device_handle = get_device_handle(ID_VENDOR, ID_PRODUCT, serial_number = serial_number)

	hid_set_report(device_handle, data_stage)

def device_init():
	serial_number = str(int(time.time()))

	data_stage = [0x82]
	data_stage.extend([ord(n) for n in serial_number])
	data_stage.extend([0]*(16-len(data_stage)))

	device_handle = get_device_handle(ID_VENDOR, ID_PRODUCT, serial_number = None)

	hid_set_report(device_handle, data_stage)

def usage():
	print("IWT303 Command")
	print("usage:")
	print("sudo python3 %s list ... List all serial number of IWT303(s)" % sys.argv[0])
	print("sudo python3 %s set <SerialNumber|\"ANY\"> <StateNumber> ... Set state of relays" % sys.argv[0])

if __name__ == '__main__':
	if len(sys.argv) == 1:
		usage()

	elif sys.argv[1] == "list":
		list_devices()

	elif sys.argv[1] == "set":
		try:
			if sys.argv[2] == "ANY":
				serial_number = None
			else:
				serial_number = sys.argv[2]
			device_control(serial_number, ord(sys.argv[3][0]))
		except IndexError:
			usage()

	elif sys.argv[1] == "init":
		device_init()

	else:
		usage()
