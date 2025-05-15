from Database.database import DBSession
from Models.canale import Canale


class ChannelDAO:
    def __init__(self):
        self.db = DBSession.get()

    def get_all_channels(self):
         try:
            channels = self.db.query(Canale).all()
            return channels
         except Exception as e:
            print(f"Error retrieving all channels: {e}")
            return None

    def get_channel_by_id(self, channel_id):
        try:
            channel = self.db.query(Canale).filter(Canale.id == channel_id).first()
            return channel
        except Exception as e:
            print(f"Error retrieving all channels: {e}")
            return None

    def get_channel_address(self, channel_id):
        channel = self.get_channel_by_id(channel_id)

        return channel.indirizzoMidi if channel else None
    

    def get_channel_by_address(self, address):
        channel = self.db.query(Canale).filter(Canale.indirizzoMidi == address)[0]
        if channel:
            return channel
        else:
            return None