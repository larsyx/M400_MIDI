from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.dao.channel_dao import ChannelDAO
from app.dao.aux_dao import AuxDAO
from app.dao.user_dao import UserDAO
from midi.midi_controller import MidiController, MidiListener, call_type
import os 

class VideoService():

    def __init__(self):
        load_dotenv()
        self.userDAO = UserDAO()
        self.channelDAO = ChannelDAO()
        self.auxDAO = AuxDAO()
        self.postMainFader = [int(val,16) for val in os.getenv("Main_Post_Fix_Fader").split(",")]
        self.postMainSwitch = [int(val,16) for val in os.getenv("Main_Post_Fix_Switch").split(",")]
        self.auxId = os.getenv("VIDEO_AUX_ID") 
        self.templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "view", "video"))
        self.midiController = MidiController()

    def load_scene(self, request):
        canali = self.channelDAO.get_all_channels()
        aux = self.auxDAO.get_aux_by_id(self.auxId)

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
        resultsValue = MidiListener.init_and_listen(listenAddressFader, call_type.CHANNEL)
        resultsValueSet = []
        
        # get channel value
        for address_channel in listenAddressFader:
            try:
                resultsValueSet.append(resultsValue[tuple(address_channel)])
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
        resultsValueSwitch = MidiListener.init_and_listen([auxIndirizzoMainSwitch], call_type.SWITCH)

        if resultsValueSwitch:
            switchMain = list(resultsValueSwitch.items())[0]
        else:
            switchMain = False

        return self.templates.TemplateResponse("scene.html", {"request": request, "canali": coppieCanali, "valueMain" : valueMain, "switchMain": switchMain})

    def set_fader(self, channel_id, value):
        channel_address = self.channelDAO.get_channel_address(channel_id)
    
        if(channel_address != None):
            aux = self.auxDAO.get_aux_by_id(self.auxId) 

            channelAddresshex = [int(x,16) for x in channel_address.split(",")]
            address_aux = [int(x,16) for x in aux.indirizzoMidi.split(",")]

            address = channelAddresshex + address_aux
            
            self.midiController.send_command(address, MidiController.convert_fader_to_hex(int(value)))

    def set_fader_main(self, value):
        aux = self.auxDAO.get_aux_by_id(self.auxId) 

        if aux:
            address_aux_main = [int(x,16) for x in aux.indirizzoMidiMain.split(",")] + self.postMainFader
            self.midiController.send_command(address_aux_main, MidiController.convert_fader_to_hex(int(value)))

    def set_switch_main(self, value):
        aux = self.auxDAO.get_aux_by_id(self.auxId)

        if aux:
            address_aux_main = [int(x,16) for x in aux.indirizzoMidiMain.split(",")] + self.postMainSwitch
            self.midiController.send_command(address_aux_main, MidiController.convert_switch_to_hex(value))