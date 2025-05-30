from sqlalchemy import Column, Integer, Date, Text, ForeignKey, String, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import date
from denjyauto.models.base import Base

class Repair(Base):
    __tablename__ = "repair"

    id = Column(Integer, primary_key=True)
    repair_date = Column(Date, default=date.today)
    repair_km = Column(Integer, default=0)
    repairs_type_field = Column(String)  # MultiSelect симулация
    repair_price = Column(Float, default=0)
    repair_notes = Column(Text, nullable=True)
    is_it_paid = Column(Boolean, default=False)
    car_id = Column(Integer, ForeignKey("car.id"))

    car = relationship("Car", back_populates="repairs")
