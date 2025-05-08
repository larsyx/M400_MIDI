

from sqlalchemy import desc, exists
from Database.database import DBSession
from Models.canale import Canale
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
            ).order_by(LayoutCanale.posizione).all()
            return layout
        except Exception as e:
            print(f"Error retrieving layout: {e}")
            return None
       
        
    def setLayoutCanale(self, user, scene, canale, posizione, descrizione, isBatteria):
        try:
            layout = self.getLayoutCanaleById(user, scene, canale)
            layout.descrizione = descrizione
            layout.posizione = posizione
            layout.isBatteria = isBatteria

            self.db.add(layout)
            self.db.commit()

            return layout
        except Exception as e:
            print(f"Error retrieving layout: {e}")
            return None
        
    def addLayoutCanale(self, user, scene, canale, descrizione):
        try: 
            layout = self.db.query(LayoutCanale).filter(
                LayoutCanale.user == user,
                LayoutCanale.scenaId == scene
            ).order_by(desc(LayoutCanale.posizione)).first()
            posizione=0
            if(layout):
                posizione = layout.posizione +1

            layout = LayoutCanale(
                scenaId=scene,
                canaleId=canale,
                user=user,
                posizione=posizione,
                descrizione=descrizione
            )

            self.db.add(layout)
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error retrieving layout: {e}")
            return None
        
    def removeLayoutCanale(self, user, scene, canale):
        try:
            channelToRemove = self.getLayoutCanaleById(user, scene, canale)

            updateChannel = self.db.query(LayoutCanale).filter(
                    LayoutCanale.user == user,
                    LayoutCanale.scenaId == scene,
                    LayoutCanale.posizione > channelToRemove.posizione
            ).all()

            for channel in updateChannel:
                self.setLayoutCanale(user,scene,channel.canaleId, channel.posizione-1, channel.descrizione)

            self.db.delete(channelToRemove)
            self.db.commit()
            return True
        
        except Exception as e:
            print(f"Error retrieving layout: {e}")
            return None