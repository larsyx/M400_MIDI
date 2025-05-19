import asyncio
import math
import threading
import mido
from dotenv import load_dotenv
import os
from enum import Enum
#header = [0xF0, 0x41, 0x10, 0x00, 0x00, 0x24, 0x12]

load_dotenv()
Manufacturer_ID = int(os.getenv("MANUFACTURER_ID"), 0)
Device_ID = int(os.getenv("DEVICE_ID"), 0)
Model_ID = [int(val,0) for val in os.getenv("MODEL_ID").split(",")]
Command_ID_Set = int(os.getenv("Command_ID_Data_Set"), 0)
Command_ID_Request = int(os.getenv("Command_ID_Data_Request"), 0)
fader_post = [int(val,0) for val in os.getenv("Main_Post_Fix_Fader").split(",")]
switch_post = [int(val,0) for val in os.getenv("Main_Post_Fix_Switch").split(",")]
preMain = os.getenv("Main_Pre_Fix")

preDca = [0x09]
dca_fader_post = [0x00, 0x0A]
dca_switch_post = [0x00, 0x08]

header = [int(Manufacturer_ID), int(Device_ID)] + [int(a) for a in Model_ID] 




class MidiController: 
    def __init__(self, name):
        self.ped = mido.get_output_names()[1]

    
    def send_command(self, address, data):
        sysex_msg = build_sysex(address, Command_ID_Set, data)

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


        div = decibel/-12.8
        first_value = 128 - math.ceil(div)
        second_value = int((math.ceil(div) - div)*127)

        return [first_value, second_value]
    
    def convertSwitch(switch):
        return [0x00] if switch else [0x01] 

    def request_value(self, address):
        data = [0x00, 0x00, 0x00, 0x04]
        sysex_msg = build_sysex(address, Command_ID_Request, data)

        msg = mido.Message('sysex', data=sysex_msg)

        with mido.open_output(self.ped) as outport:
            outport.send(msg)


def roland_checksum(address_bytes, data_bytes):
    total = sum(address_bytes) + sum(data_bytes)
    checksum = (128 - (total % 128)) % 128
    return checksum
    

def build_sysex(address, command, data):
    checksum = roland_checksum(address, data)
    return header + [command] + address + data + [checksum]

   

class call_type(Enum):
    CHANNEL = "channel"
    SWITCH = "switch"

class MidiListener:
    def __init__(self, midi_addresses, calltype):
        self.midi_addresses = [tuple(addr) for addr in midi_addresses]
        self.received = {}
        self.lock = threading.Lock()
        self.running = True

        if calltype == call_type.CHANNEL:
            callfn = self.callbackChannel
        elif calltype == call_type.SWITCH:
            callfn = self.callbackSwitch

        self.callback = callfn

        get_midi_multiplexer().register(self.callback)

    def callbackChannel(self, msg):
        if not self.running:
            return
        if msg.type == 'sysex':
            data = tuple(msg.data)
            key = data[6:10]
            with self.lock:
                if key in self.midi_addresses and key not in self.received:
                    self.received[key] = MidiListener.convert_value(data[10], data[11])

    def callbackSwitch(self, msg):
        if not self.running:
            return
        if msg.type == 'sysex':
            data = tuple(msg.data)
            key = data[6:10]
            with self.lock:
                if key in self.midi_addresses and key not in self.received:
                    self.received[key] = MidiListener.convert_switch(data[10])

    def stop(self):
        self.running = False
        get_midi_multiplexer().unregister(self.callback)

    def has_received_all(self):
        with self.lock:
            return len(self.received) == len(self.midi_addresses)
    
    def get_results(self):
        with self.lock:
            return dict(self.received)
        
    def convert_value(firstValue, secondValue):
        try:
            if firstValue == 0x00:
                value = (secondValue / 100) * 25 + 75
                return round(value)
            elif firstValue == 0x78:
                return 0
            elif firstValue == 0x79 or firstValue == 0x7A:
                norm = round(((secondValue/127) * 4) + 1)
                return norm if firstValue == 0x79 else norm + 4
            elif firstValue == 0x7B:
                norm = round((secondValue/127) * 6) 
                return norm + 9
            elif firstValue == 0x7C:
                norm = round((secondValue/127) * 6)
                return norm + 15
            elif firstValue == 0x7D:
                norm = round((secondValue/127) * 12)
                return norm + 22
            elif firstValue == 0x7E:
                norm = round((secondValue/127) * 12)
                return norm + 35
            elif firstValue == 0x7F:
                norm = round((secondValue/127) * 24)
                return norm + 48
            
            return 0
        except Exception as e:
            print(f"errore: {e}")
        

    def convert_switch(value):
        return False if value == 0x01 else True
    

