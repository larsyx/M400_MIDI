from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

from Models.dca import DCA

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
    Aux(id=1, nome="Aux 1", indirizzoMidi="0x01, 0x02", indirizzoMidiMain="0x05, 0x00, 0x00, 0x0E"),
    Aux(id=2, nome="Aux 2", indirizzoMidi="0x01, 0x0A", indirizzoMidiMain="0x05, 0x01, 0x00, 0x0E"),
    Aux(id=3, nome="Aux 3", indirizzoMidi="0x01, 0x12", indirizzoMidiMain="0x05, 0x02, 0x00, 0x0E"),
    Aux(id=4, nome="Aux 4", indirizzoMidi="0x01, 0x1A", indirizzoMidiMain="0x05, 0x03, 0x00, 0x0E"),
    Aux(id=5, nome="Aux 5", indirizzoMidi="0x01, 0x22", indirizzoMidiMain="0x05, 0x04, 0x00, 0x0E"),
    Aux(id=6, nome="Aux 6", indirizzoMidi="0x01, 0x2A", indirizzoMidiMain="0x05, 0x05, 0x00, 0x0E"),
    Aux(id=7, nome="Aux 7", indirizzoMidi="0x01, 0x32", indirizzoMidiMain="0x05, 0x06, 0x00, 0x0E"),
    Aux(id=8, nome="Aux 8", indirizzoMidi="0x01, 0x3A", indirizzoMidiMain="0x05, 0x07, 0x00, 0x0E"),
    Aux(id=9, nome="Aux 9", indirizzoMidi="0x01, 0x42", indirizzoMidiMain="0x05, 0x08, 0x00, 0x0E"),
    Aux(id=10, nome="Aux 10", indirizzoMidi="0x01, 0x4A", indirizzoMidiMain="0x05, 0x09, 0x00, 0x0E"),
    Aux(id=11, nome="Aux 11", indirizzoMidi="0x01, 0x52", indirizzoMidiMain="0x05, 0x0A, 0x00, 0x0E"),
    Aux(id=12, nome="Aux 12", indirizzoMidi="0x01, 0x5A", indirizzoMidiMain="0x05, 0x0B, 0x00, 0x0E"),
    Aux(id=13, nome="Aux 13", indirizzoMidi="0x01, 0x62", indirizzoMidiMain="0x05, 0x0C, 0x00, 0x0E"),
    Aux(id=14, nome="Aux 14", indirizzoMidi="0x01, 0x6A", indirizzoMidiMain="0x05, 0x0D, 0x00, 0x0E"),
    Aux(id=15, nome="Aux 15", indirizzoMidi="0x01, 0x72", indirizzoMidiMain="0x05, 0x0E, 0x00, 0x0E"),
    Aux(id=16, nome="Aux 16", indirizzoMidi="0x01, 0x7A", indirizzoMidiMain="0x05, 0x0F, 0x00, 0x0E"),
]

canali = [
    Canale(id=i, nome=f"CH{i}", indirizzoMidi=f"0x03, 0x{hex(i - 1)[2:].zfill(2).upper()}")
    for i in range(1, 49)
]

canali[0].descrizione = "Fisarmonica/basso"
canali[1].descrizione = "Gtr Gab"
canali[2].descrizione = "Gtr Gio"
canali[3].descrizione = "Gtr Samu"
canali[4].descrizione = "Piano L"
canali[5].descrizione = "Piano R"
canali[6].descrizione = "Piano Don"
canali[7].descrizione = "Sax"
canali[9].descrizione = "Vox 1"
canali[10].descrizione = "Vox 2"
canali[11].descrizione = "Vox 3"
canali[12].descrizione = "Vox 4"
canali[13].descrizione = "Vox 5"
canali[14].descrizione = "Vox 6"
canali[16].descrizione = "Mac L"
canali[17].descrizione = "Mac R"
canali[20].descrizione = "Shure"
canali[21].descrizione = "Pulputo"
canali[24].descrizione = "Kick"
canali[25].descrizione = "SN up" 
canali[26].descrizione = "SN dw"
canali[27].descrizione = "HH"
canali[28].descrizione = "Tom"
canali[29].descrizione = "Tom"
canali[30].descrizione = "Floor Tom"
canali[31].descrizione = "OH L"
canali[32].descrizione = "OH R"

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

