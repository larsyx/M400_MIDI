
from fastapi.templating import Jinja2Templates
from app.DAO.channel_dao import ChannelDAO
from app.DAO.layout_canale_dao import LayoutCanaleDAO
from app.DAO.partecipazione_scena_dao import PartecipazioneScenaDAO
from app.DAO.user_dao import UserDAO
import os

class UserController:
    def __init__(self):
        self.userDAO = UserDAO()
        self.partecipazioneScenaDAO = PartecipazioneScenaDAO()
        self.layoutCanaleDAO = LayoutCanaleDAO()
        self.channelDAO = ChannelDAO()
        self.templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "View", "user"))

    def load_scene(self, scenaID, userID, request):
        
        canali = self.layoutCanaleDAO.getLayoutCanale(userID, scenaID)
        aux = self.partecipazioneScenaDAO.getAuxUser(userID, scenaID)
            
        # get value canali
       
        return self.templates.TemplateResponse("scene.html", {"request": request, "canali": canali, "indirizzoaux": aux.indirizzoMidi, "indirizzoauxMain": aux.indirizzoMidiMain})
        
    def set_layout(self, userID, scenaID, request):
        
        channels = self.channelDAO.get_all_channels()
        layouts = self.layoutCanaleDAO.getLayoutCanale(userID, scenaID)
        
        layout_canali_ids = {layout_canale.canaleId for layout_canale in layouts}

        channel = [channel for channel in channels if channel.id not in layout_canali_ids]

        return self.templates.TemplateResponse("layout.html", {"request": request, "canali": channel, "layout": layouts})
      

      