class MidiUserSync():
    def __init__(self, sendback, address):
        self.loop = asyncio.get_event_loop()
        self.send_back = sendback
        self.post_address = address

        get_midi_multiplexer().register(self.listening)

    def stop(self):
        get_midi_multiplexer().unregister(self.listening)


    def listening(self, msg):

        if msg.type == 'sysex':
            data = tuple(msg.data)

            if data[:5] == tuple(header) and data[5] == Command_ID_Set:
                canale = f"0x{data[6]:02X}, 0x{data[7]:02X}"
                valore = 0
                if data[8:10] == tuple(self.post_address):
                    valore = MidiListener.convert_value(data[10], data[11])

                    asyncio.run_coroutine_threadsafe(
                        self.send_back(canale, valore),
                        self.loop
                    )



class MidiMixerSync():
    def __init__(self, send_back):
        self.loop =  asyncio.get_event_loop()
        self.send_back = send_back

        get_midi_multiplexer().register(self.listening)

    def stop(self):
        get_midi_multiplexer().unregister(self.listening)


    def listening(self, msg):

        if msg.type == 'sysex':
            data = tuple(msg.data)

            if data[:5] == tuple(header) and data[5] == Command_ID_Set:
                canale = f"0x{data[6]:02X}, 0x{data[7]:02X}"
                
                if canale == preMain:
                    canale = "main"
                typeCmd =""
                valore = 0
                if data[8:10] == tuple(switch_post):
                    typeCmd = "switch"
                    valore = MidiListener.convert_switch(data[10])
                elif data[8:10] == tuple(fader_post):
                    valore = MidiListener.convert_value(data[10], data[11])
                    typeCmd = "fader"

                if data[6] == preDca[0]:
                    canale = f"0x{data[6]:02X}, 0x{data[7]:02X}, 0x{data[8]:02X}, 0x{data[9]:02X}"
                    if data[8:10] == tuple(dca_fader_post):
                        valore = MidiListener.convert_value(data[10], data[11])
                        typeCmd = "fader"
                    elif data[8:10] == tuple(dca_switch_post):
                        typeCmd = "switch"
                        valore = MidiListener.convert_switch(data[10])
                    
                asyncio.run_coroutine_threadsafe(
                    self.send_back(typeCmd, canale, valore),
                    self.loop
                )

class MidiMultiplexer:
    def __init__(self):
        self.callbacks = []
        self.lock = threading.Lock()
        port_name = mido.get_input_names()[0]
        self.port = mido.open_input(port_name, callback=self._dispatch)

    def _dispatch(self, msg):
        with self.lock:
            for cb in self.callbacks:
                cb(msg)
            
    def register(self, callback):
        with self.lock:
            self.callbacks.append(callback)

    def unregister(self, callback):
        with self.lock:
            self.callbacks.remove(callback)

    def close(self):
        self.port.close()



_multiplexer_instance = None

def get_midi_multiplexer():
    global _multiplexer_instance
    if _multiplexer_instance is None:
        _multiplexer_instance = MidiMultiplexer()
    return _multiplexer_instance