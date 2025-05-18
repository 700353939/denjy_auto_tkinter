from tkinter import ttk, messagebox
from sqlalchemy.orm import Session
from denjyauto.database import SessionLocal
from denjyauto.forms.edit_client_form import EditClientForm
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

            client_frame = ttk.LabelFrame(
                content_frame,
                text=f"Име на клиента: {client_name}, телефон: {client_phone}",
                padding=10,
                labelanchor="n"
            )
            client_frame.pack(expand=True, fill="both", pady=5)

            cars_frame = ttk.Frame(
                client_frame,
                padding=10
            )
            cars_frame.pack(side="top", fill="y", pady=5)

            cars = session.query(Car).filter_by(client_id=client.id).all()
            if not cars:
                ttk.Label(client_frame, text="Няма регистрирани автомобили.").pack(anchor="w", padx=20)
            else:
                for i, car in enumerate(cars):
                    row = i // 5
                    column = i % 5
                    ttk.Button(
                        cars_frame,
                        text=f"{car.registration_number}",
                        command=lambda c=car: show_car_details(master, c, client_name)
                    ).pack(side="left", padx=10)

            ttk.Button(
                client_frame,
                text="ДОБАВИ АВТОМОБИЛ",
                style="RedText.TButton",
                command=lambda c=client: add_new_car_to_client(master, c)
            ).pack(side="left", padx=10)

            ttk.Button(
                client_frame,
                text="РЕДАКТИРАЙ КЛИЕНТ",
                style="RedText.TButton",
                command=lambda cl=client: edit_client(master, cl, content_frame)
            ).pack(side="left", padx=10)

            ttk.Button(
                client_frame,
                text="ИЗТРИЙ КЛИЕНТ",
                style="RedText.TButton",
                command=lambda cl=client: delete_client(
                    master,
                    cl,
                    reload_callback=lambda: load_clients(master, content_frame))
            ).pack(side="left", padx=10)

    finally:
        session.close()

def open_new_client_form(master):
    NewClientForm(master)

def edit_client(master, client, content_frame):
    EditClientForm(master, client, reload_callback=lambda: load_clients(master, content_frame))

    load_clients(master, content_frame)

def show_client_details(master, content_frame, client):
    load_clients(master, content_frame)

    client_frame = ttk.LabelFrame(content_frame, text=f"{client.name}", padding=10)
    client_frame.pack(fill="x", pady=5)

    ttk.Label(client_frame, text=f"Име: {client.name}").pack(padx=10, pady=5)
    ttk.Label(client_frame, text=f"Телефон: {client.phone_number}").pack(padx=10, pady=5)

def delete_client(master, client, reload_callback=None):
    confirm = messagebox.askyesno("Потвърждение",
                                  f"Сигурен ли си, че искаш да изтриеш клиента '{client.name}' и всички свързани данни?")
    if not confirm:
        return

    session: Session = SessionLocal()
    try:
        client = session.query(Client).get(client.id)
        session.delete(client)
        session.commit()
        messagebox.showinfo("Успех", f"Клиентът '{client.name}' е изтрит.")
        if reload_callback:
            reload_callback()
    except Exception as e:
        session.rollback()
        messagebox.showerror("Грешка", f"Неуспешно изтриване: {e}")
    finally:
        session.close()