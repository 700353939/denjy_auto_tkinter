from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from denjyauto.models.base import Base

class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    phone_number = Column(String(20), nullable=True)
    client_notes = Column(Text, nullable=True)

    cars = relationship("Car", back_populates="client")