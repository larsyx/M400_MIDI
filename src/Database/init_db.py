from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.base import Base
from models.aux_ import Aux
from models.canale import Canale
from models.utente import Utente
from models.partecipazioneScena import PartecipazioneScena
from models.scena import Scena
from models.layoutCanale import LayoutCanale
from models.dca import DCA

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
    Aux(id=1, nome="Aux 1", indirizzoMidi="0x01, 0x02", indirizzoMidiMain="0x05, 0x00"),
    Aux(id=2, nome="Aux 2", indirizzoMidi="0x01, 0x0A", indirizzoMidiMain="0x05, 0x01"),
    Aux(id=3, nome="Aux 3", indirizzoMidi="0x01, 0x12", indirizzoMidiMain="0x05, 0x02"),
    Aux(id=4, nome="Aux 4", indirizzoMidi="0x01, 0x1A", indirizzoMidiMain="0x05, 0x03"),
    Aux(id=5, nome="Aux 5", indirizzoMidi="0x01, 0x22", indirizzoMidiMain="0x05, 0x04"),
    Aux(id=6, nome="Aux 6", indirizzoMidi="0x01, 0x2A", indirizzoMidiMain="0x05, 0x05"),
    Aux(id=7, nome="Aux 7", indirizzoMidi="0x01, 0x32", indirizzoMidiMain="0x05, 0x06"),
    Aux(id=8, nome="Aux 8", indirizzoMidi="0x01, 0x3A", indirizzoMidiMain="0x05, 0x07"),
    Aux(id=9, nome="Aux 9", indirizzoMidi="0x01, 0x42", indirizzoMidiMain="0x05, 0x08"),
    Aux(id=10, nome="Aux 10", indirizzoMidi="0x01, 0x4A", indirizzoMidiMain="0x05, 0x09"),
    Aux(id=11, nome="Aux 11", indirizzoMidi="0x01, 0x52", indirizzoMidiMain="0x05, 0x0A"),
    Aux(id=12, nome="Aux 12", indirizzoMidi="0x01, 0x5A", indirizzoMidiMain="0x05, 0x0B"),
    Aux(id=13, nome="Aux 13", indirizzoMidi="0x01, 0x62", indirizzoMidiMain="0x05, 0x0C"),
    Aux(id=14, nome="Aux 14", indirizzoMidi="0x01, 0x6A", indirizzoMidiMain="0x05, 0x0D"),
    Aux(id=15, nome="Aux 15", indirizzoMidi="0x01, 0x72", indirizzoMidiMain="0x05, 0x0E"),
    Aux(id=16, nome="Aux 16", indirizzoMidi="0x01, 0x7A", indirizzoMidiMain="0x05, 0x0F"),
]

canali = [
    Canale(id=i, nome=f"CH{i}", indirizzoMidi=f"0x03, 0x{hex(i - 1)[2:].zfill(2).upper()}")
    for i in range(1, 49)
]


dca = [
    DCA(id=1, nome="DCA 1", descrizione="DCA 1", indirizzoMidiFader="0x09, 0x00, 0x00, 0x0A", indirizzoMidiSwitch="0x09, 0x00, 0x00, 0x08"),
    DCA(id=2, nome="DCA 2", descrizione="DCA 2", indirizzoMidiFader="0x09, 0x01, 0x00, 0x0A", indirizzoMidiSwitch="0x09, 0x01, 0x00, 0x08"),
    DCA(id=3, nome="DCA 3", descrizione="DCA 3", indirizzoMidiFader="0x09, 0x02, 0x00, 0x0A", indirizzoMidiSwitch="0x09, 0x02, 0x00, 0x08"),
    DCA(id=4, nome="DCA 4", descrizione="DCA 4", indirizzoMidiFader="0x09, 0x03, 0x00, 0x0A", indirizzoMidiSwitch="0x09, 0x03, 0x00, 0x08"),
    DCA(id=5, nome="DCA 5", descrizione="DCA 5", indirizzoMidiFader="0x09, 0x04, 0x00, 0x0A", indirizzoMidiSwitch="0x09, 0x04, 0x00, 0x08"),
    DCA(id=6, nome="DCA 6", descrizione="DCA 6", indirizzoMidiFader="0x09, 0x05, 0x00, 0x0A", indirizzoMidiSwitch="0x09, 0x05, 0x00, 0x08"),
    DCA(id=7, nome="DCA 7", descrizione="DCA 7", indirizzoMidiFader="0x09, 0x06, 0x00, 0x0A", indirizzoMidiSwitch="0x09, 0x06, 0x00, 0x08"),
    DCA(id=8, nome="DCA 8", descrizione="DCA 8", indirizzoMidiFader="0x09, 0x07, 0x00, 0x0A", indirizzoMidiSwitch="0x09, 0x07, 0x00, 0x08")
]


session.add_all(aux)
session.add_all(canali)

session.add_all(dca)
session.commit()

session.close()