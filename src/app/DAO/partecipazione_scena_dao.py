from Database.database import DBSession
from Models.aux_ import Aux
from Models.partecipazioneScena import PartecipazioneScena
from Models.utente import RuoloUtente, Utente


class PartecipazioneScenaDAO:
    def __init__(self):
        self.db = DBSession.get()

    def getAuxUser(self, userID, scenaID):
        try:
            partecipazione = (
                self.db.query(PartecipazioneScena)
                .filter(
                    PartecipazioneScena.utenteUsername == userID,
                    PartecipazioneScena.scenaId == scenaID,
                )
                .first()
            )

            if partecipazione:
                aux = self.db.query(Aux).filter(partecipazione.aux_id == Aux.id).first()
                return aux if aux else None
            return None
        except Exception as e:
            print(f"Error retrieving aux for user: {e}")
            return None
        
    def getPartecipantiScene(self, sceneId):
        try:
            partecipanti = self.db.query(PartecipazioneScena).filter(PartecipazioneScena.scenaId == sceneId)
            return partecipanti
        
        except Exception as e:
            print(f"Error get partecipant for user: {e}")
            return None
        
    def getAuxNotInScene(self, scenaID):
        try:
            subquery = self.db.query(PartecipazioneScena.aux_id).filter(PartecipazioneScena.scenaId == scenaID)
            aux = self.db.query(Aux).filter(Aux.id.not_in(subquery))
            return aux
        except Exception as e:
            print(f"Error get partecipant for user: {e}")
            return None
        
    def getUserNotInScene(self, scenaID):
        try:
            subquery = self.db.query(PartecipazioneScena.utenteUsername).filter(PartecipazioneScena.scenaId == scenaID)
            users = self.db.query(Utente).filter(Utente.username.not_in(subquery), Utente.ruolo == RuoloUtente.utente).order_by(Utente.nome.asc())
            return users
        except Exception as e:
            print(f"Error get partecipant for user: {e}")
            return None
        
    def addPartecipazione(self, sceneId, User, aux):
        try:
            partecipazione = PartecipazioneScena(scenaId = sceneId, utenteUsername = User, aux_id = aux)
            self.db.add(partecipazione)
            self.db.commit()
            return partecipazione
        except Exception as e:
            print(f"Error add for user: {e}")
            return None
        
    def removePartecipazione(self, sceneId, user, aux):
        try:
            partecipazione = self.db.query(PartecipazioneScena).filter(PartecipazioneScena.scenaId == sceneId, PartecipazioneScena.aux_id == aux, PartecipazioneScena.utenteUsername == user).first()

            self.db.delete(partecipazione)
            self.db.commit()
            return partecipazione
        except Exception as e:
            print(f"Error add for user: {e}")
            return None

    def changeAuxUser(self, sceneId, user, aux):


        partecipante = self.db.query(PartecipazioneScena).filter(
            PartecipazioneScena.utenteUsername == user,
            PartecipazioneScena.scenaId == int(sceneId)
        ).first()

        auxObj = self.db.query(Aux).filter(
            Aux.id == aux
        ).first()

        if partecipante and aux:
            partecipante.aux_id = aux

            self.db.commit()