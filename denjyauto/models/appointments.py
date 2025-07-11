from sqlalchemy import Column, Integer, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import date
from denjyauto.models.base import Base

class Appointment(Base):
    __tablename__ = "appointment"

    id = Column(Integer, primary_key=True)
    date = Column(Date, default=date.today)
    hour = Column(String, default="00:00")
    car_id = Column(Integer, ForeignKey("car.id"))

    car = relationship("Car", back_populates="appointments")