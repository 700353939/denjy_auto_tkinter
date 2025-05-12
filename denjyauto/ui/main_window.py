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
from denjyauto.ui.widgets import create_copyable_label
from denjyauto.ui.widgets import create_scrollable_frame


class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("DenjyAuto")
        master.geometry("800x600")

        self.header = ttk.Label(master, text="Списък с клиенти", font=("Arial", 16))
        self.header.pack(pady=10)

        self.toolbar = ttk.Frame(master)
        self.toolbar.pack(pady=5)

        self.refresh_button = ttk.Button(self.toolbar, text="Обнови списъка", command=self.load_clients)
        self.refresh_button.grid(row=0, column=0, padx=5)

        self.new_client_button = ttk.Button(self.toolbar, text="Нов клиент", command=self.open_new_client_form)
        self.new_client_button.grid(row=0, column=1, padx=5)

        self.content_frame = create_scrollable_frame(master, scroll="vertical")

        self.load_clients()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def load_clients(self):
        self.clear_content()
        session: Session = SessionLocal()

        try:
            clients = session.query(Client).all()
            for client in clients:
                client_name = client.name
                client_phone = client.phone_number

                client_frame = ttk.LabelFrame(self.content_frame, text=f"Име на клиента: {client_name}, телефон: {client_phone}", padding=10)
                client_frame.pack(fill="x", pady=5)

                ttk.Button(
                    client_frame,
                    text="Бележки за клиента",
                    command=lambda cl=client: self.client_notes(
                        cl.client_notes,
                        lambda updated: (self.save_client_note(cl.id, updated), self.load_clients())
                    )).pack(side="left", padx=20)

                ttk.Button(client_frame, text="Добави кола", command=lambda c=client: self.add_new_car_to_client(c)).pack(side="left", padx=20)

                cars = session.query(Car).filter_by(client_id=client.id).all()
                if not cars:
                    ttk.Label(client_frame, text="Няма регистрирани коли.").pack(anchor="w", padx=20)
                else:
                    for car in cars:
                        ttk.Button(client_frame, text=f"Колa: {car.registration_number}",
                                   command=lambda car=car: self.show_car_details(car, client_name)).pack(side="left", padx=5, pady=2)

        finally:
            session.close()

    def client_notes(self, client_notes, save_callback):
        win = tk.Toplevel(self.master)
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

    def save_client_note(self, client_id, updated_note):
        session = SessionLocal()
        try:
            client = session.query(Client).get(client_id)
            client.client_notes = updated_note
            session.commit()
        finally:
            session.close()

    def open_new_client_form(self):
        NewClientForm(self.master)

    def add_new_car_to_client(self, client):
        AddCarForm(self.master, client)

    def show_client_details(self, client):

        self.load_clients()

        self.client_frame = ttk.LabelFrame(self.content_frame, text=f"{client.name}", padding=10)
        self.client_frame.pack(fill="x", pady=5)

        ttk.Label(self.client_frame, text=f"Име: {client.name}").pack(padx=10, pady=5)
        ttk.Label(self.client_frame, text=f"Телефон: {client.phone_number}").pack(padx=10, pady=5)

    def show_car_details(self, car, client_name):

        self.load_clients()

        win = tk.Toplevel(self.master)
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
                        command=lambda repair=repair: self.show_repair_details(repair)
                    ).grid(row=row, column=column, padx=5, pady=5, sticky="w")
        finally:
            session.close()

    def show_repair_details(self, repair):
        win = tk.Toplevel(self.master)
        win.title(f"Дата на ремонта: {repair.repair_date}")
        ttk.Label(win, text=f"Километри при ремонта: {repair.repair_km}").pack(padx=10, pady=5)
        ttk.Label(win, text=f"Ремонти: {repair.repairs_type_field}").pack(padx=10, pady=5)
        ttk.Label(win, text=f"Бележки към ремонта: {repair.repair_notes}").pack(padx=10, pady=5)
        ttk.Label(win, text=f"Цена на ремонта: {repair.repair_price}").pack(padx=10, pady=5)