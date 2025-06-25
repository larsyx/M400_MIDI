
import time
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from app.dao.channel_dao import ChannelDAO
from app.dao.layout_canale_dao import LayoutCanaleDAO
from app.dao.partecipazione_scena_dao import PartecipazioneScenaDAO
from app.dao.user_dao import UserDAO
from fastapi.responses import RedirectResponse
import os

from midi.midiController import MidiController, MidiListener, call_type

class UserService:
    def __init__(self):
        load_dotenv()
        self.userDAO = UserDAO()
        self.partecipazioneScenaDAO = PartecipazioneScenaDAO()
        self.layoutCanaleDAO = LayoutCanaleDAO()
        self.channelDAO = ChannelDAO()
        self.templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "view", "user"))
        self.midiController = MidiController("pedal")
        self.postMainFader = [int(val,16) for val in os.getenv("Main_Post_Fix_Fader").split(",")]

    def load_scene(self, scenaID, userID, request):
        
        canali = self.layoutCanaleDAO.get_layout_channel(userID, scenaID)
        aux = self.partecipazioneScenaDAO.get_aux_user(userID, scenaID)
        hasBatteria = False

        if not canali or not aux:
            return RedirectResponse(url="/user/getScenes", status_code=303)
            
        # get value canali
        midiController = MidiController("pedal")

        listenAddress = []
        auxAddress = [int(x,16) for x in aux.indirizzoMidi.split(",")]
        auxAddressMain = [int(x,16) for x in aux.indirizzoMidiMain.split(",")] + self.postMainFader

        for canale in canali:
            channelMidi = self.channelDAO.get_channel_address(channel_id = canale.canaleId)
            channelAddress = [int(x,16) for x in channelMidi.split(",")] 

            if not hasBatteria and canale.isBatteria:
                hasBatteria = True
                
            listenAddress.append(channelAddress + auxAddress)

        listenAddress.append(auxAddressMain)
        listen = MidiListener(listenAddress, call_type.CHANNEL)

        start = time.time()

        for address in listenAddress:
            midiController.request_value(address)

        while time.time() - start < 10:
            time.sleep(0.5)
            if listen.has_received_all():
                break

        
        listen.stop()
        resultsValue = listen.get_results()
        
        resultsValueSet = []
        
        for canale in canali:
            channelMidi = self.channelDAO.get_channel_address(channel_id = canale.canaleId)
            channelAddress = [int(x,16) for x in channelMidi.split(",")] 
          
            try:
                resultsValueSet.append(resultsValue[tuple(channelAddress + auxAddress)])
            except KeyError as e:
                print(f"error key {e}")
                resultsValueSet.append(0)

        try:
            valueMain = resultsValue[tuple(auxAddressMain)]
        except KeyError as e:
            print(f"error key {e}")
            valueMain = 0

        coppieCanali = list(zip(canali, resultsValueSet))
        
        return self.templates.TemplateResponse("scene.html", {"request": request, "canali": coppieCanali, "indirizzoaux": aux.indirizzoMidi, "indirizzoauxMain": aux.indirizzoMidiMain, "valueMain": valueMain, "hasBatteria" : hasBatteria})
        
    def set_layout(self, userID, scenaID, request):
        
        channels = self.channelDAO.get_all_channels()
        layouts = self.layoutCanaleDAO.get_layout_channel(userID, scenaID)
        
        layout_canali_ids = {layout_canale.canaleId for layout_canale in layouts}

        channel = [channel for channel in channels if channel.id not in layout_canali_ids]

        return self.templates.TemplateResponse("layout.html", {"request": request, "canali": channel, "layout": layouts})
      
    def setFader(self, canaleId, value, indirizzoAux):
        canaleAddress = self.channelDAO.get_channel_address(canaleId)
    
        if(canaleAddress != None):
            addressAuxhex = [int(x,16) for x in indirizzoAux.split(",")]
            channelAddresshex = [int(x,16) for x in canaleAddress.split(",")]

            indirizzo = channelAddresshex + addressAuxhex
            
            self.midiController.send_command(indirizzo, MidiController.convertValue(int(value)))
        
    def setFaderMain(self, value, auxAddress):
        addressAuxhex = [int(x,16) for x in auxAddress.split(",")] + self.postMainFader

        self.midiController.send_command(addressAuxhex, MidiController.convertValue(int(value)))