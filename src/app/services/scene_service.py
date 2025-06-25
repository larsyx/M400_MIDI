from http.client import HTTPResponse
import os
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.dao.aux_dao import AuxDAO
from app.dao.partecipazione_scena_dao import PartecipazioneScenaDAO
from app.dao.scene_dao import SceneDAO
from app.dao.user_dao import UserDAO
from app.dao.layout_canale_dao import LayoutCanaleDAO
from dotenv import load_dotenv
from midi.midiController import MidiListener, call_type, MidiController
import time

class SceneService:
    def __init__(self):
        self.sceneDAO = SceneDAO()
        self.auxDAO = AuxDAO()
        self.utenteDAO = UserDAO()
        self.partecipazioneScenaDAO = PartecipazioneScenaDAO()
        self.layoutCanaleDAO = LayoutCanaleDAO()
        self.templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "view", "administration"))
        load_dotenv()
        self.postName = [int(val,16) for val in os.getenv("Fader_Post_Name").split(",")]
        self.midiController = MidiController("ped")

    def manageScene(self, request, adminUser):
        if self.utenteDAO.is_admin(adminUser):
            scenes = self.sceneDAO.get_all_scenes()
            return self.templates.TemplateResponse(request, "manage_scene.html", {"scenes" : scenes, })
        
        else:    
            return HTMLResponse(status_code=403, content="Non hai i permessi per accedere a questa risorsa")

    def create_scene(self, request, adminUser, nome, descrizione):
        if self.utenteDAO.is_admin(adminUser) == False:
            return HTTPResponse(status_code=403, content="Non hai i permessi per accedere a questa risorsa")
        
        scenes = self.sceneDAO.get_all_scenes()

        try:
            new_scene = self.sceneDAO.create_scene(nome, descrizione)
            scenes.append(new_scene)
            return self.templates.TemplateResponse(request, "manage_scene.html", {"scenes" : scenes, "message" : f"scena {new_scene.nome} creata con successo" })
        except Exception as e:
            print(f"Error creating scene: {e}")
            return self.templates.TemplateResponse(request, "manage_scene.html", {"scenes" : scenes, "message" : f"errore creazione scena {e}" })

    def get_scene(self, request, adminUser, id):
        if self.utenteDAO.is_admin(adminUser) == False:
            return HTTPResponse(status_code=403, content="Non hai i permessi per accedere a questa risorsa")

        try:
            scene = self.sceneDAO.get_scene_by_id(id)
            auxs = self.auxDAO.get_all_aux()
            partecipazioni = self.partecipazioneScenaDAO.get_participants_scene(id)
            utenti = self.partecipazioneScenaDAO.get_user_not_in_scene(id)

            # auxs name
            listenAddressAuxName = []
            for aux in auxs:
                auxAddress = [int(x,16) for x in aux.indirizzoMidiMain.split(",")]

                listenAddressAuxName.append(auxAddress + self.postName)
            
            listen = MidiListener(listenAddressAuxName, call_type.NAME)

            start = time.time()

            for address in listenAddressAuxName:
                self.midiController.request_value(address)

            while time.time() - start < 10:
                time.sleep(0.5)
                if listen.has_received_all():
                    break

            listen.stop()
            resultsValueAuxName = listen.get_results()
            
            resultsValueAuxSetName = []

            for aux in auxs:
                auxAddress = [int(x,16) for x in aux.indirizzoMidiMain.split(",")] 
                try:
                    resultsValueAuxSetName.append(resultsValueAuxName[tuple(auxAddress + self.postName)])
                except KeyError as k:
                    print("errore chiave ", k)
                    resultsValueAuxSetName.append("")

            auxs = list(zip(auxs, resultsValueAuxSetName))
        
            return self.templates.TemplateResponse(request, "update_scene.html", {"scene" : scene, "partecipanti" : partecipazioni, "users" : utenti, "auxs" : auxs })
        
        except Exception as e:
            print(f"Error retrieving scenes: {e}")
            return self.templates.TemplateResponse(request, "update_scene.html")

    def add_partecipante(self, request, adminUser, sceneId, user, aux):
        if self.utenteDAO.is_admin(adminUser) == False:
            return HTTPResponse(status_code=403, content="Non hai i permessi per accedere a questa risorsa")

        try:
            scene = self.sceneDAO.get_scene_by_id(sceneId)
            
            auxs = self.auxDAO.get_all_aux()
            utenti = self.partecipazioneScenaDAO.get_user_not_in_scene(sceneId)

            if user in [u.username for u in utenti] and aux in [a.id for a in auxs]:
                self.partecipazioneScenaDAO.add_participants(sceneId, user, aux)
                partecipazioni = self.partecipazioneScenaDAO.get_participants_scene(sceneId)

                utenti = self.partecipazioneScenaDAO.get_user_not_in_scene(sceneId)

                message = "utente assegnato con successo" 

                # create default layout for the user
                self.layoutCanaleDAO.add_default_layout_channel(user, sceneId)

            else:
                message ="utente ha già un aux assegnato"

            partecipazioni = self.partecipazioneScenaDAO.get_participants_scene(sceneId)

            # auxs name
            listenAddressAuxName = []
            for aux in auxs:
                auxAddress = [int(x,16) for x in aux.indirizzoMidi.split(",")]

                listenAddressAuxName.append(auxAddress + self.postName)
            
            listen = MidiListener(listenAddressAuxName, call_type.NAME)

            start = time.time()

            for address in listenAddressAuxName:
                self.midiController.request_value(address)

            while time.time() - start < 10:
                time.sleep(0.5)
                if listen.has_received_all():
                    break

            listen.stop()
            resultsValueAuxName = listen.get_results()
            
            resultsValueAuxSetName = []

            for aux in auxs:
                auxAddress = [int(x,16) for x in aux.indirizzoMidi.split(",")] 
                try:
                    resultsValueAuxSetName.append(resultsValueAuxName[tuple(auxAddress + self.postName)])
                except KeyError as k:
                    print("errore chiave ", k)
                    resultsValueAuxSetName.append("")

            auxs = list(zip(auxs, resultsValueAuxSetName))
            
            return self.templates.TemplateResponse(request, "update_scene.html", {"scene" : scene, "partecipanti" : partecipazioni, "users" : utenti, "auxs" : auxs, "message" : message })
        except Exception as e:
            print(f"Error retrieving scenes: {e}")
            return self.templates.TemplateResponse(request, "update_scene.html")

    def remove_partecipante(self, request, adminUser, sceneId, user, aux):
        if self.utenteDAO.is_admin(adminUser) == False:
            return HTTPResponse(status_code=403, content="Non hai i permessi per accedere a questa risorsa")

        try:
            scene = self.sceneDAO.get_scene_by_id(sceneId)

            partecipazioni = self.partecipazioneScenaDAO.get_participants_scene(sceneId)
            auxs = self.auxDAO.get_all_aux()

            partecipazioni = list(partecipazioni)

            if user in [u.utenteUsername for u in partecipazioni] and aux in [a.aux_id for a in partecipazioni]:
                self.partecipazioneScenaDAO.remove_participants(sceneId, user, aux)

                partecipazioni = self.partecipazioneScenaDAO.get_participants_scene(sceneId)
                utenti = self.partecipazioneScenaDAO.get_user_not_in_scene(sceneId)

                message = "utente rimosso con successo" 
            else:
                message ="utente non ha una precedente assegnazione"

            utenti = self.partecipazioneScenaDAO.get_user_not_in_scene(sceneId)

            # auxs name
            listenAddressAuxName = []
            for aux in auxs:
                auxAddress = [int(x,16) for x in aux.indirizzoMidi.split(",")]

                listenAddressAuxName.append(auxAddress + self.postName)
            
            listen = MidiListener(listenAddressAuxName, call_type.NAME)

            start = time.time()

            for address in listenAddressAuxName:
                self.midiController.request_value(address)

            while time.time() - start < 10:
                time.sleep(0.5)
                if listen.has_received_all():
                    break

            listen.stop()
            resultsValueAuxName = listen.get_results()
            
            resultsValueAuxSetName = []

            for aux in auxs:
                auxAddress = [int(x,16) for x in aux.indirizzoMidi.split(",")] 
                try:
                    resultsValueAuxSetName.append(resultsValueAuxName[tuple(auxAddress + self.postName)])
                except KeyError as k:
                    print("errore chiave ", k)
                    resultsValueAuxSetName.append("")

            auxs = list(zip(auxs, resultsValueAuxSetName))
            
            return self.templates.TemplateResponse(request, "update_scene.html", {"scene" : scene, "partecipanti" : partecipazioni, "users" : utenti, "auxs" : auxs, "message" : message })
        except Exception as e:
            print(f"Error retrieving scenes: {e}")
            return self.templates.TemplateResponse(request, "update_scene.html")


    def get_all_scene(self, adminUser):
        if self.utenteDAO.is_admin(adminUser) == False:
            return HTTPResponse(status_code=403, content="Non hai i permessi per accedere a questa risorsa")

        try:
            scenes = self.sceneDAO.get_all_scenes()
            return scenes
        except Exception as e:
            print(f"Error retrieving all scenes: {e}")
            return None

    def delete_scene(self, request, adminUser, sceneId):
        if self.utenteDAO.is_admin(adminUser) == False:
            return HTTPResponse(status_code=403, content="Non hai i permessi per accedere a questa risorsa")

        try:
            scenes = self.sceneDAO.delete_scene(sceneId)
            return RedirectResponse(url="/admin/manageScene", status_code=303)
            
        except Exception as e:
            print(f"Error retrieving all scenes: {e}")
            return None

    def update_scene(self, adminUser, id, nome, descrizione):

        if self.utenteDAO.is_admin(adminUser) == False:
            return HTTPResponse(status_code=403, content="Non hai i permessi per accedere a questa risorsa")

        try:
            scene = self.sceneDAO.updateScene(id, nome, descrizione)
            return scene != None
        except Exception as e:
            print(f"Error updating scene: {e}")
            return False
        

    def get_all_user_scene(self, username, request):
        try:
            scenes = self.sceneDAO.get_all_user_scene(username)

            templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "view", "user"))
            
            

            return templates.TemplateResponse("scenes.html",
                {"request": request, "scenes": scenes}
            )

        except Exception as e:
            print(f"Error retrieving all user scenes: {e}")
            return None