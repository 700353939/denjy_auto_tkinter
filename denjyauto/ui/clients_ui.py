import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.orm import Session
from denjyauto.database import SessionLocal
from denjyauto.forms.edit_client_form import EditClientForm
from denjyauto.forms.new_client_form import NewClientForm
from denjyauto.models.client import Client
from denjyauto.models.car import Car
from denjyauto.context import AppContext
from denjyauto.ui.widgets import create_scrollable_frame, close_parent_window_and
from denjyauto.ui.car_ui import add_new_car_to_client, show_car_details


def load_clients(context: AppContext):
    for widget in context.content_frame.winfo_children():
        widget.destroy()

    session: Session = SessionLocal()

    try:
        clients = session.query(Client).order_by(Client.id.desc()).all()
        for client in clients:

            client_frame = ttk.LabelFrame(
                context.content_frame,
                text=f"Име: {client.name}, телефон: {client.phone_number}",
                padding=10,
                labelanchor="n"
            )
            client_frame.pack(anchor="nw", pady=5, fill="x", expand=True, padx=10)

            ttk.Button(
                client_frame,
                text="ДЕТАЙЛИ",
                style="TButton",
                command=lambda c=client: show_client_details(context, c.id)
            ).pack(side="left", padx=10, pady=5)

            ttk.Button(
                client_frame,
                text="РЕДАКТИРАЙ КЛИЕНТ",
                style="TButton",
                command=lambda cl=client: edit_client(context, cl.id)
            ).pack(side="left", padx=10, pady=5)

            ttk.Button(
                client_frame,
                text="ИЗТРИЙ КЛИЕНТ",
                style="RedText.TButton",
                command=lambda cl=client: delete_client(
                    cl,
                    reload_callback=lambda: load_clients(context))
            ).pack(side="left", padx=10, pady=5)

            ttk.Button(
                client_frame,
                text="ДОБАВИ АВТОМОБИЛ",
                style="TButton",
                command=lambda c=client: add_new_car_to_client(context, c.id)
            ).pack(side="left", padx=10, pady=5)

            cars_frame = ttk.LabelFrame(
                client_frame,
                text="Автомобили",
            )
            cars_frame.pack(side="right", fill="y", pady=5)

            cars = session.query(Car).filter_by(client_id=client.id).order_by(Car.id.desc()).all()
            if not cars:
                ttk.Label(client_frame, text="Няма регистрирани автомобили.").pack(anchor="w", padx=20)
            else:
                for car in cars:
                    ttk.Button(
                        cars_frame,
                        text=f"{car.registration_number}",
                        command=lambda cl=client, c=car: show_car_details(context, c.id, cl)
                    ).pack(side="left", padx=10, pady=5)


    finally:
        session.close()

def load_single_client(context: AppContext, session: Session, client):
    try:
        client_frame = ttk.LabelFrame(
            context.content_frame,
            text=f"Име на клиента: {client.name}, телефон: {client.phone_number}",
            padding=10,
            labelanchor="n"
        )
        client_frame.pack(anchor="nw", pady=5, fill="x", expand=True, padx=10)

        ttk.Button(
            client_frame,
            text="ДЕТАЙЛИ",
            style="TButton",
            command=lambda c=client: show_client_details(context, c.id)
        ).pack(side="left", padx=10, pady=5)

        ttk.Button(
            client_frame,
            text="РЕДАКТИРАЙ КЛИЕНТ",
            style="TButton",
            command=lambda cl=client: edit_client(context, cl.id)
        ).pack(side="left", padx=10, pady=5)

        ttk.Button(
            client_frame,
            text="ИЗТРИЙ КЛИЕНТ",
            style="RedText.TButton",
            command=lambda cl=client: delete_client(
                cl,
                reload_callback=lambda: load_clients(context))
        ).pack(side="left", padx=10, pady=5)

        ttk.Button(
            client_frame,
            text="ДОБАВИ АВТОМОБИЛ",
            style="TButton",
            command=lambda c=client: add_new_car_to_client(context, c.id)
        ).pack(side="left", padx=10, pady=5)

        cars_frame = ttk.LabelFrame(
            client_frame,
            text="Автомобили",
        )
        cars_frame.pack(side="right", fill="y", pady=5)

        cars = session.query(Car).filter_by(client_id=client.id).order_by(Car.id.desc()).all()
        if not cars:
            ttk.Label(client_frame, text="Няма регистрирани автомобили.").pack(anchor="w", padx=20)
        else:
            for car in cars:
                ttk.Button(
                    cars_frame,
                    text=f"{car.registration_number}",
                    command=lambda cl=client, c=car: show_car_details(context, c.id, cl)
                ).pack(side="left", padx=10, pady=5)


    finally:
        session.close()


