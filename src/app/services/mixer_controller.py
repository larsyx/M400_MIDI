import os
import time
from fastapi.templating import Jinja2Templates
from app.DAO.channel_dao import ChannelDAO
from app.DAO.dca_dao import DCA_DAO
from midi.midiController import MidiController, MidiListener, call_type
from dotenv import load_dotenv


class MixerController:
    def __init__(self):
        self.channelDAO = ChannelDAO()
        self.dcaDAO = DCA_DAO()

        load_dotenv()
        self.postMainFader = [int(val,16) for val in os.getenv("Main_Post_Fix_Fader").split(",")]
        self.postSwitch = [int(val,16) for val in os.getenv("Main_Post_Fix_Switch").split(",")]
        self.preMain = [int(val,16) for val in os.getenv("Main_Pre_Fix").split(",")]
        self.webSocketIp = os.getenv("WEBSOCKET_IP")
        self.templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "View", "mixer"))


    def loadFader(self, request):
        canali = self.channelDAO.get_all_channels()
        dca = self.dcaDAO.get_dca()
                    
        # get value canali
        midiController = MidiController("pedal")
        
        listenAddressFader = []
        listenAddressSwitch = []

        # initialize the list of addresses for request and listen
        for canale in canali:
            channelAddress = [int(x,16) for x in canale.indirizzoMidi.split(",")] 
            
            listenAddressFader.append(channelAddress + self.postMainFader)
            listenAddressSwitch.append(channelAddress + self.postSwitch)

        for dcaChannel in dca:
            dcaFader = [int(x,16) for x in dcaChannel.indirizzoMidiFader.split(",")] 
            dcaSwitch = [int(x,16) for x in dcaChannel.indirizzoMidiSwitch.split(",")]

            listenAddressFader.append(dcaFader)
            listenAddressSwitch.append(dcaSwitch)


        listenAddressFader.append(self.preMain + self.postMainFader)
        listenAddressSwitch.append(self.preMain + self.postSwitch)


        # channel request and listen
        listen = MidiListener(listenAddressFader, call_type.CHANNEL)

        start = time.time()

        for address in listenAddressFader:
            midiController.request_value(address)

        while time.time() - start < 10:
            time.sleep(0.5)
            if listen.has_received_all():
                break

        listen.stop()
        resultsValue = listen.get_results()
        
        resultsValueSet = []
        
        # get channel value
        for canale in canali:
            channelAddress = [int(x,16) for x in canale.indirizzoMidi.split(",")] 
            try:
                resultsValueSet.append(resultsValue[tuple(channelAddress + self.postMainFader)])
            except KeyError as k:
                print("errore chiave ", k)
                resultsValueSet.append(0)

        # get dca value
        resultDcaValueSet = []

        for dcaChannel in dca:
            dcaAddress = [int(x,16) for x in dcaChannel.indirizzoMidiFader.split(",")] 
            try:
                resultDcaValueSet.append(resultsValue[tuple(dcaAddress)])
            except KeyError as k:
                print("errore chiave ", k)
                resultDcaValueSet.append(0)

        # get main fader value
        try:
            valueMain = resultsValue[tuple(self.preMain + self.postMainFader)]
        except KeyError as e:
            print(f"error key {e}")
            valueMain = 0


        # Channel switch get value and listen
        listenSwitch = MidiListener(listenAddressSwitch, call_type.SWITCH)

        start = time.time()

        for address in listenAddressSwitch:
            midiController.request_value(address)

        while time.time() - start < 10:
            time.sleep(0.5)
            if listenSwitch.has_received_all():
                break

        listenSwitch.stop()

        resultsValueSwitch = listenSwitch.get_results()
        
        resultsValueSetSwitch = []
        
        for canale in canali:
            channelAddress = [int(x,16) for x in canale.indirizzoMidi.split(",")] 
            try:
                resultsValueSetSwitch.append(resultsValueSwitch[tuple(channelAddress + self.postSwitch)])
            except KeyError as k:
                print("errore chiave ", k)
                resultsValueSetSwitch.append(0)

        resultDcaValueSetSwitch = []

        for dcaChannel in dca:
            dcaAddress = [int(x,16) for x in dcaChannel.indirizzoMidiSwitch.split(",")] 
            try:
                resultDcaValueSetSwitch.append(resultsValueSwitch[tuple(dcaAddress)])
            except KeyError as k:
                print("errore chiave ", k)
                resultDcaValueSetSwitch.append(0)

        try:
            switchMain = resultsValueSwitch[tuple(self.preMain + self.postSwitch)]
        except KeyError as e:
            print(f"error key {e}")
            switchMain = False

        coppieCanali = list(zip(canali, resultsValueSet, resultsValueSetSwitch))
        

        #DCA
        coppieDca = list(zip(dca, resultDcaValueSet, resultDcaValueSetSwitch))

        return self.templates.TemplateResponse("scene.html", {"request": request, "canali": coppieCanali, "dcas": coppieDca, "valueMain" : valueMain, "switchMain" : switchMain, "ipSocket" : self.webSocketIp})
        

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

    def setMainFaderValue(self, value):

        midiController = MidiController("pedal")

        indirizzo = self.preMain + self.postMainFader
        
        midiController.send_command(indirizzo, MidiController.convertValue(int(value)))

    def setMainSwitchChannel(self, switch):
        midiController = MidiController("pedal")
    
        indirizzo = self.preMain + self.postSwitch
        midiController.send_command(indirizzo, MidiController.convertSwitch(switch))

    def setDcaFaderValue(self, dca_id, value):
        midiController = MidiController("pedal")
        dca = self.dcaDAO.get_dca_by_id(dca_id)

        if dca:
            address = [int(x, 16) for x in dca.indirizzoMidiFader.split(",")]
            midiController.send_command(address, MidiController.convertValue(int(value)))

    def setDcaSwitchChannel(self, dca_id, switch):
        midiController = MidiController("pedal")
        dca = self.dcaDAO.get_dca_by_id(dca_id)

        if dca:
            address = [int(x, 16) for x in dca.indirizzoMidiSwitch.split(",")]
            midiController.send_command(address, MidiController.convertSwitch(switch))