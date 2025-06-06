from http.client import HTTPResponse
import os
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.DAO.aux_dao import AuxDAO
from app.DAO.partecipazione_scena_dao import PartecipazioneScenaDAO
from app.DAO.scene_dao import SceneDAO
from app.DAO.user_dao import UserDAO

class SceneController:
    def __init__(self):
        self.sceneDAO = SceneDAO()
        self.auxDAO = AuxDAO()
        self.utenteDAO = UserDAO()
        self.partecipazioneScenaDAO = PartecipazioneScenaDAO()
        self.templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "View", "administration"))

    def manageScene(self, request, adminUser):
        if self.utenteDAO.isAdmin(adminUser):
            scenes = self.sceneDAO.getAllScenes()
            return self.templates.TemplateResponse(request, "manageScene.html", {"scenes" : scenes, })
        
        else:    
            return HTMLResponse(status_code=403, content="Non hai i permessi per accedere a questa risorsa")

    def create_scene(self, request, adminUser, nome, descrizione):
        if self.utenteDAO.isAdmin(adminUser) == False:
            return HTTPResponse(status_code=403, content="Non hai i permessi per accedere a questa risorsa")
        
        scenes = self.sceneDAO.getAllScenes()

        try:
            new_scene = self.sceneDAO.createScene(nome, descrizione)
            scenes.append(new_scene)
            return self.templates.TemplateResponse(request, "manageScene.html", {"scenes" : scenes, "message" : f"scena {new_scene.nome} creata con successo" })
        except Exception as e:
            print(f"Error creating scene: {e}")
            return self.templates.TemplateResponse(request, "manageScene.html", {"scenes" : scenes, "message" : f"errore creazione scena {e}" })

    def get_scene(self, request, adminUser, id):
        if self.utenteDAO.isAdmin(adminUser) == False:
            return HTTPResponse(status_code=403, content="Non hai i permessi per accedere a questa risorsa")

        try:
            scene = self.sceneDAO.getSceneById(id)
            auxs = self.auxDAO.getAllAux()
            partecipazioni = self.partecipazioneScenaDAO.getPartecipantiScene(id)
            utenti = self.partecipazioneScenaDAO.getUserNotInScene(id)

            return self.templates.TemplateResponse(request, "updateScene.html", {"scene" : scene, "partecipanti" : partecipazioni, "users" : utenti, "auxs" : auxs })
        except Exception as e:
            print(f"Error retrieving scenes: {e}")
            return self.templates.TemplateResponse(request, "updateScene.html")

    def add_partecipante(self, request, adminUser, sceneId, user, aux):
        if self.utenteDAO.isAdmin(adminUser) == False:
            return HTTPResponse(status_code=403, content="Non hai i permessi per accedere a questa risorsa")

        try:
            scene = self.sceneDAO.getSceneById(sceneId)
            
            auxs = self.auxDAO.getAllAux()
            utenti = self.partecipazioneScenaDAO.getUserNotInScene(sceneId)

            if user in [u.username for u in utenti] and aux in [a.id for a in auxs]:
                self.partecipazioneScenaDAO.addPartecipazione(sceneId, user, aux)
                partecipazioni = self.partecipazioneScenaDAO.getPartecipantiScene(sceneId)

                utenti = self.partecipazioneScenaDAO.getUserNotInScene(sceneId)

                message = "utente assegnato con successo" 
            else:
                message ="utente ha già un aux assegnato"

            partecipazioni = self.partecipazioneScenaDAO.getPartecipantiScene(sceneId)
            
            return self.templates.TemplateResponse(request, "updateScene.html", {"scene" : scene, "partecipanti" : partecipazioni, "users" : utenti, "auxs" : auxs, "message" : message })
        except Exception as e:
            print(f"Error retrieving scenes: {e}")
            return self.templates.TemplateResponse(request, "updateScene.html")

    def remove_partecipante(self, request, adminUser, sceneId, user, aux):
        if self.utenteDAO.isAdmin(adminUser) == False:
            return HTTPResponse(status_code=403, content="Non hai i permessi per accedere a questa risorsa")

        try:
            scene = self.sceneDAO.getSceneById(sceneId)

            partecipazioni = self.partecipazioneScenaDAO.getPartecipantiScene(sceneId)
            auxs = self.auxDAO.getAllAux()

            partecipazioni = list(partecipazioni)

            if user in [u.utenteUsername for u in partecipazioni] and aux in [a.aux_id for a in partecipazioni]:
                self.partecipazioneScenaDAO.removePartecipazione(sceneId, user, aux)

                partecipazioni = self.partecipazioneScenaDAO.getPartecipantiScene(sceneId)
                utenti = self.partecipazioneScenaDAO.getUserNotInScene(sceneId)

                message = "utente rimosso con successo" 
            else:
                message ="utente non ha una precedente assegnazione"

            utenti = self.partecipazioneScenaDAO.getUserNotInScene(sceneId)
            
            return self.templates.TemplateResponse(request, "updateScene.html", {"scene" : scene, "partecipanti" : partecipazioni, "users" : utenti, "auxs" : auxs, "message" : message })
        except Exception as e:
            print(f"Error retrieving scenes: {e}")
            return self.templates.TemplateResponse(request, "updateScene.html")


    def get_all_scene(self, adminUser):
        if self.utenteDAO.isAdmin(adminUser) == False:
            return HTTPResponse(status_code=403, content="Non hai i permessi per accedere a questa risorsa")

        try:
            scenes = self.sceneDAO.getAllScenes()
            return scenes
        except Exception as e:
            print(f"Error retrieving all scenes: {e}")
            return None

    def delete_scene(self, request, adminUser, sceneId):
        if self.utenteDAO.isAdmin(adminUser) == False:
            return HTTPResponse(status_code=403, content="Non hai i permessi per accedere a questa risorsa")

        try:
            scenes = self.sceneDAO.deleteScene(sceneId)
            return RedirectResponse(url="/admin/manageScene", status_code=303)
            
        except Exception as e:
            print(f"Error retrieving all scenes: {e}")
            return None

    def update_scene(self, adminUser, id, nome, descrizione):

        if self.utenteDAO.isAdmin(adminUser) == False:
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

            templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "View", "user"))
            
            

            return templates.TemplateResponse("scenes.html",
                {"request": request, "scenes": scenes}
            )

        except Exception as e:
            print(f"Error retrieving all user scenes: {e}")
            return None