from Database.database import DBSession
from Models.aux_ import Aux


class AuxDAO:
    def __init__(self):
        self.db = DBSession.get()

    def getAllAux(self):
        try:
            aux = self.db.query(Aux).all()
            return aux
        except Exception as e:
            print(f"Error retrieving all aux: {e}")
            return None

    def getAuxById(self, id):
        try:
            aux = self.db.query(Aux).filter(Aux.id == id).first()
            return aux
        except Exception as e:
            print(f"Error retrieving aux by id: {e}")
            return None
        