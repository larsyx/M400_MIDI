from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Models.base import Base
from Models.aux_ import Aux
from Models.canale import Canale
from Models.utente import Utente
from Models.partecipazioneScena import PartecipazioneScena
from Models.scena import Scena
from Models.layoutCanale import LayoutCanale

# Inizializzazione DB canali e aux

DATABASE_URL = "sqlite:///Database/database.db"
engine = create_engine(DATABASE_URL, echo=True)


# Creazione delle tabelle nel DB
Base.metadata.create_all(engine)


#Sessione
Session = sessionmaker(bind=engine)
session = Session()

# Inizializzazione
aux = [
    Aux(id=1, nome="Aux 1", indirizzoMidi="0x01, 0x02"),
    Aux(id=2, nome="Aux 2", indirizzoMidi="0x01, 0x0A"),
    Aux(id=3, nome="Aux 3", indirizzoMidi="0x01, 0x12"),
    Aux(id=4, nome="Aux 4", indirizzoMidi="0x01, 0x1A"),
    Aux(id=5, nome="Aux 5", indirizzoMidi="0x01, 0x22"),
    Aux(id=6, nome="Aux 6", indirizzoMidi="0x01, 0x2A"),
    Aux(id=7, nome="Aux 7", indirizzoMidi="0x01, 0x32"),
    Aux(id=8, nome="Aux 8", indirizzoMidi="0x01, 0x3A"),
    Aux(id=9, nome="Aux 9", indirizzoMidi="0x01, 0x42"),
    Aux(id=10, nome="Aux 10", indirizzoMidi="0x01, 0x4A"),
    Aux(id=11, nome="Aux 11", indirizzoMidi="0x01, 0x52"),
    Aux(id=12, nome="Aux 12", indirizzoMidi="0x01, 0x5A"),
    Aux(id=13, nome="Aux 13", indirizzoMidi="0x01, 0x62"),
    Aux(id=14, nome="Aux 14", indirizzoMidi="0x01, 0x6A"),
    Aux(id=15, nome="Aux 15", indirizzoMidi="0x01, 0x72"),
    Aux(id=16, nome="Aux 16", indirizzoMidi="0x01, 0x7A"),
]

canali = [
    Canale(id=i, nome=f"CH{i}", indirizzoMidi=f"0x03, 0x{hex(i - 1)[2:].zfill(2).upper()}")
    for i in range(1, 49)
]

utente = Utente(username="admin", nome="admin", ruolo="amministratore")
utente1 = Utente(username="Gabri", nome="Gabriele", ruolo="utente")

scena = Scena(id= 0, nome="Domenica", descrizione="scena della domenica")



partecipazione = PartecipazioneScena(
    scenaId=scena.id,
    utenteUsername=utente1.username,
    aux_id=aux[0].id,
)

layoutCanale = [
    LayoutCanale(
        scenaId=scena.id,
        canaleId=canali[i].id,
        user=utente1.username,
        posizione=i,
        descrizione=f"Descrizione canale {i + 1}",
    )
    for i in range(len(canali))
]


session.add_all(aux)
session.add_all(canali)
session.add(utente)
session.add(utente1)
session.add(scena)
session.add(partecipazione)
session.add_all(layoutCanale)
session.commit()

session.close()