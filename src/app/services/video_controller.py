from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.DAO.channel_dao import ChannelDAO
from app.DAO.aux_dao import AuxDAO
from app.DAO.user_dao import UserDAO
from midi.midiController import MidiController, MidiListener, call_type
import os 
import time

class VideoController():

    def __init__(self):
        load_dotenv()
        self.userDAO = UserDAO()
        self.channelDAO = ChannelDAO()
        self.auxDAO = AuxDAO()
        self.postMainFader = [int(val,16) for val in os.getenv("Main_Post_Fix_Fader").split(",")]
        self.postMainSwitch = [int(val,16) for val in os.getenv("Main_Post_Fix_Switch").split(",")]
        self.auxId = os.getenv("VIDEO_AUX_ID") 
        self.templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "View", "video"))
        self.midiController = MidiController("pedal")
        self.webSocketIp = os.getenv("WEBSOCKET_IP")

    def loadScene(self, request):
        canali = self.channelDAO.get_all_channels()
        aux = self.auxDAO.getAuxById(self.auxId)

        # get value canali
        
        listenAddressFader = []

        # initialize the list of addresses for request and listen

        auxIndirizzo = [int(x,16) for x in aux.indirizzoMidi.split(",")] 
        auxIndirizzoMain = [int(x,16) for x in aux.indirizzoMidiMain.split(",")] + self.postMainFader
        auxIndirizzoMainSwitch = [int(x,16) for x in aux.indirizzoMidiMain.split(",")] + self.postMainSwitch

        for canale in canali:
            channelAddress = [int(x,16) for x in canale.indirizzoMidi.split(",")]
            listenAddressFader.append(channelAddress + auxIndirizzo)


        listenAddressFader.append(auxIndirizzoMain)


        # channel request and listen
        listen_channel = MidiListener(listenAddressFader, call_type.CHANNEL)

        start = time.time()

        for address in listenAddressFader:
            self.midiController.request_value(address)

        while time.time() - start < 10:
            time.sleep(0.5)
            if listen_channel.has_received_all():
                break

        listen_channel.stop()
        resultsValue = listen_channel.get_results()
        
        resultsValueSet = []
        
        # get channel value
        for canale in canali:
            channelAddress = [int(x,16) for x in canale.indirizzoMidi.split(",")] 
            try:
                resultsValueSet.append(resultsValue[tuple(channelAddress + auxIndirizzo)])
            except KeyError as k:
                print("errore chiave ", k)
                resultsValueSet.append(0)

        # get main fader value
        try:
            valueMain = resultsValue[tuple(auxIndirizzoMain)]
        except KeyError as e:
            print(f"error key {e}")
            valueMain = 0

        coppieCanali = list(zip(canali, resultsValueSet))


        # switch Main request and listen
        listen = MidiListener([auxIndirizzoMainSwitch], call_type.SWITCH)

        start = time.time()

        self.midiController.request_value(auxIndirizzoMainSwitch)

        while time.time() - start < 10:
            time.sleep(0.5)
            if listen.has_received_all():
                break

        listen.stop()
        resultsValueSwitch = listen.get_results()

        switchMain = list(resultsValueSwitch.items())[0]

        return self.templates.TemplateResponse("scene.html", {"request": request, "canali": coppieCanali, "valueMain" : valueMain, "switchMain": switchMain, "ipSocket" : self.webSocketIp})


    def setFader(self, channel_id, value):
        channel_address = self.channelDAO.get_channel_address(channel_id)
    
        if(channel_address != None):
            aux = self.auxDAO.getAuxById(self.auxId) 

            channelAddresshex = [int(x,16) for x in channel_address.split(",")]
            address_aux = [int(x,16) for x in aux.indirizzoMidi.split(",")]

            address = channelAddresshex + address_aux
            
            self.midiController.send_command(address, MidiController.convertValue(int(value)))


    def setFaderMain(self, value):
        aux = self.auxDAO.getAuxById(self.auxId) 

        if aux:
            address_aux_main = [int(x,16) for x in aux.indirizzoMidiMain.split(",")] + self.postMainFader
            self.midiController.send_command(address_aux_main, MidiController.convertValue(int(value)))

    def setSwitchMain(self, value):
        aux = self.auxDAO.getAuxById(self.auxId)

        if aux:
            address_aux_main = [int(x,16) for x in aux.indirizzoMidiMain.split(",")] + self.postMainSwitch
            self.midiController.send_command(address_aux_main, MidiController.convertSwitch(value))