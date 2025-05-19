from sqlalchemy import Column, Integer, String
from Models.base import Base


class DCA(Base):
    __tablename__ = 'dca'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    descrizione = Column(String, nullable=True)
    indirizzoMidiFader = Column(String, nullable=False, unique=True)
    indirizzoMidiSwitch = Column(String, nullable=False, unique=True)

