import tkinter as tk
from tkinter import ttk
from sqlalchemy.orm import Session
from denjyauto.database import SessionLocal
from denjyauto.forms.add_car_form import AddCarForm
from denjyauto.forms.add_repair_form import AddRepairForm
from denjyauto.models.repair import Repair
from denjyauto.ui.widgets import create_copyable_label, create_scrollable_frame

def add_new_car_to_client(master, client):
    AddCarForm(master, client)

def show_car_details(master, car, client_name):

    win = tk.Toplevel(master)
    win.title(f"Клиент: {client_name}, кола: {car.registration_number}")
    win.configure(background="#111")

    ttk.Button(win, text="Добави ремонт", command=lambda: AddRepairForm(win, car)).pack(
        anchor="nw",
        pady=10
    )

    create_copyable_label(win, text=f"Рег. номер: {car.registration_number}")
    create_copyable_label(win, f"VIN: {car.vin}")
    create_copyable_label(win, text=f"Марка: {car.brand}")
    create_copyable_label(win, text=f"Година: {car.year}")

    repairs_frame = create_scrollable_frame(win)

    session: Session = SessionLocal()
    try:
        repairs = session.query(Repair).filter_by(car_id=car.id).all()
        if not repairs:
            ttk.Label(repairs_frame, text="Няма регистрирани ремонти.").grid(row=0, column=0, sticky="w")
        else:
            for i, repair in enumerate(repairs):
                row = i // 5
                column = i % 5
                ttk.Button(
                    repairs_frame,
                    text=f"Ремонт: {repair.repair_date}",
                    command=lambda r=repair: show_repair_details(master, r)
                ).grid(row=row, column=column, padx=5, pady=5, sticky="w")
    finally:
        session.close()


def show_repair_details(master, repair):
    win = tk.Toplevel(master)
    win.configure(bg="#111")
    win.title(f"Дата на ремонта: {repair.repair_date}")
    ttk.Label(win, text=f"Километри при ремонта: {repair.repair_km}").pack(padx=10, pady=5)
    ttk.Label(win, text=f"Ремонти: {repair.repairs_type_field}").pack(padx=10, pady=5)
    ttk.Label(win, text=f"Бележки към ремонта: {repair.repair_notes}").pack(padx=10, pady=5)
    ttk.Label(win, text=f"Цена на ремонта: {repair.repair_price}").pack(padx=10, pady=5)
