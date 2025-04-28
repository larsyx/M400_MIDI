
from fastapi.templating import Jinja2Templates
from app.DAO.layout_canale_dao import LayoutCanaleDAO
from app.DAO.partecipazione_scena_dao import PartecipazioneScenaDAO
from app.DAO.user_dao import UserDAO
import os

class UserController:
    def __init__(self):
        self.userDAO = UserDAO()
        self.partecipazioneScenaDAO = PartecipazioneScenaDAO()
        self.layoutCanaleDAO = LayoutCanaleDAO()


    def load_scene(self, scenaID, userID, request):
        
        canali = self.layoutCanaleDAO.getLayoutCanale(userID, scenaID)
        aux = self.partecipazioneScenaDAO.getAuxUser(userID, scenaID)   
        # get value canali

        templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "View", "user"))
       
        return templates.TemplateResponse("scene.html", {"request": request, "canali": canali, "indirizzoaux": aux.indirizzoMidi})
        