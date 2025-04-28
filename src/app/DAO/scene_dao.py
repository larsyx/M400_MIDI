
from Database.database import DBSession
from Models.scena import Scena


class SceneDAO:
    def __init__(self):
        self.db = DBSession.get()


    def getSceneById(self, id):
        try:
            scene = self.db.query(Scena).filter(Scena.id == id).first()
            return scene
        except Exception as e:
            print(f"Error retrieving scene: {e}")
            return None

    def getAllScenes(self):
        try:
            scenes = self.db.query(Scena).all()
            return scenes
        except Exception as e:
            print(f"Error retrieving scenes: {e}")
            return None


    def createScene(self, nome, descrizione):
        try:
            new_scene = Scena(nome=nome, descrizione=descrizione)
            self.db.add(new_scene)
            self.db.commit()
            return new_scene
        except Exception as e:
            print(f"Error creating scene: {e}")
            return None
        

    def updateScene(self, id, nome, descrizione):
        try:
            scene = self.getSceneById(id)
            if scene:
                scene.nome = nome
                scene.descrizione = descrizione
                self.db.commit()
                return scene
            else:
                return None
        except Exception as e:
            print(f"Error updating scene: {e}")
            return None
        
    
    def deleteScene(self, id):
        try:
            scene = self.getSceneById(id)
            if scene:
                self.db.delete(scene)
                self.db.commit()
                return scene
            else:
                return None
        except Exception as e:
            print(f"Error deleting scene: {e}")
            return None
        
    def get_all_user_scene(self, username):
        try:
            scenes = self.db.query(Scena).filter(Scena.partecipazioneScena.any(utenteUsername=username)).all()
            return scenes
        except Exception as e:
            print(f"Error retrieving user scenes: {e}")
            return None