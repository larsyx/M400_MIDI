from sqlalchemy import Column, String, Integer, ForeignKey, and_
from sqlalchemy.orm import relationship, foreign


from .base import Base

class PartecipazioneScena(Base):
    __tablename__ = 'partecipazione_scena'

    scenaId = Column(Integer, ForeignKey('scena.id'), primary_key=True)
    utenteUsername = Column(String, ForeignKey('utente.username'), primary_key=True)
    aux_id = Column(Integer, ForeignKey('aux.id'), nullable=False)

    scena = relationship("Scena", back_populates="partecipazioneScena")
    utente = relationship("Utente", back_populates="partecipazioneScena")
    aux = relationship("Aux", back_populates="partecipazioneScena")
    