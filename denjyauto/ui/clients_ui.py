import tkinter as tk
from tkinter import ttk
from sqlalchemy.orm import Session
from denjyauto.database import SessionLocal
from denjyauto.forms.new_client_form import NewClientForm
from denjyauto.forms.add_car_form import AddCarForm
from denjyauto.models.client import Client
from denjyauto.models.car import Car
from denjyauto.forms.add_repair_form import AddRepairForm
from denjyauto.models.repair import Repair
from denjyauto.ui.widgets import create_copyable_label, create_scrollable_frame, clear_content


def load_clients(master, content_frame):
    clear_content(content_frame)
    session: Session = SessionLocal()

    try:
        clients = session.query(Client).all()
        for client in clients:
            client_name = client.name
            client_phone = client.phone_number

            client_frame = ttk.LabelFrame(content_frame,
                                          text=f"Име на клиента: {client_name}, телефон: {client_phone}", padding=10)
            client_frame.pack(fill="x", pady=5)

            ttk.Button(
                client_frame,
                text="Бележки за клиента",
                command=lambda cl=client: edit_client_notes(master,
                    cl.client_notes,
                    lambda updated: (save_client_note(cl.id, updated), load_clients(master, content_frame))
                )).pack(side="left", padx=20)

            ttk.Button(client_frame, text="Добави кола", command=lambda c=client: add_new_car_to_client(master, c)).pack(
                side="left", padx=20)

            cars = session.query(Car).filter_by(client_id=client.id).all()
            if not cars:
                ttk.Label(client_frame, text="Няма регистрирани коли.").pack(anchor="w", padx=20)
            else:
                for car in cars:
                    ttk.Button(client_frame, text=f"Колa: {car.registration_number}",
                               command=lambda c=car: show_car_details(master, content_frame, c, client_name)).pack(side="left",
                                                                                                     padx=5, pady=2)

    finally:
        session.close()


def edit_client_notes(master, client_notes, save_callback):
    win = tk.Toplevel(master)
    win.title("Бележки към клиента")
    win.geometry("400x300")

    ttk.Label(win, text="Редактирай бележката:").pack(padx=10, pady=5)

    text_widget = tk.Text(win, wrap="word", height=10)
    text_widget.pack(padx=10, pady=5, fill="both", expand=True)

    if client_notes:
        text_widget.insert("1.0", client_notes)

    def save_notes():
        updated_notes = text_widget.get("1.0", "end-1c")
        save_callback(updated_notes)
        win.destroy()

    ttk.Button(win, text="Запази", command=save_notes).pack(pady=10)


def save_client_note(client_id, updated_note):
    session = SessionLocal()
    try:
        client = session.query(Client).get(client_id)
        client.client_notes = updated_note
        session.commit()
    finally:
        session.close()


def open_new_client_form(master):
    NewClientForm(master)


def add_new_car_to_client(master, client):
    AddCarForm(master, client)


def show_client_details(master, content_frame, client):
    load_clients(master, content_frame)

    client_frame = ttk.LabelFrame(content_frame, text=f"{client.name}", padding=10)
    client_frame.pack(fill="x", pady=5)

    ttk.Label(client_frame, text=f"Име: {client.name}").pack(padx=10, pady=5)
    ttk.Label(client_frame, text=f"Телефон: {client.phone_number}").pack(padx=10, pady=5)


def show_car_details(master, content_frame, car, client_name):
    load_clients(master, content_frame)

    win = tk.Toplevel(master)
    win.title(f"Клиент: {client_name}, кола: {car.registration_number}")

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
    win.title(f"Дата на ремонта: {repair.repair_date}")
    ttk.Label(win, text=f"Километри при ремонта: {repair.repair_km}").pack(padx=10, pady=5)
    ttk.Label(win, text=f"Ремонти: {repair.repairs_type_field}").pack(padx=10, pady=5)
    ttk.Label(win, text=f"Бележки към ремонта: {repair.repair_notes}").pack(padx=10, pady=5)
    ttk.Label(win, text=f"Цена на ремонта: {repair.repair_price}").pack(padx=10, pady=5)