from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from denjyauto.models.base import Base

class Car(Base):
    __tablename__ = "car"

    id = Column(Integer, primary_key=True)
    registration_number = Column(String)
    lower_registration_number = Column(String)
    vin = Column(String, nullable=True)
    brand = Column(String, nullable=True)
    model = Column(String, nullable=True)
    year = Column(Integer, default=0)
    client_id = Column(Integer, ForeignKey("client.id"))

    client = relationship("Client", back_populates="cars")
    repairs = relationship("Repair", back_populates="car", cascade="all, delete")

