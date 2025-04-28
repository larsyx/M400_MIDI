import math
import mido
from dotenv import load_dotenv
import os

#header = [0xF0, 0x41, 0x10, 0x00, 0x00, 0x24, 0x12]

load_dotenv()
Manufacturer_ID = int(os.getenv("MANUFACTURER_ID"), 0)
Device_ID = int(os.getenv("DEVICE_ID"), 0)
Model_ID = [int(val,0) for val in os.getenv("MODEL_ID").split(",")]
Command_ID = int(os.getenv("Command_ID_Data_Set"), 0)

header = [int(Manufacturer_ID), int(Device_ID)] + [int(a) for a in Model_ID] + [int(Command_ID)]



class MidiController: 
    def __init__(self, name):
        self.ped = mido.get_output_names()[1]

    
    def send_command(self, address, data):
        sysex_msg = build_sysex(address, data)

        msg = mido.Message('sysex', data=sysex_msg)

        with mido.open_output(self.ped) as outport:
            outport.send(msg)

    def convertValue(value):
        if value == 0:
            return [0x78, 0x76]
        if value >=75:
            newvalue = ((value-75)/25)*100 
            return [0x00, int(newvalue)]
        
        #conversione in db
        decibel = 0
        if value >= 50:
            decibel = (((value-50)*10)/25) -10

        if value < 50 and value >= 20:
            decibel = value - 60

        if value < 20 and value >= 10:
            decibel = ((value-10)*2) -60

        if value < 10 and value >= 1:
            decibel = ((value-1)*(29.6/9))-89.6


        div = decibel/-12.
        8
        first_value = 128 - math.ceil(div)
        second_value = int((math.ceil(div) - div)*127)

        return [first_value, second_value]
    

def roland_checksum(address_bytes, data_bytes):
    total = sum(address_bytes) + sum(data_bytes)
    checksum = (128 - (total % 128)) % 128
    return checksum
    

def build_sysex(address, data):
    checksum = roland_checksum(address, data)
    return header + address + data + [checksum]

   


