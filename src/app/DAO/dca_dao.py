

from Database.database import DBSession
from Models.dca import DCA


class DCA_DAO:

    def __init__(self):
        self.db = DBSession.get()

    def get_dca(self):
        return self.db.query(DCA).all()
        
    def get_dca_by_id(self, dca_id):
        return self.db.query(DCA).filter(DCA.id == dca_id).first()
    
    def edit_dca(self,dca_id, descrizione):
        dca = self.get_dca_by_id(dca_id)
        if dca:
            dca.descrizione = descrizione
            self.db.commit()
            return dca
        
    def get_dca_by_address(self, address):
        return self.db.query(DCA).filter(DCA.indirizzoMidiFader == address).first()
    
    def get_dca_by_address_switch(self, address):
        return self.db.query(DCA).filter(DCA.indirizzoMidiSwitch == address).first()