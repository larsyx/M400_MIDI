


import os
import time

from fastapi.templating import Jinja2Templates
from app.DAO.channel_dao import ChannelDAO
from midi.midiController import MidiController, MidiListener
from dotenv import load_dotenv


class MixerController:
    def __init__(self):
        self.channelDAO = ChannelDAO()
        load_dotenv()
        self.postMainFader = [int(val,16) for val in os.getenv("Main_Post_Fix_Fader").split(",")]
        self.postSwitch = [int(val,16) for val in os.getenv("Main_Post_Fix_Switch").split(",")]
        self.templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "View", "mixer"))


    def loadFader(self, request):
        canali = self.channelDAO.get_all_channels()
                    

        # get value canali
        midiController = MidiController("pedal")
        
        listenAddress = []

        for canale in canali:
            channelAddress = [int(x,16) for x in canale.indirizzoMidi.split(",")] 
            
            listenAddress.append(channelAddress + self.postMainFader)


        listen = MidiListener(listenAddress)

        start = time.time()

        for address in listenAddress:
            print(f"indirizzo: {address}")
            midiController.request_value(address)

        while time.time() - start < 10:
            time.sleep(0.5)
            if listen.has_received_all():
                print("Tutti ricevuti.")
                break

        listen.stop()
        print("thread terminato")
        resultsValue = listen.get_results()
        
        resultsValueSet = []
        
        for canale in canali:
            channelAddress = [int(x,16) for x in canale.indirizzoMidi.split(",")] 
            try:
                resultsValueSet.append(resultsValue[tuple(channelAddress + self.postMainFader)])
            except KeyError as k:
                print("errore chiave ", k)
                resultsValueSet.append(0)

        print(resultsValueSet)

        coppieCanali = list(zip(canali, resultsValueSet))
        
        return self.templates.TemplateResponse("scene.html", {"request": request, "canali": coppieCanali})
        

    def setFaderValue(self, canaleId, value):

        midiController = MidiController("pedal")

        canaleAddress = self.channelDAO.get_channel_address(canaleId)
        
        if(canaleAddress != None):
            channelAddresshex = [int(x,16) for x in canaleAddress.split(",")]

            indirizzo = channelAddresshex + self.postMainFader
            
            midiController.send_command(indirizzo, MidiController.convertValue(int(value)))

    def setSwitchChannel(self, canaleId, switch):
        canaleAddress = self.channelDAO.get_channel_address(canaleId)
        midiController = MidiController("pedal")
        
        if(canaleAddress != None):
            channelAddresshex = [int(x,16) for x in canaleAddress.split(",")]

            indirizzo = channelAddresshex + self.postSwitch
            midiController.send_command(indirizzo, MidiController.convertSwitch(switch))

