import tkinter as tk
from tkinter import ttk
from sqlalchemy.orm import Session
from denjyauto.database import SessionLocal
from denjyauto.forms.new_client_form import NewClientForm
from denjyauto.models.client import Client
from denjyauto.models.car import Car
from denjyauto.ui.widgets import clear_content
from denjyauto.ui.car_ui import add_new_car_to_client, show_car_details


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
                command=lambda cl=client: edit_client_notes(master, cl.name, cl.client_notes,
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
                               command=lambda c=car: show_car_details(master, c, client_name)).pack(side="left",
                                                                                                     padx=5, pady=2)

    finally:
        session.close()


def edit_client_notes(master, client_name, client_notes, save_callback):
    win = tk.Toplevel(master)
    win.title(f"Бележки към клиент {client_name}")
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

def show_client_details(master, content_frame, client):
    load_clients(master, content_frame)

    client_frame = ttk.LabelFrame(content_frame, text=f"{client.name}", padding=10)
    client_frame.pack(fill="x", pady=5)

    ttk.Label(client_frame, text=f"Име: {client.name}").pack(padx=10, pady=5)
    ttk.Label(client_frame, text=f"Телефон: {client.phone_number}").pack(padx=10, pady=5)