utente = Utente(username="admin", nome="admin", ruolo="amministratore")
utente1 = Utente(username="Thomas", nome="Thomas", ruolo="mixerista")

musicisti_giovani = [
    Utente(username="Gabri", nome="Gabriele", ruolo="utente"),
    Utente(username="Gionathan", nome="Gionathan", ruolo="utente"),
    Utente(username="Donato", nome = "Donato", ruolo="utente"),
    Utente(username="Irene", nome="Irene", ruolo="utente"),
    Utente(username="Samuel", nome="Samuel", ruolo="utente"),
    Utente(username="Lucrezia", nome="Lucrezia", ruolo="utente"),
    Utente(username="Christian", nome="Christian", ruolo="utente"),
    Utente(username="Andrea", nome="Andrea", ruolo="utente")
]

cantanti_giovani = [
    Utente(username="Denise", nome = "Denise", ruolo="utente"),
    Utente(username="Maria", nome = "Maria", ruolo="utente"),
    Utente(username="Manuel", nome = "Manuel", ruolo="utente"),
    Utente(username="Martina", nome = "Martina", ruolo="utente"),
    Utente(username="Giusy", nome = "Giusy", ruolo="utente"),
    Utente(username="Vanessa", nome = "Vanessa", ruolo="utente")
]

scena = Scena(id = 0, nome="Domenica", descrizione="scena della domenica")

partecipazione_dom = []

partecipazione_dom.append(PartecipazioneScena(
        scenaId=scena.id,
        utenteUsername=musicisti_giovani[0].username,
        aux_id=aux[13].id,
    ))

partecipazione_dom.append(PartecipazioneScena(
        scenaId=scena.id,
        utenteUsername=musicisti_giovani[1].username,
        aux_id=aux[0].id,
    ))

partecipazione_dom.append(PartecipazioneScena(
        scenaId=scena.id,
        utenteUsername=musicisti_giovani[2].username,
        aux_id=aux[0].id,
    ))

scena2 = Scena(id=1, nome="Giovani", descrizione="Scena gruppo Giovani Fiamme" )


partecipazione_musicisti = []

for user in musicisti_giovani:
    partecipazione_musicisti.append(PartecipazioneScena(
        scenaId=scena2.id,
        utenteUsername=user.username,
        aux_id=aux[1].id,
    ))

partecipazione_musicisti[0].aux_id=aux[13].id  #gab
partecipazione_musicisti[1].aux_id=aux[1].id   #gion
partecipazione_musicisti[2].aux_id=aux[5].id  #don
partecipazione_musicisti[3].aux_id=aux[10].id  #irene
partecipazione_musicisti[4].aux_id=aux[11].id  #samu
partecipazione_musicisti[5].aux_id=aux[12].id  #luc
partecipazione_musicisti[6].aux_id=aux[6].id  #christian
partecipazione_musicisti[7].aux_id=aux[0].id  #andrea


partecipazione_cantanti = []

for user in cantanti_giovani:
    partecipazione_cantanti.append(PartecipazioneScena(
        scenaId=scena2.id,
        utenteUsername=user.username,
        aux_id=aux[1].id,
    ))

partecipazione_cantanti[0].aux_id=aux[3].id  #Deni
partecipazione_cantanti[1].aux_id=aux[2].id  #Maria
partecipazione_cantanti[2].aux_id=aux[2].id  #Manu
partecipazione_cantanti[3].aux_id=aux[2].id  #Martina
partecipazione_cantanti[4].aux_id=aux[3].id  #Giusy
partecipazione_cantanti[5].aux_id=aux[3].id  #Vane


session.add_all(aux)
session.add_all(canali)
session.add(utente)
session.add(utente1)
session.add_all(musicisti_giovani)
session.add_all(cantanti_giovani)
session.add(scena)
session.add_all(partecipazione_dom)
session.add(scena2)
session.add_all(partecipazione_musicisti)
session.add_all(partecipazione_cantanti)
session.add_all(dca)
session.commit()

session.close()