import tkinter as tk
from tkinter import ttk, messagebox

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from denjyauto.database import SessionLocal
from denjyauto.forms.add_car_form import AddCarForm
from denjyauto.forms.add_repair_form import AddRepairForm
from denjyauto.forms.edit_car_form import EditCarForm
from denjyauto.forms.edit_repair_form import EditRepairForm
from denjyauto.models.car import Car
from denjyauto.models.client import Client
from denjyauto.models.repair import Repair
from denjyauto.context import AppContext
from denjyauto.ui.widgets import create_copyable_label, create_scrollable_frame, close_parent_window_and


def add_new_car_to_client(context: AppContext, client_id):

    session: Session = SessionLocal()
    try:
        client = session.query(Client).get(client_id)
        if not client:
            messagebox.showerror("Грешка", "Клиентът не е намерен.")
            return

        AddCarForm(context, client, reload_callback=lambda car_id: show_car_details(context, car_id, client))

    finally:
        session.close()

def show_car_details(context: AppContext, car_id, client):
    from denjyauto.ui.clients_ui import show_client_details

    session: Session = SessionLocal()
    try:
        car = session.query(Car).get(car_id)
        if not car:
            messagebox.showerror("Грешка", "Автомобилът не е намерен.")
            return

        win = tk.Toplevel(context.master)
        win.title("Детайли автомобил")
        win.configure(background="gray80")
        win.geometry("600x600")

        ttk.Label(win, text=f"Клиент: {client.name}", foreground="dodger blue").pack(anchor="nw", pady=5, padx=10)

        create_copyable_label(win, text=f"Рег. номер: {car.registration_number}")
        create_copyable_label(win, text=f"VIN: {car.vin}")
        create_copyable_label(win, text=f"Марка: {car.brand}")
        create_copyable_label(win, text=f"Модел: {car.model}")

        year = "" if car.year == 0  else car.year
        create_copyable_label(win, text=f"Година: {year}")

        car_buttons_frame = ttk.Frame(win, padding=10)
        car_buttons_frame.pack(side="top", fill="y", pady=5)

        ttk.Button(
            car_buttons_frame,
            text="ДОБАВИ РЕМОНТ",
            command=lambda: close_parent_window_and(add_repair_to_car, car_buttons_frame, context, car, client)
        ).pack(side="left", pady=10, padx=10)

        ttk.Button(
            car_buttons_frame,
            text="РЕДАКТИРАЙ АВТОМОБИЛА",
            style="TButton",
            command=lambda: close_parent_window_and(edit_car, car_buttons_frame, context, car.id, client)
        ).pack(side="left", pady=10, padx=10)

        ttk.Button(
            car_buttons_frame,
            text="ИЗТРИЙ АВТОМОБИЛА",
            style="RedText.TButton",
            command=lambda: close_parent_window_and(
                delete_car,
                car_buttons_frame,
                car,
                reload_callback=lambda: show_client_details(context, client.id))
        ).pack(side="left", pady=10, padx=10)

        repairs_frame = create_scrollable_frame(win)

        repairs = session.query(Repair).filter_by(car_id=car.id).order_by(Repair.repair_date.desc()).all()
        if not repairs:
            ttk.Label(repairs_frame, text="Няма регистрирани ремонти.").grid(row=0, column=0, sticky="w")
        else:
            for i, repair in enumerate(repairs):
                row = i // 4
                column = i % 4
                ttk.Button(
                    repairs_frame,
                    text=f"Ремонт: {repair.repair_date}",
                    command=lambda r=repair: close_parent_window_and(
                        show_repair_details,
                        repairs_frame,
                        context,
                        r.id,
                        car,
                        client)
                ).grid(row=row, column=column, padx=5, pady=5, sticky="w")

    finally:
        session.close()


def edit_car(context: AppContext, car_id, client):
    session: Session = SessionLocal()
    try:
        car = session.query(Car).get(car_id)
        if not car:
            messagebox.showerror("Грешка", "Автомобилът не е намерен.")
            return
    finally:
        session.close()
    EditCarForm(context, car, client, reload_callback=lambda: show_car_details(context, car_id, client))


def delete_car(car, reload_callback=None):
    confirm = messagebox.askyesno("Потвърждение",
                                  f"Сигурен ли си, че искаш да изтриеш автомобил '{car.registration_number}' "
                                  f"и всички свързани данни?"
                                  )
    if not confirm:
        return

    session: Session = SessionLocal()
    try:
        car = session.query(Car).get(car.id)
        session.delete(car)
        session.commit()
        messagebox.showinfo("Успех", f"Автомобилът '{car.registration_number}' е изтрит.")
        if reload_callback:
            reload_callback()
    except Exception as e:
        session.rollback()
        messagebox.showerror("Грешка", f"Неуспешно изтриване: {e}")
    finally:
        session.close()