def add_new_client(context: AppContext):
    def on_client_added():
        load_clients(context)

    NewClientForm(context, on_client_added)

def edit_client(context: AppContext, client_id):
    session: Session = SessionLocal()
    try:
        client = session.query(Client).get(client_id)
        if not client:
            messagebox.showerror("Грешка", "Клиентът не е намерен.")
            return

        EditClientForm(context, client, reload_callback=lambda: show_client_details(context, client_id))

    finally:
        session.close()

def show_client_details(context: AppContext, client_id):
    session: Session = SessionLocal()
    try:
        client = session.query(Client).get(client_id)
        if not client:
            messagebox.showerror("Грешка", "Клиентът не е намерен.")
            return

        win = tk.Toplevel(context.master)
        win.configure(bg="gray80")
        win.title("Детайли за клиента")
        win.geometry("600x600")

        ttk.Label(win, text=f"Име: {client.name}", style="Blue.TLabel").pack(padx=10, pady=5)
        ttk.Label(win, text=f"Телефон: {client.phone_number}", style="Blue.TLabel").pack(padx=10, pady=5)
        ttk.Label(win, text=f"Бележки: {client.client_notes}", wraplength=500, justify="left").pack(padx=10, pady=5)

        client_buttons_frame = ttk.LabelFrame(win, padding=10 )
        client_buttons_frame.pack(side="top", fill="y", pady=5)

        ttk.Button(
            client_buttons_frame,
            text="РЕДАКТИРАЙ КЛИЕНТ",
            style="TButton",
            command=lambda cl=client: close_parent_window_and(edit_client, client_buttons_frame,context, cl.id)
        ).pack(side="left", padx=10, pady=5)

        ttk.Button(
            client_buttons_frame,
            text="ИЗТРИЙ КЛИЕНТ",
            style="RedText.TButton",
            command=lambda cl=client: close_parent_window_and(
                delete_client,
                client_buttons_frame,
                cl,
                reload_callback=lambda: load_clients(context))
        ).pack(side="left", padx=10, pady=5)

        ttk.Button(
            client_buttons_frame,
            text="ДОБАВИ АВТОМОБИЛ",
            style="TButton",
            command=lambda c=client: close_parent_window_and(
                add_new_car_to_client,
                client_buttons_frame,
                context,
                c.id)
        ).pack(side="left", padx=10, pady=5)

        cars_frame = create_scrollable_frame(win)

        cars = session.query(Car).filter_by(client_id=client.id).order_by(Car.id.desc()).all()
        if not cars:
            ttk.Label(cars_frame, text="Няма регистрирани автомобили.").pack(anchor="w", padx=20)
        else:
            for i, car in enumerate(cars):
                row = i // 4
                column = i % 4
                ttk.Button(
                    cars_frame,
                    text=f"{car.registration_number}",
                    command=lambda cl=client, c=car: close_parent_window_and(
                        show_car_details,
                        cars_frame,
                        context,
                        c.id,
                        cl)
                ).grid(row=row, column=column, padx=5, pady=5, sticky="w")

    finally:
        session.close()

def delete_client(client, reload_callback=None):
    confirm = messagebox.askyesno(
        "Потвърждение",
        f"Сигурен ли си, че искаш да изтриеш клиента '{client.name}' и всички свързани данни?")
    if not confirm:
        return

    session: Session = SessionLocal()
    try:
        client = session.query(Client).get(client.id)
        session.delete(client)
        session.commit()
        messagebox.showinfo("Готово", f"Клиентът '{client.name}' е изтрит.")
        if reload_callback:
            reload_callback()
    except Exception as e:
        session.rollback()
        messagebox.showerror("Грешка", f"Неуспешно изтриване: {e}")
    finally:
        session.close()

def search_clients(context: AppContext, query: str):
    query = query.strip().lower()

    for widget in context.content_frame.winfo_children():
        widget.destroy()

    if not query:
        load_clients(context)
        return

    session: Session = SessionLocal()
    try:
        matched_clients = session.query(Client).filter(Client.lower_name.like(f"%{query}%")).all()

        for client in matched_clients:
            load_single_client(context, session, client)

    finally:
        session.close()