from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base import Base


class Canale(Base):
    __tablename__ = 'canale'

    id = Column(String, primary_key=True)
    nome = Column(String, nullable=False)
    indirizzoMidi = Column(String, nullable=False)

    partecipazioneScena = relationship("PartecipazioneScena", back_populates="canale")
