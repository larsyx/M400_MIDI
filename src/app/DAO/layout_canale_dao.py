

from Database.database import DBSession
from Models.layoutCanale import LayoutCanale


class LayoutCanaleDAO:

    def __init__(self):
        self.db = DBSession.get()
        
    def getLayoutCanaleById(self, user, scene, canale):
        try:
            layout = self.db.query(LayoutCanale).filter(
                LayoutCanale.user == user,
                LayoutCanale.scenaId == scene,
                LayoutCanale.canaleId == canale
            ).first()
            return layout
        except Exception as e:
            print(f"Error retrieving layout: {e}")
            return None
        

    def getLayoutCanale(self, user, scene):
        try:
            layout = self.db.query(LayoutCanale).filter(
                LayoutCanale.user == user,
                LayoutCanale.scenaId == scene
            ).all()
            return layout
        except Exception as e:
            print(f"Error retrieving layout: {e}")
            return None
       
        
    def setLayoutCanale(self, user, scene, canale, posizione, descrizione):
        try:
            layout = self.getLayoutCanaleById(user, scene, canale)
            layout.descrizione = descrizione
            layout.posizione = posizione

            self.db.add(layout)
            self.db.commit()

            return layout
        except Exception as e:
            print(f"Error retrieving layout: {e}")
            return None