def add_repair_to_car(context: AppContext, car, client):
    AddRepairForm(context, car, client, reload_callback=lambda repair_id: show_repair_details(context, repair_id, car, client))

def show_repair_details(context: AppContext, repair_id, car, client):
    session: Session = SessionLocal()
    try:
        repair = session.query(Repair).get(repair_id)
        if not car:
            messagebox.showerror("Грешка", "Автомобилът не е намерен.")
            return
    finally:
        session.close()

    win = tk.Toplevel(context.master)
    win.configure(bg="gray80")
    win.geometry("500x600")
    win.title(f"РЕМОНТ")

    ttk.Label(win, text=f"КЛИЕНТ: {client.name}").pack(anchor="n", padx=10, pady=5)
    ttk.Label(win, text=f"Телефон: {client.phone_number}").pack(anchor="n", padx=10, pady=5)
    ttk.Label(win, text=f"АВТОМОБИЛ: {car.registration_number}").pack(anchor="n", padx=10, pady=5)
    ttk.Label(win, text=f"ДАТА: {repair.repair_date}").pack(anchor="nw", padx=10, pady=5)

    repair_km = "" if repair.repair_km == 0 else repair.repair_km
    ttk.Label(win, text=f"КИЛОМЕТРИ ПРИ РЕМОНТА: {repair_km}").pack(anchor="nw",padx=10, pady=5)

    ttk.Label(win, text=f"РЕМОНТИ: {repair.repairs_type_field}", wraplength=500, justify="left").pack(anchor="nw",padx=10, pady=5)
    ttk.Label(win, text=f"БЕЛЕЖКИ: {repair.repair_notes}", wraplength=500, justify="left").pack(anchor="nw",padx=10, pady=5)
    ttk.Label(win, text=f"ЦЕНА НА РЕМОНТА: {repair.repair_price}").pack(anchor="nw",padx=10, pady=5)

    paid_bool = "Да" if repair.is_it_paid else "Не"
    color = "dodger blue" if repair.is_it_paid else "red"
    ttk.Label(win, text=f"Платено: {paid_bool}", foreground=color).pack(anchor="nw",padx=10, pady=5)


    repair_buttons_frame = ttk.Frame(win, padding=10 )
    repair_buttons_frame.pack(side="top", fill="y", pady=5)

    ttk.Button(
        repair_buttons_frame,
        text="РЕДАКТИРАЙ РЕМОНТА",
        style="TButton",
        command=lambda r=repair: close_parent_window_and(
            edit_repair,
            repair_buttons_frame,
            context,
            r.id,
            car,
            client)
    ).pack(side="left", pady=10, padx=10)

    ttk.Button(
        repair_buttons_frame,
        text="ИЗТРИЙ РЕМОНТА",
        style="RedText.TButton",
        command=lambda r=repair: close_parent_window_and(
            delete_repair,
            repair_buttons_frame,
            r,
            reload_callback=lambda: show_car_details(context, car.id, client))
    ).pack(side="left", pady=10, padx=10)


def edit_repair(context: AppContext, repair_id, car, client):
    session: Session = SessionLocal()
    try:
        repair = session.query(Repair).get(repair_id)
        if not repair:
            messagebox.showerror("Грешка", "Ремонтът не е намерен.")
            return
    finally:
        session.close()
    EditRepairForm(context, repair, car, client, reload_callback=lambda: show_repair_details(context, repair.id, car, client))

def delete_repair(repair, reload_callback=None):
    confirm = messagebox.askyesno("Потвърждение",
                                  f"Сигурен ли си, че искаш да изтриеш ремонта на дата '{repair.repair_date}'?")
    if not confirm:
        return

    session: Session = SessionLocal()
    try:
        repair = session.query(Repair).get(repair.id)
        session.delete(repair)
        session.commit()
        messagebox.showinfo("Успех", f"Ремонтът е изтрит.")
        if reload_callback:
            reload_callback()
    except Exception as e:
        session.rollback()
        messagebox.showerror("Грешка", f"Неуспешно изтриване: {e}")
    finally:
        session.close()


def search_cars(context: AppContext, query: str):
    from denjyauto.ui.clients_ui import load_clients, load_single_client

    query = query.strip().lower()

    for widget in context.content_frame.winfo_children():
        widget.destroy()

    if not query:
        load_clients(context)
        return

    session: Session = SessionLocal()
    try:
        matched_cars = session.query(Car).options(joinedload(Car.client)).filter(Car.lower_registration_number.ilike(f"%{query}%")).all()

        for car in matched_cars:
            load_single_client(context, session, car.client)

    finally:
        session.close()