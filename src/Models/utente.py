from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base import Base
from enum import Enum
from sqlalchemy import Enum as SQLEnum



class RuoloUtente(Enum):
    mixerista = "mixerista"
    utente = "utente"
    amministratore = "amministratore"
    video = "video"

class Utente(Base):
    __tablename__ = 'utente'
    username = Column(String, primary_key=True)
    nome = Column(String, nullable=False)
    ruolo = Column(SQLEnum(RuoloUtente), nullable=False)

    partecipazioneScena = relationship("PartecipazioneScena", back_populates="utente", cascade="all, delete-orphan", passive_deletes=True)
    layoutCanale = relationship("LayoutCanale", back_populates="utente", cascade="all, delete-orphan", passive_deletes=True)
    
