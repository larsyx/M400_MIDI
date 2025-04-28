from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from .base import Base

class Scena(Base):
    __tablename__ = 'scena'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    descrizione = Column(String, nullable=True)

    partecipazioneScena = relationship("PartecipazioneScena", back_populates="scena")
    layoutCanale = relationship("LayoutCanale", back_populates="scena")