from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base import Base

class Aux(Base):
    __tablename__ = 'aux'

    id = Column(String, primary_key=True)
    nome = Column(String, nullable=False)
    indirizzoMidi = Column(String, nullable=False)

    partecipazioneScena = relationship("PartecipazioneScena", back_populates="aux")
