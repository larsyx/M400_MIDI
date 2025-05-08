from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, foreign


from .base import Base


class Canale(Base):
    __tablename__ = 'canale'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    descrizione = Column(String, nullable = True)
    indirizzoMidi = Column(String, nullable=False)

    layoutCanale = relationship("LayoutCanale", back_populates="canale")