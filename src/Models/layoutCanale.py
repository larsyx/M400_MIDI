from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship


from .base import Base

class LayoutCanale(Base):
    __tablename__ = 'layout_canale'
    scenaId = Column(Integer, ForeignKey('scena.id', ondelete="CASCADE"), primary_key=True)
    canaleId = Column(Integer, ForeignKey('canale.id'), primary_key=True)
    user = Column(String, ForeignKey('utente.username', ondelete="CASCADE"), primary_key=True)

    posizione = Column(Integer, nullable=False)
    descrizione = Column(String, nullable=True)
    isBatteria = Column(Boolean, nullable=False, default = False)

    scena = relationship("Scena", back_populates="layoutCanale")
    canale = relationship("Canale", back_populates="layoutCanale")
    utente = relationship("Utente", back_populates="layoutCanale", passive_deletes=True)