
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from app.dao.channel_dao import ChannelDAO
from app.dao.layout_canale_dao import LayoutCanaleDAO
from app.dao.partecipazione_scena_dao import PartecipazioneScenaDAO
from app.dao.user_dao import UserDAO
from fastapi.responses import RedirectResponse
import os
import json

from midi.midi_controller import MidiController, MidiListener, call_type

class UserService:
    def __init__(self):
        load_dotenv()
        self.userDAO = UserDAO()
        self.partecipazioneScenaDAO = PartecipazioneScenaDAO()
        self.layoutCanaleDAO = LayoutCanaleDAO()
        self.channelDAO = ChannelDAO()
        self.templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "view", "user"))
        self.midiController = MidiController()
        self.postMainFader = [int(val,16) for val in os.getenv("Main_Post_Fix_Fader").split(",")]

    def load_scene(self, scenaID, userID, request):
        
        canali = self.layoutCanaleDAO.get_layout_channel(userID, scenaID)
        aux = self.partecipazioneScenaDAO.get_aux_user(userID, scenaID)
        hasBatteria = False

        if not canali or not aux:
            return RedirectResponse(url="/user/getScenes", status_code=303)

        for canale in canali:
            if not hasBatteria and canale.isBatteria:
                hasBatteria = True
                break

        return self.templates.TemplateResponse("scene.html", {"request": request, "canali": canali, "indirizzoaux": aux.indirizzoMidi, "indirizzoauxMain": aux.indirizzoMidiMain, "hasBatteria" : hasBatteria})
        
    def set_layout(self, userID, scenaID, request):  
        channels = self.channelDAO.get_all_channels()
        layouts = self.layoutCanaleDAO.get_layout_channel(userID, scenaID)
        
        if not layouts:
            return RedirectResponse(url="/user/getScenes", status_code=303)

        layout_canali_ids = {layout_canale.canaleId for layout_canale in layouts}
        channel = [channel for channel in channels if channel.id not in layout_canali_ids]

        return self.templates.TemplateResponse("layout.html", {"request": request, "canali": channel, "layout": layouts})
      
    def set_fader(self, canaleId, value, indirizzoAux):
        canaleAddress = self.channelDAO.get_channel_address(canaleId)
    
        if(canaleAddress != None):
            addressAuxhex = [int(x,16) for x in indirizzoAux.split(",")]
            channelAddresshex = [int(x,16) for x in canaleAddress.split(",")]

            indirizzo = channelAddresshex + addressAuxhex
            
            self.midiController.send_command(indirizzo, MidiController.convert_fader_to_hex(int(value)))
        
    def set_fader_main(self, value, auxAddress):
        addressAuxhex = [int(x,16) for x in auxAddress.split(",")] + self.postMainFader
        self.midiController.send_command(addressAuxhex, MidiController.convert_fader_to_hex(int(value)))

    def get_faders_value(self, user_id, scene_id, aux, aux_main):
        channels = self.layoutCanaleDAO.get_layout_channel(user_id, scene_id)
        listen_address = []
        aux = [int(x,16) for x in aux.split(",")]
        aux_main = [int(x,16) for x in aux_main.split(",")] + self.postMainFader

        for channel in channels:
            channel_midi = self.channelDAO.get_channel_address(channel_id = channel.canaleId)
            channel_address = [int(x,16) for x in channel_midi.split(",")] 

            listen_address.append(channel_address + aux)

        listen_address.append(aux_main)

        results_value = MidiListener.init_and_listen(listen_address, call_type.CHANNEL)

        results_value_set = {}

        for channel in channels:
            channel_midi = self.channelDAO.get_channel_address(channel_id = channel.canaleId)
            channel_address = [int(x,16) for x in channel_midi.split(",")] + aux
            try:
                results_value_set[channel.canaleId] = results_value[tuple(channel_address)]
            except KeyError as e:
                print(f"error key {e}")
                results_value_set[channel.canaleId] = 0

        try:
            results_value_set["main"] = results_value[tuple(aux_main)]
        except KeyError as e:
            print(f"error key {e}")
            results_value_set["main"] = 0

        return json.dumps(results_value_set, indent=2)