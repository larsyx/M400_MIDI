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


def roland_checksum(address_bytes, data_bytes):
    total = sum(address_bytes) + sum(data_bytes)
    checksum = (128 - (total % 128)) % 128
    return checksum
    

def build_sysex(address, data):
    checksum = roland_checksum(address, data)
    return header + address + data + [checksum]

   


