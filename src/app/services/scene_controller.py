from http.client import HTTPResponse
import os

from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from app.DAO.scene_dao import SceneDAO
from app.DAO.user_dao import UserDAO

class SceneController:
    def __init__(self):
        self.sceneDAO = SceneDAO()
        self.utenteDAO = UserDAO()


    def create_scene(self, adminUser, nome, descrizione):
        if self.utenteDAO.isAdmin(adminUser) == False:
            return HTTPResponse(status_code=403, content="Non hai i permessi per accedere a questa risorsa")
        
        try:
            new_scene = self.sceneDAO.createScene(nome, descrizione)
            return new_scene != None
        except Exception as e:
            print(f"Error creating scene: {e}")
            return False


    def delete_scene(self, adminUser, id):
        if self.utenteDAO.isAdmin(adminUser) == False:
            return HTTPResponse(status_code=403, content="Non hai i permessi per accedere a questa risorsa")

        try:
            scene = self.sceneDAO.deleteScene(id)
            return scene != None
        except Exception as e:
            print(f"Error deleting scene: {e}")
            return False


    def get_scene(self, adminUser, id):
        if self.utenteDAO.isAdmin(adminUser) == False:
            return HTTPResponse(status_code=403, content="Non hai i permessi per accedere a questa risorsa")

        try:
            scenes = self.sceneDAO.getSceneById(id)
            return scenes
        except Exception as e:
            print(f"Error retrieving scenes: {e}")
            return None


    def get_all_scene(self, adminUser):
        if self.utenteDAO.isAdmin(adminUser) == False:
            return HTTPResponse(status_code=403, content="Non hai i permessi per accedere a questa risorsa")

        try:
            scenes = self.sceneDAO.getAllScenes()
            return scenes
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