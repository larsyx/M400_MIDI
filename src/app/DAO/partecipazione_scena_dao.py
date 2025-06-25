from Database.database import DBSession
from models.aux_ import Aux
from models.partecipazioneScena import PartecipazioneScena
from models.utente import RuoloUtente, Utente


class PartecipazioneScenaDAO:
    def __init__(self):
        self.db = DBSession.get()

    def get_aux_user(self, userID, scenaID):
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
        
    def get_participants_scene(self, sceneId):
        try:
            partecipanti = self.db.query(PartecipazioneScena).filter(PartecipazioneScena.scenaId == sceneId)
            return partecipanti
        
        except Exception as e:
            print(f"Error get partecipant for user: {e}")
            return None
        
    def get_aux_not_in_scene(self, scenaID):
        try:
            subquery = self.db.query(PartecipazioneScena.aux_id).filter(PartecipazioneScena.scenaId == scenaID)
            aux = self.db.query(Aux).filter(Aux.id.not_in(subquery))
            return aux
        except Exception as e:
            print(f"Error get partecipant for user: {e}")
            return None
        
    def get_user_not_in_scene(self, scenaID):
        try:
            subquery = self.db.query(PartecipazioneScena.utenteUsername).filter(PartecipazioneScena.scenaId == scenaID)
            users = self.db.query(Utente).filter(Utente.username.not_in(subquery), Utente.ruolo == RuoloUtente.utente).order_by(Utente.nome.asc())
            return users
        except Exception as e:
            print(f"Error get partecipant for user: {e}")
            return None
        
    def add_participants(self, sceneId, User, aux):
        try:
            partecipazione = PartecipazioneScena(scenaId = sceneId, utenteUsername = User, aux_id = aux)
            self.db.add(partecipazione)
            self.db.commit()
            return partecipazione
        except Exception as e:
            print(f"Error add for user: {e}")
            return None
        
    def remove_participants(self, sceneId, user, aux):
        try:
            partecipazione = self.db.query(PartecipazioneScena).filter(PartecipazioneScena.scenaId == sceneId, PartecipazioneScena.aux_id == aux, PartecipazioneScena.utenteUsername == user).first()

            self.db.delete(partecipazione)
            self.db.commit()
            return partecipazione
        except Exception as e:
            print(f"Error add for user: {e}")
            return None

    def change_aux_user(self, sceneId, user, aux):


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