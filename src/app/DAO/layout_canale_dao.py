from sqlalchemy import desc
from Database.database import DBSession
from Models.canale import Canale
from Models.layoutCanale import LayoutCanale
from app.DAO.channel_dao import ChannelDAO 
import json
import os


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
        
    def addLayoutCanale(self, user, scene, canale, descrizione, isBatteria=False):
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
                descrizione=descrizione,
                isBatteria=isBatteria
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
                self.setLayoutCanale(user,scene,channel.canaleId, channel.posizione-1, channel.descrizione, channel.isBatteria)

            self.db.delete(channelToRemove)
            self.db.commit()
            return True
        
        except Exception as e:
            print(f"Error retrieving layout: {e}")
            return None

    
    def addDefaultLayoutCanale(self, user, scene):
        file_path = os.path.join(os.path.dirname(__file__), "..", "..", "Database", "default_layout.json")
        with open(file_path, "r") as json_data:
            data = json.load(json_data)

            channels = set(ch['id'] for ch in data.get('channels', []))
            drums = set(d['id'] for d in data.get('drums', [])) - channels

            if self.getLayoutCanale(user, scene) is not None and len(self.getLayoutCanale(user, scene)) > 0:
                return True
            
            channelDAO = ChannelDAO()

            for channel in channels:
                channel_obj = channelDAO.get_channel_by_id(channel)
                if channel_obj is not None:
                    self.addLayoutCanale(user, scene, channel, channel_obj.descrizione, False)


            for drum in drums:
                channel_obj = channelDAO.get_channel_by_id(drum)
                if channel_obj is not None:
                    self.addLayoutCanale(user, scene, drum, channel_obj.descrizione, True)

