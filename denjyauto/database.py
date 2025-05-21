from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from denjyauto.models.base import Base
from denjyauto.models.client import Client
from denjyauto.models.car import Car

DB_PATH = "sqlite:///db.sqlite3"
engine = create_engine(DB_PATH, echo=False)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def add_car_to_client(client_id, license_plate, vin, brand, model, year):
    session = SessionLocal()
    try:
        car = Car(
            client_id=client_id,
            registration_number=license_plate.upper(),
            vin=vin.upper(),
            brand=brand.capitalize(),
            model=model.capitalize(),
            year=year
        )
        session.add(car)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Грешка при добавяне на кола: {e}")
    finally:
        session.close()


def get_all_clients():
    session = SessionLocal()
    try:
        clients = session.query(Client).all()
        clients_list = [(client.id, client.name) for client in clients]
        print(clients_list)
        return clients_list
    finally:
        session.close()
