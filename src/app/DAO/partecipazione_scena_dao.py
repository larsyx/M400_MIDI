
from Database.database import DBSession
from Models.aux_ import Aux
from Models.partecipazioneScena import PartecipazioneScena


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